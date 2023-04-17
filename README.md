# fastapi-wb-parse
#### Simple WB parser with dockercomposed fastapi+sqlalchemy+postgres

#### Settings
You may want to specify your own .env settings. Basic one are already included in .env file
```sh
DB_ENGINE # If you don't specify engine sqlite will be used and rest of the database related settings ignored.
DB_HOST # Host where db is running. Defaults to docker-compose service name
DB_NAME # Name of your database
DB_PORT # Database port
POSTGRES_USER # Database user
POSTGRES_PASSWORD # Database password
```
If installing full compose orchestra just simply run
```sh
sudo docker-compose up -d
```
It is possible to just separately build api but you need to provide .env to container.

#### Usage
There is 4 basic endpoints (PATH METHOD - DESCRIPTION):
```sh
/wares/ GET - list all products in db
/wares/ POST - add new product with body like {"nm_id": "12345"}. Value must be a string
/wares/{nm_id}/ GET - retrieve product with given {nm_id} parameter
/wares/{nm_id}/ DELETE - delete product with given {nm_id} from db
```
### Author: Rosh_penin
### About: Pet project. Very basic WB parser that can store information about products.
