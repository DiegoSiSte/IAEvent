"""Tests del reset y la recuperación de sesión del frontend (T14 — Alcides, M4)."""

import threading

import httpx
from fastapi.testclient import TestClient

from backend.api.routes import session_service
from backend.main import app
from frontend.services.api_client import FacebotApiClient
from frontend.services.session_recovery import (
    MENSAJE_RESET_FALLIDO,
    MENSAJE_RESPUESTA_INVALIDA,
    MENSAJE_SIN_CONEXION,
    ApiResult,
    SessionRecovery,
)


def _cliente_con_backend_real() -> FacebotApiClient:
    """FacebotApiClient conectado al backend real en memoria (sin red)."""
    cliente = FacebotApiClient("http://testserver")
    cliente._client = TestClient(app)
    return cliente


def _cliente_con_transporte(handler) -> FacebotApiClient:
    """FacebotApiClient cuyas respuestas las decide `handler` (simula fallas)."""
    cliente = FacebotApiClient("http://testserver")
    cliente._client = httpx.Client(
        base_url="http://testserver", transport=httpx.MockTransport(handler)
    )
    return cliente


def _sin_conexion(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("conexión rechazada", request=request)


def _sin_dormir(_segundos: float) -> None:
    """Evita esperas reales entre reintentos durante los tests."""


# --- Reset contra el backend real ---------------------------------------------


def test_reiniciar_devuelve_waiting_desde_recognized():
    session_service.set_recognized({"id": "USR001", "name": "Carlos"})
    recovery = SessionRecovery(_cliente_con_backend_real(), dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert resultado.ok
    assert resultado.data == {"status": "waiting", "person": None}
    assert session_service.status() == ("waiting", None)


def test_reiniciar_devuelve_waiting_desde_unknown():
    session_service.set("unknown")
    recovery = SessionRecovery(_cliente_con_backend_real(), dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert resultado.ok
    assert session_service.status() == ("waiting", None)


def test_backend_disponible_con_backend_real():
    recovery = SessionRecovery(_cliente_con_backend_real())

    assert recovery.backend_disponible() is True


def test_obtener_sesion_con_backend_real():
    session_service.reset()
    recovery = SessionRecovery(_cliente_con_backend_real())

    resultado = recovery.obtener_sesion()

    assert resultado.ok
    assert resultado.data == {"status": "waiting", "person": None}


# --- Errores de conexión --------------------------------------------------------


def test_reiniciar_sin_conexion_reintenta_y_avisa():
    llamadas = []

    def handler(request: httpx.Request) -> httpx.Response:
        llamadas.append(request.url.path)
        return _sin_conexion(request)

    esperas = []
    recovery = SessionRecovery(
        _cliente_con_transporte(handler), reintentos=3, espera_segundos=0.5, dormir=esperas.append
    )

    resultado = recovery.reiniciar()

    assert not resultado.ok
    assert resultado.offline
    assert resultado.error == MENSAJE_SIN_CONEXION
    assert llamadas == ["/api/session/reset"] * 3
    assert esperas == [0.5, 0.5]


def test_reiniciar_se_recupera_si_el_backend_vuelve():
    intentos = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        intentos["n"] += 1
        if intentos["n"] < 3:
            return _sin_conexion(request)
        return httpx.Response(200, json={"status": "waiting", "person": None})

    recovery = SessionRecovery(_cliente_con_transporte(handler), reintentos=3, dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert resultado.ok
    assert intentos["n"] == 3


def test_reiniciar_con_tiempo_agotado_se_trata_como_sin_conexion():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("tiempo agotado", request=request)

    recovery = SessionRecovery(_cliente_con_transporte(handler), reintentos=2, dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert not resultado.ok
    assert resultado.offline


def test_reiniciar_no_reintenta_si_la_respuesta_es_invalida():
    llamadas = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        llamadas["n"] += 1
        return httpx.Response(500, text="Internal Server Error")

    recovery = SessionRecovery(_cliente_con_transporte(handler), reintentos=3, dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert not resultado.ok
    assert not resultado.offline
    assert resultado.error == MENSAJE_RESPUESTA_INVALIDA
    assert llamadas["n"] == 1


def test_reiniciar_falla_si_el_backend_no_confirma_waiting():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": "error", "person": None})

    recovery = SessionRecovery(_cliente_con_transporte(handler), dormir=_sin_dormir)

    resultado = recovery.reiniciar()

    assert not resultado.ok
    assert resultado.error == MENSAJE_RESET_FALLIDO


def test_backend_disponible_es_false_sin_conexion():
    recovery = SessionRecovery(_cliente_con_transporte(_sin_conexion))

    assert recovery.backend_disponible() is False


def test_obtener_sesion_sin_conexion_no_lanza_excepcion():
    recovery = SessionRecovery(_cliente_con_transporte(_sin_conexion))

    resultado = recovery.obtener_sesion()

    assert not resultado.ok
    assert resultado.offline
    assert resultado.error == MENSAJE_SIN_CONEXION


# --- Reinicio automático tras la interacción ------------------------------------


def test_programar_reinicio_vuelve_a_waiting():
    session_service.set("unknown")
    recovery = SessionRecovery(_cliente_con_backend_real(), dormir=_sin_dormir)
    terminado = threading.Event()
    resultados: list[ApiResult] = []

    def al_terminar(resultado: ApiResult) -> None:
        resultados.append(resultado)
        terminado.set()

    recovery.programar_reinicio(0.05, al_terminar)

    assert terminado.wait(timeout=2)
    assert resultados[0].ok
    assert session_service.status() == ("waiting", None)
    assert recovery.reinicio_pendiente is False


def test_cancelar_reinicio_evita_el_reset():
    recovery = SessionRecovery(_cliente_con_backend_real(), dormir=_sin_dormir)
    llamado = threading.Event()

    recovery.programar_reinicio(0.2, lambda _resultado: llamado.set())
    assert recovery.reinicio_pendiente is True
    recovery.cancelar_reinicio()

    assert not llamado.wait(timeout=0.4)
    assert recovery.reinicio_pendiente is False
