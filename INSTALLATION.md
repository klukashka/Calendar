# Installation

1. Make sure all the required dependencies are
   installed:
    * [git](https://github.com/git-guides/install-git)
    * [Docker](https://docs.docker.com/engine/install/)
    * [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
    * Any database compatible with SQLAlchemy
2. Clone the repository: `git clone https://github.com/klukashka/Calendar.git`
3. Create `.env` file from `.env.example` and provide your credentials
4. Create `alembic.ini` from `alembic.ini.example` and provide your DB_URL
5. Execute with `docker compose up --build`