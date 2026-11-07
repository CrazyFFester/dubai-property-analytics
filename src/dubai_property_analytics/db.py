import os

import psycopg


def conn_params() -> dict[str, str]:
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "dbname": os.environ["POSTGRES_DB"],
    }


def connect() -> psycopg.Connection:
    return psycopg.connect(**conn_params())
