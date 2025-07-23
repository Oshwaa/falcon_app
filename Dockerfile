FROM python:3.11-slim

WORKDIR /app

COPY requirementsALL.txt .

#no cache-dir (avoids storing temporary files that bloats docker image)
RUN pip install --no-cache-dir -r requirementsALL.txt

#Copies everyting from projec into the container's  current workdir
COPY . .

#JUST AN INFO, DOES NOT OPEN OR PUBLISH A PORT (DECLARES CONTAINER INTENDS TO LISTEN TO PORT)
EXPOSE 8000

#Actual commmand to run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
