# 1) starting with minimal Python image
FROM python:3.10-slim

# 2) install dependencies
COPY CODE/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copy app source
COPY . /app
WORKDIR /app

# 4) Streamlit port 
EXPOSE 8080

# 5) launch the app

CMD ["sh","-c", \
  "streamlit run CODE/dg_app.py \
   --server.port $PORT \
   --server.address 0.0.0.0"]

