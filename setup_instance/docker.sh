# ------------------------------------------
# # clone a repo that you want to build a docker image for:
# ssh-keygen
# git clone git@github.com:nesaboz/whisper.git
# 
#  -----------------------------------------
# # build a docker image
# docker_image="ai-therapist-from-ec2"
# docker build -t $docker_image .

# # test it:
# docker run -it -p 8501:8501 $docker_image


sudo usermod -aG docker $USER

docker inspect --format='{{.Architecture}}' ai_therapist


docker ps
docker ps -a
docker images

my_image=ai_therapist
my_container=ai_therapist

docker build -t $my_image . --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# absolutely critical to pass on a port from container to the host
docker run -d --name $my_container --rm -p 8501:8501 $my_image
docker exec -it $my_container /bin/bash

docker run -d --name $my_container --device=/dev/snd --rm -p 8501:8501 $my_image

docker run -d --name $my_container --rm -p 8501:8501  -v /run/user/$(id -u)/pulse:/run/pulse:ro -e PULSE_SERVER=unix:/run/pulse/native $my_image


docker logs $my_container
docker rm $my_container
docker rmi $my_image


# aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 504308483447.dkr.ecr.us-west-1.amazonaws.com

# docker tag $docker_image:latest 504308483447.dkr.ecr.us-west-1.amazonaws.com/$docker_image:latest
# docker push 504308483447.dkr.ecr.us-west-1.amazonaws.com/$docker_image:latest
