import os

import dj_database_url
import environ

env = environ.Env()
environ.Env.read_env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SQLITE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

POSTGRESQL = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRESQL_NAME"),
        "USER": env("POSTGRESQL_USER"),
        "PASSWORD": env("POSTGRESQL_PASSWORD"),
        "HOST": env("POSTGRESQL_HOST"),
        "PORT": env("POSTGRESQL_PORT"),
    }
}

MYSQL = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "traditional",
        },
    }
}

RENDER = {
    'default': dj_database_url.parse(env("DATABASE_URL"))
}

SUPABASE = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("SUP_NAME"),
        "USER": env("SUP_USER"),
        "PASSWORD": env("SUP_PASSWORD"),
        "HOST": env("SUP_HOST"),
        "PORT": env("SUP_PORT"),
    }
}