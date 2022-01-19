# FastAPI + ormar

- [FastAPI + ormar](#fastapi--ormar)
  - [.env](#env)
  - [Database migration](#database-migration)
    - [Step1: Initiate alembic(only once)](#step1-initiate-alembiconly-once)
    - [Step2: Set metadata and models](#step2-set-metadata-and-models)
    - [Step3: Set DB url](#step3-set-db-url)
    - [Step4: (Auto) Generate migration files](#step4-auto-generate-migration-files)
    - [Step5: Apply migrations](#step5-apply-migrations)
    - [NOTES](#notes)
      - [1. Import ormar into migration files](#1-import-ormar-into-migration-files)
  - [Switching to Test Database](#switching-to-test-database)

## .env

```sh
ENVIRONMENT=develop
```

## Database migration

When using ormar, we need to make migration files by ourselves.
For this we use **[alembic](https://github.com/alembic/alembic)**.

### Step1: Initiate alembic(only once)

```sh
alembic init migrations
```

`migrations` is a name of the folder. This can be anything.

### Step2: Set metadata and models

When making a migration for your models, you need to **import** the models into `env.py` created by alembic and set the metadata to `target_metadata`.

```py
# in migrations/env.py
from .database import metadata
from .models import Book

target_metadata = metadata
```

### Step3: Set DB url

Usually you would need to set the `sqlalchemy.url` in your alembic file. But in order to make this connection more dynamic, we set this value in `env.py` as follows.

```py
# in migrations/env.py
from .database import get_db_url

config.set_main_option("sqlalchemy.url", get_db_url())
```

### Step4: (Auto) Generate migration files

```sh
alembic revision --autogenerate -m "<write migration comments>"
```

### Step5: Apply migrations

```sh
alembic upgrade head
```

### NOTES

#### 1. Import ormar into migration files

After running `alembic revision --autogenerate -m "<write migration comments>"`, you may need to import `ormar` package to the file that is generated.

## Switching to Test Database

If you want to use a different database for running unit tests, change the value of environment variable ENVIRONMENT to `test`

```py
from .settings import settings


TEST_DB_URL = f"sqlite:///{str(settings.base_dir)}/db/test_db.sqlite"
DB_URL = f"sqlite:///{str(settings.base_dir)}/db/dev_db.sqlite"
# DB_URL = f"postgresql://root:root1234@db:5432/dev_db" # your DB url


def get_db_url():
    if settings.environment == "test":
        return TEST_DB_URL
    return DB_URL
```
