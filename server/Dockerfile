    FROM python:3.8.2

    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1

    ARG WATSON_NLU_APIKEY

    RUN apt-get update \
        && apt-get install -y netcat

    ENV APP=/app

    # Change the workdir.
    WORKDIR $APP

    # Copy the rest of the files
    COPY . $APP

    # Install the requirements
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt

    # Generate secrets file
    RUN echo "WATSON_NLU_API_KEY=\"${WATSON_NLU_APIKEY}\"" > djangoapp/api_settings.py

    EXPOSE 8000

    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/app/entrypoint.sh"]

    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]