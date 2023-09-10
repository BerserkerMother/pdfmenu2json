FROM continuumio/miniconda3

WORKDIR /app

ADD src/ /app

ADD spec-file.txt /app

RUN conda install --file spec-file.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app