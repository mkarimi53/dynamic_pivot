FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir streamlit pandas openpyxl

EXPOSE 8501
CMD ["streamlit", "run", "pivot_explorer.py", "--server.address=0.0.0.0"]
