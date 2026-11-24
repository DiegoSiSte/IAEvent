"""Reset y recuperación de la sesión en el frontend (T14 — Alcides, M4).

Envuelve al cliente HTTP (`FacebotApiClient`) para que el frontend:

- reinicie la sesión con ``POST /api/session/reset`` y confirme que volvió a
  ``waiting`` (S7, S10 regla 10);
- maneje los errores de conexión con el backend sin cerrarse (S4, S9);
- programe el regreso automático a ``waiting`` después de una interacción.

Este módulo no dibuja pantallas ni navega: devuelve resultados simples
(`ApiResult`) que la navegación del frontend (T13) usa para decidir qué mostrar.
No accede a ``profiles.json`` ni hace reconocimiento facial (S4).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from threading import Lock, Timer
from typing import Any, Callable, Dict, Optional, Protocol

import httpx

WAITING = "waiting"

MENSAJE_SIN_CONEXION = "No se pudo conectar con el servidor de FACEBOT."
MENSAJE_RESPUESTA_INVALIDA = "El servidor respondió con datos no válidos."
MENSAJE_RESET_FALLIDO = "No se pudo reiniciar la sesión."


class SessionApi(Protocol):
    """Lo mínimo que necesita este módulo del cliente HTTP (FacebotApiClient)."""

    def get_status(self) -> Dict[str, Any]: ...

    def get_session(self) -> Dict[str, Any]: ...

    def reset_session(self) -> Dict[str, Any]: ...


@dataclass(frozen=True)
class ApiResult:
    """Resultado de una llamada al backend, sin lanzar excepciones a la interfaz.

    - ``ok``: la llamada funcionó y la respuesta tiene la forma esperada.
    - ``data``: el JSON recibido (o ``None`` si falló).
    - ``offline``: el backend no respondió (sin red, apagado o tiempo agotado).
    - ``error``: mensaje en español para mostrar en pantalla.
    """

    ok: bool
    data: Optional[Dict[str, Any]] = None
    offline: bool = False
    error: Optional[str] = None


def _llamar(funcion: Callable[[], Dict[str, Any]]) -> ApiResult:
    """Ejecuta una llamada del cliente y convierte los errores en un ApiResult."""
    try:
        data = funcion()
    except httpx.TransportError:
        # Conexión rechazada, sin red o tiempo de espera agotado.
        return ApiResult(ok=False, offline=True, error=MENSAJE_SIN_CONEXION)
    except (httpx.HTTPError, ValueError):
        # Error HTTP o respuesta que no es JSON.
        return ApiResult(ok=False, error=MENSAJE_RESPUESTA_INVALIDA)

    if not isinstance(data, dict):
        return ApiResult(ok=False, error=MENSAJE_RESPUESTA_INVALIDA)
    return ApiResult(ok=True, data=data)


class SessionRecovery:
    """Reset de la sesión y recuperación ante errores de conexión (T14)."""

    def __init__(
        self,
        api: SessionApi,
        reintentos: int = 3,
        espera_segundos: float = 1.0,
        dormir: Callable[[float], None] = time.sleep,
    ) -> None:
        if reintentos < 1:
            raise ValueError("reintentos debe ser al menos 1")
        self._api = api
        self._reintentos = reintentos
        self._espera = espera_segundos
        self._dormir = dormir
        self._lock = Lock()
        self._temporizador: Optional[Timer] = None

    def backend_disponible(self) -> bool:
        """``True`` si ``GET /api/status`` responde ``online``."""
        resultado = _llamar(self._api.get_status)
        return resultado.ok and resultado.data is not None and resultado.data.get("status") == "online"

    def obtener_sesion(self) -> ApiResult:
        """``GET /api/session`` sin lanzar excepciones (para el sondeo de T13)."""
        resultado = _llamar(self._api.get_session)
        if resultado.ok and resultado.data is not None and "status" not in resultado.data:
            return ApiResult(ok=False, error=MENSAJE_RESPUESTA_INVALIDA)
        return resultado

    def reiniciar(self) -> ApiResult:
        """``POST /api/session/reset`` con reintentos.

        Solo reintenta cuando el backend no responde. Devuelve ``ok=True``
        únicamente si el backend confirma el estado ``waiting``.
        """
        resultado = ApiResult(ok=False, error=MENSAJE_RESET_FALLIDO)
        for intento in range(1, self._reintentos + 1):
            resultado = _llamar(self._api.reset_session)
            if resultado.ok:
                if resultado.data is not None and resultado.data.get("status") == WAITING:
                    return resultado
                return ApiResult(ok=False, data=resultado.data, error=MENSAJE_RESET_FALLIDO)
            if not resultado.offline:
                return resultado
            if intento < self._reintentos:
                self._dormir(self._espera)
        return resultado

    def programar_reinicio(
        self,
        segundos: float,
        al_terminar: Callable[[ApiResult], None],
    ) -> None:
        """Reinicia la sesión automáticamente después de ``segundos``.

        Se usa al mostrar las pantallas ``recognized`` o ``unknown``. Si ya
        había un reinicio programado, se reemplaza. ``al_terminar`` recibe el
        ``ApiResult`` del reset y se ejecuta en un hilo en segundo plano.
        """
        if segundos < 0:
            raise ValueError("segundos no puede ser negativo")

        def _ejecutar() -> None:
            with self._lock:
                self._temporizador = None
            al_terminar(self.reiniciar())

        with self._lock:
            if self._temporizador is not None:
                self._temporizador.cancel()
            self._temporizador = Timer(segundos, _ejecutar)
            self._temporizador.daemon = True
            self._temporizador.start()

    def cancelar_reinicio(self) -> None:
        """Cancela el reinicio automático pendiente, si existe."""
        with self._lock:
            if self._temporizador is not None:
                self._temporizador.cancel()
                self._temporizador = None

    @property
    def reinicio_pendiente(self) -> bool:
        """``True`` mientras haya un reinicio automático programado."""
        with self._lock:
            return self._temporizador is not None
