FROM python:3.10-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

COPY ./application.yml ./

COPY ./dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl

CMD ["gunicorn", "todos_app.wsgi:app", "-w", "1", "--bind", "0.0.0.0:8000"]