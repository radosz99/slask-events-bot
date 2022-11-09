docker stop $(docker ps -q --filter ancestor=slask_bot)
docker rm slask_bot
docker build -t slask_bot .
docker run -d -p 8140:8140 --name slask_bot slask_bot