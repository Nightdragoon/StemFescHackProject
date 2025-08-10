<div align="center">
<h1 align="center">
ProfAI – Voice-Driven AI Professor with Emotional Intelligence<br />
<br />
<a href="assets/banner.jpg">
<img src="assets/banner.jpg" alt="banner" width="500">
</a>
</h1>
</div>
---

## Videos
### Demo
https://youtu.be/demo_profai

### Technical Presentation
https://youtu.be/presentacion_profai

---

## Description

**ProfAI** is a virtual teacher with emotional intelligence that teaches Artificial Intelligence theory and/or tools, with the ability to:

- **Detect confusion or frustration** in the student.
- Adapt the explanation and level of detail in real time.
- Provide practical exercises with **instant feedback**.
- Present content in multiple formats: video, audio, slides, or text.

The system is organized into **4 main modules**:
1. **Content Generation (The Brain 🧠)** – Create explanations, examples, quizzes, and scripts.
2. **Content Delivery (The Face and Voice 🗣️)** – Present the content in the chosen format (text, audio, or video with an avatar).
3. **Emotion Detection (The Heart ❤️)** – Analyzes the student's emotional state to adapt the lesson.
4. **Practice and Feedback (The Hands 👐)** – Allows the student to practice code or exercises with immediate feedback.

---

## Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

---

### Environment Variables

Before running the code, you must set up a `.env` file in the root folder with your API keys:

```env
OPENAI_API_KEY=your_openai_key
HUME_API_KEY=your_hume_key
REPLIT_API_KEY=your_replit_key
```
### To load it automatically on Linux/macOS:

```bash
export $(cat .env | xargs)
On Windows PowerShell:
```
Copy
Edit
$env:OPENAI_API_KEY="your_openai_key"
$env:HUME_API_KEY="your_hume_key"
$env:REPLIT_API_KEY="your_replit_key"
Backend – Installation and Execution
Go to the backend directory:
bash
Copy
Edit
cd backend
Create and activate a virtual environment:
bash
Copy
Edit
python -m venv .venv
# Activate on Linux/macOS
source .venv/bin/activate
# Activate on Windows
.venv\Scripts\activate
Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Start the server:
bash
Copy
Edit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
📍 The backend will be located at: http://localhost:8000
📍 API documentation: http://localhost:8000/docs

Frontend – Installation and Running
Go to the frontend directory:
bash
Copy
Edit
cd frontend
Create and activate a virtual environment:
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows
Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Run the application:
bash
Copy
Edit
streamlit run app.py
📍 The frontend will be located at: http://localhost:8501

Testing the Application
Make sure the backend and frontend are running.

Select the lesson format (video, text, audio).

Start a session and answer questions.

Watch how ProfAI adapts explanations based on your interaction.

Do practical exercises and receive automatic feedback.

Main Endpoints
POST /api/v1/generate-content/ – Generate educational material.

POST /api/v1/emotion-detection/ – Analyze the student's emotional state.

POST /api/v1/practice-feedback/ – Evaluate code and provide feedback.

GET /api/v1/session/{id} – Get the status of a learning session.

Troubleshooting
Verify that .env has the correct keys and no extra spaces.

Confirm that the libraries are installed in the virtual environment.

If using Windows, always run from PowerShell or CMD with permissions.

Restart the backend if you changed environment variables.
