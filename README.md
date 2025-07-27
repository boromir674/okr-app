# OKR Desktop Application

> `Objectives and Key Results` goal-setting framework for individuals.

**OKR App** is an open-source `Objectives and Key Results` full-stack application.


## Run in prod

```sh
export OKR_APP_DEPLOY_MODE='prod'
docker-compose up db backend frontend --build
```

## Run staging

Useful for Staging deployment, where we want some toy data to be inserted in the DB

```sh
export OKR_APP_DEPLOY_MODE='staging'
docker-compose up db backend frontend --build
```

### Delete staging data to start afresh db on init

1. Stop compose
2. Remove containers
    
    ```sh
    docker-compose rm -y
    ```

3. Delete Volume `postgres_data`

    ```sh
    docker volume rm postgres_data
    ```

4. Rerun `docker-compose up`

### Delete staging data to start afresh db on init - Opt 2

1. stop psql service

    ```sh
    docker exec -it okr-app-db-1 bash -c "pg_ctl stop -D /var/lib/postgresql/data"
    ```

2. Delete data

    ```sh
    docker exec -it okr-app-db-1 rm -rf /var/lib/postgresql/data
    ```

3. Stop and rerun `docker-compose up`


## Dev Setup to iterate fast

> Iterate fast on UI changes with only restarting UI service

Run `backend` and `db`

### Setup `okr_network_dev` docker network

```sh
docker network create okr_network_dev
```

### DB

```sh
# Run DB on local host and 'okr_network_dev' network
export POSTGRES_USER='postgres'
export POSTGRES_PASSWORD='password'
export POSTGRES_DB='okr_db'
export DB_HOST_PORT=5431  # use this to access db from localhost
export OKR_APP_DEPLOY_MODE='staging'  #  adds toy data in db, if db is empty
docker run -it --rm --network okr_network_dev -e POSTGRES_USER -e POSTGRES_PASSWORD -e POSTGRES_DB -e DB_HOST_PORT -v "./db/init_${OKR_APP_DEPLOY_MODE:-staging}.sql:/docker-entrypoint-initdb.d/init_db.sql" -v "./db/schema.sql:/db/schema.sql" -v "./db/data.sql:/db/data.sql" -p "${DB_HOST_PORT}:5432" --name okr_db_dev postgres:latest
```

> ommiting `-v postgres_data:/var/lib/postgresql/data` to force afresh start every time

### Backend
```sh
docker build -t okr-api-dev -f ./backend/Dockerfile ./backend

# Run Backend on local host and 'okr_network_dev' network
export DATABASE_URL='postgresql://postgres:password@okr_db_dev:5432/okr_db'
export OKR_API_HOST_PORT=8000  # use this to access backend service from localhost
docker run -it --rm --network okr_network_dev -e DATABASE_URL -p "${OKR_API_HOST_PORT}:8000" --name okr_api_dev okr-api-dev
```

### Frontend

```sh
docker build -t okr-ui-dev -f ./frontend/Dockerfile ./frontend


# Run Frontend on local host and 'okr_network_dev' network
export OKR_BACKEND_URL='http://okr_api_dev:8000'
docker run -it --rm --network okr_network_dev -e OKR_BACKEND_URL -v ./frontend/app.py:/app/app.py -v ./frontend/key_results_card.py:/app/key_results_card.py -v ./frontend/key_result_item.py:/app/key_result_item.py -v ./frontend/key_result_item_edit.py:/app/key_result_item_edit.py -v ./frontend/key_result_item_view.py:/app/key_result_item_view.py -v ./frontend/key_result_to_add_to_objective.py:/app/key_result_to_add_to_objective.py -v ./frontend/key_result_item_creation_ui.py:/app/key_result_item_creation_ui.py -v ./frontend/key_result_item_v2.py:/app/key_result_item_v2.py -v ./frontend/knowledge_base.py:/app/knowledge_base.py -p "8501:8501" -w /app --name okr_ui_dev okr-ui-dev
```

### Run SQL Queries against DB

```sh
export OKR_APP_DEPLOY_MODE='staging'
# OR
export OKR_APP_DEPLOY_MODE='prod'
export OKR_DB_CONTAINER="okr_db_{OKR_APP_DEPLOY_MODE:-staging}"
```

---

```sh
docker exec -it ${OKR_DB_CONTAINER} psql -U postgres -d okr_db -c "SELECT progress FROM objectives WHERE id = 1; SELECT progress FROM key_results WHERE id = 1;"
```

```sh
docker exec -it ${OKR_DB_CONTAINER} psql -U postgres -d okr_db -c "
SELECT 
    o.id AS objective_id, 
    o.name AS objective_name, 
    o.progress AS objective_progress, 
    kr.id AS key_result_id, 
    kr.description AS key_result_description, 
    kr.progress AS key_result_progress 
FROM objectives o 
LEFT JOIN key_results kr ON o.id = kr.objective_id 
ORDER BY o.id, kr.id;
"
```

#### View all Tables

```sh
docker exec -it ${OKR_DB_CONTAINER} psql -U postgres -d okr_db -c "
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE';
"
```

#### View Columns and their types of 'objectives' table

```sh
docker exec -it ${OKR_DB_CONTAINER} psql -U postgres -d okr_db -c "
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'objectives';
"
```
