# usage: > source stop.sh

echo shutting down container: $(sudo docker stop $DB_DOCKER_ID)
unset DB_DOCKER_ID