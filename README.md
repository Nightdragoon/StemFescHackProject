<p align="center">
  <img src="assets/banner.jpg" width="600"/>
</p>
## ProfAI – Profesor con IA Emocionalmente Inteligente

Sistema educativo impulsado por IA que enseña teoría y práctica en una vertical específica, detectando la confusión del alumno y adaptando la lección en tiempo real.  



<p align="center">
  <img src="assets/background.png" width="600"/>
</p>

---

## Videos
### Demo
https://youtu.be/demo_profai

### Presentación Técnica
https://youtu.be/presentacion_profai

---

## Descripción

**ProfAI** es un profesor virtual con inteligencia emocional que enseña teoría y/o herramientas de Inteligencia Artificial, con la capacidad de:

- **Detectar confusión o frustración** en el alumno.
- Adaptar la explicación y el nivel de detalle en tiempo real.
- Proporcionar ejercicios prácticos con **feedback instantáneo**.
- Presentar contenido en múltiples formatos: video, audio, diapositivas o texto.

El sistema se organiza en **4 módulos principales**:
1. **Generación de Contenido (El Cerebro 🧠)** – Crea explicaciones, ejemplos, cuestionarios y guiones.
2. **Entrega de Contenido (La Cara y la Voz 🗣️)** – Presenta el contenido en el formato elegido (texto, audio o video con avatar).
3. **Detección de Emociones (El Corazón ❤️)** – Analiza el estado emocional del alumno para adaptar la clase.
4. **Práctica y Feedback (Las Manos 👐)** – Permite al alumno practicar código o ejercicios con retroalimentación inmediata.

---

## Setup

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Virtual environment (recomendado)

---

### Variables de Entorno

Antes de ejecutar el código, debes configurar un archivo `.env` en la carpeta raíz con tus claves de API:

```env
OPENAI_API_KEY=tu_clave_openai
HUME_API_KEY=tu_clave_hume
REPLIT_API_KEY=tu_clave_replit
```
### Para cargarlo automáticamente en Linux/macOS:

```bash
export $(cat .env | xargs)
En Windows PowerShell:
```
Copiar
Editar
$env:OPENAI_API_KEY="tu_clave_openai"
$env:HUME_API_KEY="tu_clave_hume"
$env:REPLIT_API_KEY="tu_clave_replit"
Backend – Instalación y Ejecución
Ir al directorio del backend:
bash
Copiar
Editar
cd backend
Crear y activar un entorno virtual:
bash
Copiar
Editar
python -m venv .venv
# Activar en Linux/macOS
source .venv/bin/activate
# Activar en Windows
.venv\Scripts\activate
Instalar dependencias:
bash
Copiar
Editar
pip install -r requirements.txt
Iniciar el servidor:
bash
Copiar
Editar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
📍 El backend estará en: http://localhost:8000
📍 Documentación de API: http://localhost:8000/docs

Frontend – Instalación y Ejecución
Ir al directorio del frontend:
bash
Copiar
Editar
cd frontend
Crear y activar un entorno virtual:
bash
Copiar
Editar
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
Instalar dependencias:
bash
Copiar
Editar
pip install -r requirements.txt
Ejecutar la aplicación:
bash
Copiar
Editar
streamlit run app.py
📍 El frontend estará en: http://localhost:8501

Probando la Aplicación
Asegúrate de que backend y frontend están corriendo.

Selecciona el formato de lección (video, texto, audio).

Comienza una sesión y responde preguntas.

Observa cómo ProfAI adapta las explicaciones según tu interacción.

Realiza ejercicios prácticos y recibe retroalimentación automática.

Endpoints Principales
POST /api/v1/generate-content/ – Generar material educativo.

POST /api/v1/emotion-detection/ – Analizar estado emocional del alumno.

POST /api/v1/practice-feedback/ – Evaluar código y dar feedback.

GET /api/v1/session/{id} – Obtener estado de una sesión de aprendizaje.

Troubleshooting
Verifica que .env tiene las claves correctas y sin espacios extras.

Confirma que las librerías están instaladas en el entorno virtual.

Si usas Windows, ejecuta siempre desde PowerShell o CMD con permisos.

Reinicia el backend si cambiaste variables de entorno.
