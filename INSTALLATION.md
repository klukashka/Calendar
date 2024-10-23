# Installation

1. Make sure required dependencies are installed: [Docker](https://docs.docker.com/engine/install/), [git](https://github.com/git-guides/install-git)
2. Clone the repository: `git clone https://github.com/klukashka/Calendar.git`
3. Create `.env` file from `.env.example` and provide your credentials
4. Create `alembic.ini` from `alembic.ini.example` and provide your DB_URL
5. Execute with `docker compose up --build` or `sudo docker compose up --build` 
if you are new to docker and read [this](https://docs.docker.com/engine/install/linux-postinstall/) to 
get rid of `sudo`