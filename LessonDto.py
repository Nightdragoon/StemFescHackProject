# LessonDto.py
from pydantic import BaseModel, Field
from typing import List

# Esta clase define la estructura de nuestro plan de lección
class HybridLesson(BaseModel):
    title: str = Field(description="Un título corto y atractivo para el video, estilo YouTube.")
    theory_script: str = Field(description="El guion para la parte teórica. Debe explicar el concepto de forma simple e incluir una buena analogía.")
    bridge_script: str = Field(description="Una frase corta que conecte la teoría con la parte práctica del video.")
    tooling_script_steps: List[str] = Field(description="Una lista de pasos para la narración de la parte práctica. Cada paso describe una acción a mostrar en la pantalla.")

