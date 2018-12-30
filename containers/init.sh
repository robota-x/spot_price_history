# usage: > source init.sh

# ensure psql folder
mkdir -p data/psql

# run psql server
export DB_DOCKER_ID=$(sudo docker run --rm --name postgres-server -d -v $(pwd)/data/psql:/var/lib/postgresql/data postgres:alpine)
echo started container $DB_DOCKER_ID

# run data fetcher
sudo docker run --rm --network spot_monitor --name spot-runner -e ENV=dev -v ~/.aws:/.aws  spot_runner:v1

# admin version with published port to localhost
# sudo docker run --rm --network spot_monitor --name psql-server -d -p 15432:5432 -v $(pwd)/data/psql:/var/lib/postgresql/data postgres:alpine 
