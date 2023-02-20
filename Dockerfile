FROM python:3.10 AS builder

EXPOSE 8000
WORKDIR /energy-prime-back

RUN pip install -U poetry==1.3.2

COPY ./poetry.lock poetry.toml pyproject.toml /energy-prime-back/
RUN poetry install --only main

FROM python:3.10-slim

RUN apt update && apt install -y libpq-dev

WORKDIR /energy-prime-back
COPY . /energy-prime-back
COPY --from=builder /energy-prime-back/.venv /energy-prime-back/.venv
ENV PATH=/energy-prime-back/.venv/bin:$PATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
