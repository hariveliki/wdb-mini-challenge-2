#https://github.com/seleniumhq-community/docker-seleniarm

FROM selenium/standalone-chrome

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4444

CMD ["python", "main.py"]