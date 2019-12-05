docker build -t bob .
docker kill bob
docker rm bob
docker run --name bob bob