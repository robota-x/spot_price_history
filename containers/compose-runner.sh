# usage: > sudo bash compose-runner.sh dev

# set up env vars for compose interpolation
export PSQL_MOUNT=$(pwd)
export ENV=${1:-live}

if [ $ENV = 'live' ]; 
    then export RUNNER_TAG=v1; 
    else export RUNNER_TAG=dev; 
fi

docker-compose run runner