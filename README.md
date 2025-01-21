# Dashboard

1. virtual environment
   ```bash
   python3 venv .venv

   source .venv/bin/activate

   pip install -r requirements.txt
   ```

1. configure database
   - get data YAML files from OERR API for referencing, setup
   - add configurations in config for  'application.config.yml'
   - run migration
    ```bash
      python -m flask db init

      python -m flask db migrate

      python -m flask db upgrade
    ```
    - seed the data
    ```bash
      python -m seeds.run_seeder
    ```
1.     