### Prerequisites

- Python 3.x
- Flask
- pyodbc
 

## Setup

1. **Install required Python packages:**
    ```bash
    pip install flask pyodbc
    ```

2. **Create ODBC DSN on the server running the application**

    - Note: My ODBC DSN was named `nsad` that points to our SQL Server with our CAMPUSNEXUS database.

## Configuration

Update the `get_db_connection` function in `utils.py` with the correct DSN, username, and password for your database:

```python
def get_db_connection():
    connection = pyodbc.connect("DSN=<ODBC DSN name>;UID=<sql user ID>;PWD=<sql password>")
    return connection```
	
## Running the Application
Run the Flask application:

```python app.py```
## Access the application:

```Open a web browser and go to http://127.0.0.1:5000.```

##Usage

Generate Users File
1.  Select an academic term from the dropdown menu.
2.  Click the "Generate Users File" button.
3.  The generated users file will be downloaded as ecsi_users_file.txt.

Generate Stipend File
1.  Select a transaction date from the dropdown menu.
2.  Click the "Generate Stipend File" button.
3.  The generated stipend file will be downloaded as ecsi_stipend_file.txt.

Generate Tuition Stipend File
1.  Select a transaction date from the dropdown menu.
2.  Click the "Generate Tuition Stipend File" button.
3.  The generated tuition stipend file will be downloaded as ecsi_tuition_stipend_file.txt.

makeservice.py = Python script to make the python program a windows service.

Using IIS server with reverse-proxy rule to url:port of application.

Acknowledgements
Built with Flask - a lightweight WSGI web application framework in Python.
 
 