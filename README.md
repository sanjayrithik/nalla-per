docker-compose down -v  
//to stop existing docker image

docker-compose build --no-cache   
//It rebuilds everything from scratch, re-running every step in your Dockerfile

docker-compose up   
//The command that starts your application

OPTIONAL
docker-compose build --no-cache web   
//Rebuilds only the web service from your docker-compose.yml


