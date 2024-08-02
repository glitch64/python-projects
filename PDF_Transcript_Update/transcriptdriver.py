import os
import sys
import pyodbc
import subprocess
import logging
from datetime import datetime

def get_student_info(student_number, conn):
    query = f"""
select 
sy.systudentid,
sy.stunum,
sy.lastname,
sy.firstname,
isnull(convert(varchar,sy.dob,101),'01/01/1900') dob,
   
case 
	when trim(sy.ssn) = '' then '000-00-0000' 
	when sy.ssn = '   -  -' then '0000-00-0000'
	else isnull(sy.ssn,'000-00-0000') 
end as ssn,
t.* from transcript_full_list t
left join campusvue.dbo.systudent sy on convert(int,replace(t.filename,'.pdf','')) = sy.systudentid 
  
    WHERE sy.systudentid = {student_number}  and 
    t.filename not in(select * from donelist)
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        dob, ssn = result.dob, result.ssn
        # Ensure that None values are replaced with empty strings
        dob = dob if dob else ""
        ssn = ssn if ssn else ""
        return dob, ssn
    return "", ""
 
def process_pdfs(directory_path, output_path, conn):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".pdf"):
            student_number = os.path.splitext(file_name)[0]
 
            dob, ssn = get_student_info(student_number, conn)
            if dob and ssn:
                input_pdf_path = os.path.join(directory_path, file_name)
                output_pdf_path = os.path.join(output_path, file_name)
                # Run updatepdf.py
                subprocess.run(['python', 'updatepdf.py', input_pdf_path, output_pdf_path, ssn, dob])
            else:
                logging.info(f"Student info not found for {file_name}")
                 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: process_pdfs.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    output_path = "W:\\amackey\\transcripts2"

    # Setup logging
    log_filename = f"log{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

    logging.info("Processing started")

    # Database connection
    conn_str = "DSN=bsc_staging;UID=sa2;PWD=reporter"
    conn = pyodbc.connect(conn_str)

    process_pdfs(directory_path, output_path, conn)

    conn.close()
    logging.info("Processing completed")
    print(f"Processing completed. Log file created: {log_filename}")

