

## Run migrations whenever SQLAlchemy Object Model changes

- we change the SQLAlchemy Object Model, when we want to modify the Relational Data schema.


To generate migrations
```sh
docker-compose run -it --build --rm alembic revision --autogenerate -m "<commit-like message>"
```

To upgrade live staging DB
```sh
docker-compose run -it --build --rm alembic upgrade head
```

To downgrade live staging DB
```sh
docker-compose run -it --build --rm alembic downgrade <revision_id>
```


Generate SQL script and print in console
```sh
docker-compose run -it --build --rm alembic revision --sql -m "<commit message>"
```


## During development

Deploy the services in Staging: to work on DB migrations:


```sh
export OKR_APP_DEPLOY_MODE='staging'
docker-compose up frontend --build
```

---

During development to generate a new migration the DB state needs to be in sync with the chain of migration scripts, so that we get a "correct DIFF".

This means that we need a way during development to:

- start up `dev` DB with empty schema
- apply current migrations
  - while ensuring the `env.py` includes an sqlalchemy.url that name resolution (roughly DNS) can work with
- Synced state reached

    useful when we want to apply the migrations (and verify they work) in order to commit the migration generated script (during development)

OR
- start up `dev` DB with data already synced

    useful when we want to update the production DB instance schema/state


Container that runs migrations
- has proper python deps installed
- can discover DB service in network while doing Name resolution
