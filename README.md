# Collecting the text from bills introduced in state legislatures

## Launch the development environment
First, download, install, and launch the [Docker Desktop Client](https://www.docker.com/products/docker-desktop/) on your computer.

Next, make sure you have cloned this repository, and use the `cd` command to navigate to this folder on your computer. Update the repository by typing
```
git pull origin main
```

The databases will require some passwords. Open your .env file and add the following lines:
```
MONGO_INITDB_ROOT_USERNAME=mongo 
MONGO_INITDB_ROOT_PASSWORD=redlobstercheddarbiscuit
POSTGRES_PASSWORD=outbackbloominonion
```
Leave the `MONGO_INITDB_ROOT_USERNAME` as "mongo", but change the passwords on the next two lines to whatever you want (just please don't use the @ symbol).

Then to launch the development environments, type
```
docker compose up
```
(If you see an error that says port 8888 is in use, shut down any local instances of Jupyter Lab by pushing Control + C in the terminal window you used to launch Jupyter Lab.)

You will see output start to display in your terminal window. Within the output, you will see text such as

```
Or copy and paste one of these URLs:
pipeline-github-jupyterlab-1  |         http://ea59a8fbdbac:8888/lab?token=205a9abc0c59b11e2ba7d21c35703dd1013b5f42617f1646
pipeline-github-jupyterlab-1  |         http://127.0.0.1:8888/lab?token=205a9abc0c59b11e2ba7d21c35703dd1013b5f42617f1646

```	
Copy the URL that begins http://127.0.0.1:8888/ and paste it into a web browser to launch JupyterLab with all associated packages and databases connected.
