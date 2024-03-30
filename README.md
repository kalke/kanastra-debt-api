# Made by Henrique Kalke for Kanastra Software Engineer Test

## Disclaimer

This README is to run as debug, to get all the services running together as asked please follow the instructions avaiable on the [kanastra-compose](https://github.com/kalke/kanastra-compose) repository

### Prerequisites

Before proceeding, ensure you have the following installed on your system:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [MySQL](https://dev.mysql.com/downloads/installer/)

### Step 1: Clone the Project

Please clone this project on ~/Projects

```bash
mkdir ~/Projects
```

Navigate to the folder:

```bash
cd ~/Projects
```

Clone the repository:

```bash
git clone https://github.com/kalke/kanastra-debt-api.git
```

### Step 2: Download Python

To setup Python, we will download and install Anaconda, Anaconda is a Python distribution to simplify the package management, to install, just follow the steps:

```bash
cd ~/Downloads
```

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
```

```bash
sh Anaconda3-2024.02-1-Linux-x86_64.sh
```

Then follow the installation steps or just press `q` to go to the end of the installation process.

After the end of the instalation please restart your terminal

### Step 3: Create the environment

Once you installed Anaconda, you can open other terminal and create a new Python environment to the api project with:

```bash
conda create -n kanastra-debt-api python=3.11
```

Wait to the environment to be created and activate it:

```bash
conda activate kanastra-debt-api
```

Navigate to the project folder with:

```bash
cd ~/Projects/kanastra-debt-api
```

And install the requirements:

```bash
pip install -r requirements.txt
```

### Step 4: Setup the database

Ensure that you have an mysql running on localhost:3306

```sql
CREATE DATABASE kanastra;
```

After creating the kanastra database you can run to setup all the schemas the project needs:

```bash
alembic upgrade head
```

### Step 5: Run the api

If you follow all the steps correctly you can run the api with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The documentation is avaiable in:

```bash
xdg-open http://localhost:8000/docs# > /dev/null
```
