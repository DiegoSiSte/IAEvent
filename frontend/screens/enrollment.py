"""Inscripción de una plantilla facial para un participante consentido."""

import asyncio
from collections.abc import Callable

import flet as ft
import httpx

from frontend.services.api_client import FacebotApiClient


class EnrollmentScreen(ft.Column):
    def __init__(
        self,
        picker: ft.FilePicker,
        api: FacebotApiClient,
        on_back: Callable,
    ) -> None:
        self._picker = picker
        self._api = api
        self._image_bytes: bytes | None = None
        self._profile_id = ft.TextField(label="ID del participante", hint_text="Ej. USR001")
        self._consent = ft.Checkbox(
            label="Confirmo que el participante autorizó el uso de su rostro.",
            value=False,
        )
        self._file_label = ft.Text("No se ha seleccionado una imagen.", color="#BAC9DB")
        self._message = ft.Text("", text_align=ft.TextAlign.CENTER)
        self._submit_button = ft.Button(
            "Inscribir rostro",
            icon=ft.Icons.PERSON_ADD,
            bgcolor="#6DE8D1",
            color="#10222B",
            on_click=self._submit,
        )
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            tight=True,
            controls=[
                ft.Icon(ft.Icons.FACE, size=48, color="#6DE8D1"),
                ft.Text("Inscripción facial", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "El participante debe tener un perfil con consentimiento en la base de datos. "
                    "Selecciona una foto clara que muestre un solo rostro.",
                    size=15,
                    color="#BAC9DB",
                    text_align=ft.TextAlign.CENTER,
                ),
                self._profile_id,
                self._consent,
                ft.Button(
                    "Elegir foto",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=self._pick_image,
                ),
                self._file_label,
                self._message,
                self._submit_button,
                ft.Button("Volver", icon=ft.Icons.ARROW_BACK, on_click=on_back),
            ],
        )

    async def _pick_image(self, event: ft.Event) -> None:
        files = await self._picker.pick_files(
            dialog_title="Selecciona una foto frontal",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=["jpg", "jpeg", "png"],
            allow_multiple=False,
            with_data=True,
        )
        if not files:
            return
        selected = files[0]
        if selected.bytes is None:
            self._set_message("No se pudo leer el archivo seleccionado.", error=True)
            return
        if len(selected.bytes) > 8 * 1024 * 1024:
            self._image_bytes = None
            self._file_label.value = "La imagen supera el límite de 8 MB."
            self._set_message("Selecciona una imagen más pequeña.", error=True)
            return
        self._image_bytes = selected.bytes
        self._file_label.value = selected.name
        self._set_message("Foto cargada; se enviará solo para crear la plantilla facial.")
        self.update()

    async def _submit(self, event: ft.Event) -> None:
        profile_id = (self._profile_id.value or "").strip()
        if not profile_id:
            self._set_message("Escribe el ID que aparece en profiles.json.", error=True)
            return
        if not self._consent.value:
            self._set_message("Confirma el consentimiento antes de inscribir.", error=True)
            return
        if self._image_bytes is None:
            self._set_message("Selecciona una foto antes de inscribir.", error=True)
            return

        self._submit_button.disabled = True
        self._set_message("Procesando la imagen...")
        try:
            result = await asyncio.to_thread(
                self._api.enroll_participant,
                profile_id,
                self._image_bytes,
            )
        except httpx.HTTPStatusError as exc:
            detail = exc.response.json().get("detail", "No se pudo completar la inscripción.")
            self._set_message(str(detail), error=True)
        except httpx.HTTPError:
            self._set_message("No se pudo conectar con FACEBOT. Verifica que el backend esté activo.", error=True)
        else:
            self._image_bytes = None
            self._file_label.value = "Foto procesada; la imagen original no se conserva."
            self._set_message(
                f"Inscripción completada para {result.get('profile_id', profile_id)}. "
                "La plantilla se guardó localmente."
            )
        finally:
            self._submit_button.disabled = False
            self.update()

    def _set_message(self, message: str, error: bool = False) -> None:
        self._message.value = message
        self._message.color = "#FF9A9A" if error else "#6DE8D1"
        self.update()
