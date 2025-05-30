# 1) start from a minimal Python image
FROM python:3.10-slim

# 2) install dependencies
COPY CODE/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copy in your app source
COPY . /app
WORKDIR /app

# 4) expose the port Streamlit uses
EXPOSE 8501

# 5) launch your app
CMD ["streamlit", "run", "CODE/dg_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
