"""Servicio de reconocimacial — implementación (M5 - Diego).

Detección de rostros con OpenCV (Haar cascade); inscripción de plantillas
localmente; reconocimacial por similitud (coseno) con umbral de confianza.
Respeta (§10): solo participantes inscritos y consensuados. Sin bases de
datasets externas (§10): plantillas en memoria, datos sintéticos para pruebas.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple

import cv2
import numpy as np


class FaceService:
    """Detección, inscripción y reconocimacial de rostros (plantillas en memoria)."""

    def __init__(
        self,
        detector: Optional[Any] = None,
        face_size: Tuple[int, int] = (64, 64),
        confidence_threshold: float = 0.6,
    ) -> None:
        self.face_size = face_size
        self.confidence_threshold = confidence_threshold
        if detector is None:
            detector = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
        self._detector = detector
        self._templates: Dict[str, np.ndarray] = {}

    # -- detección ------------------------------------------------------

    def detect_faces(self, frame: Any) -> List[np.ndarray]:
        """Rostros detectados en un frame: crops normalizados (unidimensionales)."""
        gray = cv2.cvtColor(np.asarray(frame), cv2.COLOR_BGR2GRAY)
        boxes = self._detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(32, 32)
        )
        faces: List[np.ndarray] = []
        for (x, y, w, h) in boxes:
            if w <= 0 or h <= 0:
                continue
            crop = gray[y : y + h, x : x + w]
            if crop.size == 0:
                continue
            faces.append(self._normalize_face(crop))
        return faces

    def _normalize_face(self, face: Any) -> np.ndarray:
        """Preprocesa un rostro: equalización, escalado y normalización L2."""
        gray = np.asarray(face)
        if gray.ndim == 3:
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.resize(gray, self.face_size)
        vector = gray.astype(np.float32).ravel()
        norm = float(np.linalg.norm(vector))
        return vector / norm if norm > 0 else vector

    @staticmethod
    def _similarity(face: np.ndarray, template: np.ndarray) -> float:
        if face.shape != template.shape:
            return 0.0
        norm_face = float(np.linalg.norm(face))
        norm_template = float(np.linalg.norm(template))
        if norm_face == 0 or norm_template == 0:
            return 0.0
        return float(np.dot(face, template) / (norm_face * norm_template))

    # -- inscripción ----------------------------------------------------

    def enroll(self, profile_id: str, face: np.ndarray) -> bool:
        """Inscribe la plantilla de un rostro (§5). False si ya está inscrito."""
        if profile_id in self._templates:
            return False
        self._templates[profile_id] = self._normalize_face(face)
        return True

    def enroll_if_consented(
        self, profile_id: str, face: np.ndarray, consent_checker: Callable[[str], bool]
    ) -> bool:
        """Inscribe solo si el participante dio consent (§10, §5)."""
        if consent_checker is not None and not consent_checker(profile_id):
            return False
        return self.enroll(profile_id, face)

    def is_enrolled(self, profile_id: str) -> bool:
        return profile_id in self._templates

    def template_count(self, profile_id: str) -> int:
        """Número de plantillas inscritas para un participante (0/1, §10)."""
        return int(self.is_enrolled(profile_id))

    def reset(self) -> None:
        """Limpia las plantillas inscritas (§10, regla 8)."""
        self._templates.clear()

    # -- reconocimacial --------------------------------------------------

    def _best_match(self, face: np.ndarray) -> Tuple[Optional[str], float]:
        best_id: Optional[str] = None
        best_sim = 0.0
        for profile_id, template in self._templates.items():
            sim = self._similarity(face, template)
            if sim > best_sim:
                best_sim, best_id = sim, profile_id
        return best_id, best_sim

    def _match(
        self, face: np.ndarray, consent_checker: Optional[Callable[[str], bool]] = None
    ) -> Optional[str]:
        best_id, best_sim = self._best_match(face)
        if best_id is None or best_sim < self.confidence_threshold:
            return None
        if consent_checker is not None and not consent_checker(best_id):
            return None
        return best_id

    def recognize_face(
        self, face: np.ndarray, consent_checker: Optional[Callable[[str], bool]] = None
    ) -> Optional[str]:
        """Reconoce un rostro procesado (sin detección); útil para pruebas."""
        return self._match(self._normalize_face(face), consent_checker)

    def recognize(
        self, frame: Any, consent_checker: Optional[Callable[[str], bool]] = None
    ) -> Optional[str]:
        """Detecta y reconoce en un frame; devuelve el id con mejor confianza.

        Devuelve None si nada coincide o no hay consent (§10).
        """
        for face in self.detect_faces(frame):
            profile_id = self._match(face, consent_checker)
            if profile_id is not None:
                return profile_id
        return None


_service = FaceService()


def enroll_participant(profile_id: str, frame: Optional[np.ndarray]) -> int:
    """Inscribe la plantilla de un rostro de un participante consensuado (§5, §10).

    Devuelve el número de plantillas inscritas para el participante.
    """
    if frame is not None:
        faces = _service.detect_faces(frame)
        if faces:
            _service.enroll(profile_id, faces[0])
    return _service.template_count(profile_id)


def recognize(
    frame: Any, consent_checker: Optional[Callable[[str], bool]] = None
) -> Optional[str]:
    """Detecta y reconoce en un frame; devuelve el id con mejor confianza o None (§10)."""
    return _service.recognize(frame, consent_checker)
