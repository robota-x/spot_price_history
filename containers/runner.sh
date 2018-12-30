# usage: > sudo bash runner.sh

# ensure psql folder
mkdir -p data/psql

# run psql server and fetch data
echo starting psql server container and fetching data!

docker run --rm --network spot_monitor --name psql-server -d -v $(pwd)/data/psql:/var/lib/postgresql/data postgres:alpine
docker run --rm --network spot_monitor --name spot-runner -e ENV=dev -v ~/.aws:/.aws  spot_runner:dev

# cleanup
echo completed fetch, shutting down!
docker stop psql-server

# admin version with published port to localhost
# docker run --rm --network spot_monitor --name psql-server -d -p 15432:5432 -v $(pwd)/data/psql:/var/lib/postgresql/data postgres:alpine 
