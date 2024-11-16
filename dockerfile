FROM python:3.9-slim
WORKDIR /app
# Copiar los archivos de Pipenv y luego instalar dependencias
COPY requirements.txt ./
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el resto del código de la aplicación
COPY . .
EXPOSE 5000
# Comando para ejecutar la aplicación
CMD ["python", "application.py"]