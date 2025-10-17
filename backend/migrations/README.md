# Generic single-database configuration.

When you make changes to the `ORM Model`, the `migrations` scripts
**should be updated** (and commited) too, to help human Operators, update their "live" DB instance, later

## Update ORM - Guide 

For example if, you have a live DB as part of **Staging** deployment locally:

<table>
<tr>
<td><strong>Deploy Staging</strong></td>
<td><pre><code>export OKR_APP_DEPLOY_MODE='staging' <br>docker-compose up db backend frontend --build</code></pre></td>
</tr>
<tr>
<td><strong>Run only DB</strong></td>
<td><pre><code>export OKR_APP_DEPLOY_MODE='staging' <br>docker-compose up db</code></pre></td>
</tr>
</table>

1. Ensure that **live DB reflects commited "migration chain"**
    ```sh
    docker-compose run -it --build --rm alembic upgrade head
    ```

2. And then **generate** and **add new migration script** to the chain
    ```sh
    docker-compose run -it --build --rm alembic revision --autogenerate -m "<commit-like message>"
    ```

**Commit** `ORM` and `migrations` changes together!

### Other operations

See immenent SQL statements to be executed for live DB update

```sh
docker-compose run -it --build --rm alembic revision --sql
```

Target custom DB service using `DATABASE_URL` env var
Example: for db exposed by default `docker-compose`

```sh
docker-compose run -it --build --rm -e DATABASE_URL=postgresql://postgres:password@localhost:5433/okr_db alembic revision --autogenerate -m "<commit-like message>"
```

## Reboot Dev DB - Guide

1. Delete volume with Development (temporary) data, ie used for testing

    ```sh
    docker volume rm okr_db_staging
    ```

2. Start PostgreSQL service, create tables with [schema](../../db/schema.sql), and put some [toy data](../../db/data.sql)

    ```sh
    export OKR_APP_DEPLOY_MODE='staging' docker-compose up db
    ```

3. Apply migrations scripts to sync "live DB" with local checkout

    ```sh
    docker-compose run -it --build --rm alembic upgrade head
    ```

---

## Other

Deploy the services in Staging: to work on DB migrations:


```sh
export OKR_APP_DEPLOY_MODE='staging'
docker-compose up frontend --build
```

```sh
uv venv env -p python3.11
uv export --frozen --extra migrations -o "p+m.txt"
source env/bin/activate
uv pip install --no-deps -r "p+m.txt"
```

**Configure `sqlalchemy.url` in **alembic.ini** to point to DB service

To generate migrations
```sh
alembic revision --autogenerate -m "<commit-like message>"
```


To upgrade live staging DB
```sh
alembic upgrade head"
```

To downgrade live staging DB
```sh
alembic downgrade <revision_id>
```
