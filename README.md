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

## Steps to run bill scraper for one session on Rivanna

1. If off-grounds, use Cisco Secure Client and log on to a VPN. UVA Anywhere will suffice.

2. On the command line, log on to Rivanna by typing `ssh -Y mst3k@login.hpc.virginia.edu` and entering UVA password, replacing `mst3k` with your UVA compute ID

3. Type `pwd`, confirm that the directory is `/home/mst3k`, replacing `mst3k` with your UVA compute ID

4. (You only need to do this step the first time you set up this system) Type `git clone https://github.com/jkropko/legiscan_api`. Follow any additional instructions from GitHub
      
5. Type `cd legiscan_api` then `git pull origin main`

6. Activate Conda, which enables us to use the most recent version of Python: `module load miniforge/24.3.0-py3.11` (Eventually this command will become outdated, but you can type `module spider miniforge` to see the latest version of the command)

7. (You only need to do this step the first time you set up this system) Create the Python environment by typing

    * `conda create -n legiscan_end python=3.12.5`
    * `pip install -r requrements.txt`

8. Activate the conda environment: `conda activate legiscan_env`

9. (You only need to do this step the first time you set up the system) Create an .env file for the legiscan key:

    * Type `touch .env` (this creates the empty text file named .env)
    * Type `vim .env` (this opens the text editor to make changes on .env)
    * Type `i` (this allows for new text to be typed in the file)
    * Type in the file `legiscan_key=123456789` where 123456789 is your API key from legiscan
    * Press ESC
    * Press Shift and the ; key together
    * Type `wq` and press return (this saves the changes and quits the text editor)
    * On the original command line type `cat .env` and confirm that your API key appears

10. Choose one session number from the ones listed in concluded_session_ids.csv (say 1254) and type: `python get_session_bills.py 1254`. The code will display each of the bill IDs on the screen, and create a file (such as "bills_AL_2017_regular_session.json") in the Data folder. 



