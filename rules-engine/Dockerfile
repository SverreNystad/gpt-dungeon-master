FROM python:3.13

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8000

CMD [ "uvicorn", "webserver:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--proxy-headers" ]