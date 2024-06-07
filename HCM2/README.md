# HCM2 - used by internal web application that takes an uploaded excel file and loads it's data into a staging database table.  

## Description
`hcm2.py` is a Python script designed to load data from Excel files into a staging database. It supports both SQL Server and MySQL through ODBC connections.

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
## C:\<yourpath>\>python hcm2.py
## Screenshots
Directory Structure:<br>
![Directory structure](../z_images/folders2.jpg)



ODBC <br>
![ODBC SQL Server](../z_images/odbcconfig.jpg)

    ```
