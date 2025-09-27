@echo off
echo 🚀 Starting Coding Mentor Chatbot...
echo.

echo 📦 Installing dependencies...
pip install -r requirements_full.txt
echo.

echo 🔧 Starting FastAPI backend...
start "FastAPI Backend" cmd /k "python -m uvicorn backend_api:app --reload --port 8000"

echo ⏳ Waiting for backend to start...
timeout /t 5

echo 🎨 Starting Streamlit frontend...
python -m streamlit run streamlit_frontend.py

pause