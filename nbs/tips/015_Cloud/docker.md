# Docker

A docker contain is a great way to set up an environment. Once the docker container is built and running, one can attach to it from VSCode and use it as a remote machine. To do this, install "Remote Development" extension [pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack), then one can attach the container in VSCode by going to a command pallette (Cmd+Shift+P) and typing "Attach to running container". If typing `sudo` all the time is annoying add user to the docker group:

```zsh
sudo usermod -aG docker $USER
```
and (maybe, not always) restart the machine.

## Build a Docker image 

One needs Dockerfile and requirements.txt. See Dockerfile for details on steps.

We'll use `docker build -t <some_image_name> .` to build docker image from files in the current folder (indicated by the `.` at the end)
```zsh
sudo docker build -t my_project:1.0 .  
```

Very common command:
```zsh
sudo docker images  # to see existing images
```

## Running a container

After building an Image we now run a container (one can run many containers from the same image). 

Important flags: 
| flag | action |
|----------|----------|
| `-it`/`-d` | runs container in interactive\detached mode |  
| `-rm` | removes docker after it's done the task |  
| `-p X:Y` | maps port X on docker container to port Y on local machine |

Very common commands:
```zsh
sudo docker run <image name>  # to run a container 
sudo docker ps      # to see running containers
sudo docker container stop <container name>  # to stop specific container
sudo docker container stop $(sudo docker container ls -aq)  # to stop all containers
```

### Detached mode
To run container in detached mode requires defining entry point in the Dockerfile (typically last command there see `CMD` or `ENTRYPOINT`):
```zsh
sudo docker run -d -p 8501:8501 my_project:1.0
```
Now simply go to `localhost:8501` in your browser and you should see the app.

To connect to the terminal of a running container (find container name using `sudo docker ps`): 
```zsh
sudo docker exec -it <container_name> bash
```

### Interactive mode

Run container and then run the some commnad (here for example Streamlit app)
: 
```zsh
sudo docker run -p 8501:8501 -it my_project:1.0 bash    # bash here is what will run 
streamlit run entry_file.py --server.port 8501
```

To exit from a container's bash use:
```zsh
exit
```
If you had flag `-rm` this exit would kill the container.
Without the flag the container would still be running (see with `sudo docker ps`).

# App deployment

When deploying Docker to a remote machine, to set up ports, env variables, memory to reserve etc, one uses `docker-compose.yaml`.