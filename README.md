# Dashboard

1. virtual environment
 ```bash
 python3 venv .venv
 source .venv/bin/activate

 pip install -r requirements.txt
 ```

1. configure database
  get data YAML files from OERR API for referencing, setup
  add configurations in config for  'application.config.yml'
  run migration
  ```bash
  python -m flask db init
  python -m flask db migrate
  python -m flask db upgrade
  ```

1. seed initial data data
  ```bash
  python -m seeds.run_seeder
  ```

1. configure dashboard
  reference the data folder for test short names

1. set up a systemd service for the api
  to execute `python -m dashboard_api`

1. set up a systemd service for the dashboard
  to execute `python -m run`