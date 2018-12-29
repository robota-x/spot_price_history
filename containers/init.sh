# usage: > source init.sh

# ensure psql folder
mkdir -p data/psql

# run psql server
export DB_DOCKER_ID=$(sudo docker run --rm --name postgres-server -d -p 15432:5432 -v $(pwd)/data/psql:/var/lib/postgresql/data postgres:alpine)
echo started container $DB_DOCKER_ID