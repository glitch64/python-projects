# Excel Loader

## Description
`excelload.py` is a Python script designed to load data from Excel files into a staging database. It supports both SQL Server and MySQL through ODBC connections.

## Features
- Automatically creates database tables based on Excel worksheet names and columns.
- Inserts data from Excel worksheets into the corresponding database tables.
- Processes multiple Excel files from a specified input directory.
- Moves processed files to a history directory.

## Requirements
- Python 3.x
- `openpyxl`
- `pyodbc`

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/python-projects.git
    cd python-projects/excel-loader
    ```

2. Install the required packages:
    ```bash
    pip install openpyxl pyodbc
    ```

## Usage
1. Place the Excel files to be processed in the `Input` directory.
2. Run the script:
    ```bash
    python excelload.py
    ```

3. Follow the prompts to enter the DSN, sqlserver username, and password for the database connection.


 - ExcelLoader
   |- history
   |- input
   excelload.py
