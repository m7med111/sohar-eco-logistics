# 1. Use a lightweight Python base
FROM python:3.9-slim

# 2. Set the working directory to /app
WORKDIR /app

# 3. Copy requirements first (to cache them)
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your app code
COPY . .

# 6. Expose the port used by Streamlit
EXPOSE 8501

# 7. Run the app
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]