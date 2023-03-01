# python-fast-api

### Steps:
- Please see the `requirements.txt` file for the libraries, modules or packages used to built this project.
- Before running the app, please create the Database first.
- Create a Database name `Log` 
- Once the Database is setup, from the root directory of this repository `/python-fast-api` open terminal and run the following script to start creating the table.
  ```
   python create_db.py
  ```
- To populate the logs Table, use the `logs_backup` file and import it to the Logs Table as csv.
- do change the value in the `database.py` with your current local setup
  ```
    postgresql://{username}:{password}@localhost/Log
  ```

### Database
- postgreSQL 15





