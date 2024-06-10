import pyodbc
from flask import Response

def get_db_connection():
    connection = pyodbc.connect("DSN=<your dbserver>;UID=<your sql userid>;PWD=<your sql user password")
    return connection
    
def generate_users_file(adtermid):
    conn = get_db_connection()
    cursor = conn.cursor()
    print("adtermid",adtermid)
    
 # Define the header query and parameters
    header_query = '''
    SELECT 
        'ACc7i|' + 
        CONVERT(NVARCHAR(4), ISNULL((SELECT COUNT(sy.systudentid) 
            FROM campusnexus.dbo.systudent sy 
            JOIN campusnexus.dbo.adenroll ade ON sy.systudentid = ade.systudentid 
            JOIN campusnexus.dbo.syschoolstatus sss ON ade.syschoolstatusid = sss.syschoolstatusid 
            JOIN campusnexus.dbo.syschoolstatus sss2 ON sy.syschoolstatusid = sss2.syschoolstatusid 
            JOIN campusnexus.dbo.adprogram adp ON ade.adprogramid = adp.adprogramid 
            JOIN campusnexus.dbo.adenrollterm aet ON ade.adenrollid = aet.adenrollid 
            WHERE aet.adtermid = ? AND ade.syschoolstatusid IN (13, 16, 51, 15, 5, 7) 
            AND ISNULL((aet.termregcredits), 0.00) BETWEEN 0 AND 99), 0)) + '|0|' + 
        CONVERT(NVARCHAR(10), ISNULL((SELECT COUNT(sy.systudentid) 
            FROM campusnexus.dbo.systudent sy 
            JOIN campusnexus.dbo.adenroll ade ON sy.systudentid = ade.systudentid 
            JOIN campusnexus.dbo.syschoolstatus sss ON ade.syschoolstatusid = sss.syschoolstatusid 
            JOIN campusnexus.dbo.syschoolstatus sss2 ON sy.syschoolstatusid = sss2.syschoolstatusid 
            JOIN campusnexus.dbo.adprogram adp ON ade.adprogramid = adp.adprogramid 
            JOIN campusnexus.dbo.adenrollterm aet ON ade.adenrollid = aet.adenrollid 
            WHERE aet.adtermid = ? AND ade.syschoolstatusid IN (13, 16, 51, 15, 5, 7) 
            AND ISNULL((aet.termregcredits), 0.00) BETWEEN 0 AND 99), 0)) + '|0|' AS header
    '''
    header_params = (adtermid, adtermid)
    
    # Print the header query and parameters
    #print("Header Query:", header_query)
    #print("Header Params:", header_params)   
    cursor.execute(header_query, header_params)
    header = cursor.fetchone()[0]
  
   # Define the body query and parameters
    body_query = '''
    SELECT DISTINCT
        TRIM(sy.stunum) + '|' + 
        TRIM(sy.firstname) + '|' + 
        '' + '|' + 
        TRIM(sy.lastname) + '|' + 
        '' + '|' + 
        TRIM(sy.otheremail) + '|' + 
        TRIM(REPLACE(REPLACE(REPLACE(REPLACE(sy.phone, '(', ''), ')', ''), '-', ''), ' ', '')) + '|' + 
        '' + '|' + 
        CONVERT(VARCHAR, sy.dob, 23) + '|' + 
        TRIM(sy.addr1) + '|' + 
        TRIM(ISNULL(sy.addr2, '')) + '|' + 
        TRIM(sy.city) + '|' + 
        TRIM(sy.state) + '|' + 
        '' + '|' + 
        TRIM(sy.zip) AS body
    FROM campusnexus.dbo.systudent sy 
    JOIN campusnexus.dbo.adenroll ade ON sy.systudentid = ade.systudentid 
    JOIN campusnexus.dbo.syschoolstatus sss ON ade.syschoolstatusid = sss.syschoolstatusid 
    JOIN campusnexus.dbo.syschoolstatus sss2 ON sy.syschoolstatusid = sss2.syschoolstatusid 
    JOIN campusnexus.dbo.adprogram adp ON ade.adprogramid = adp.adprogramid 
    JOIN campusnexus.dbo.adenrollterm aet ON ade.adenrollid = aet.adenrollid 
    WHERE aet.adtermid = ? 
    AND ade.syschoolstatusid IN (13, 16, 51, 15, 5, 7) 
    AND ISNULL((aet.termregcredits), 0.00) BETWEEN 0 AND 99
    '''
    body_params = (adtermid,)

  # Print the body query and parameters
    #print("Body Query:", body_query)
    #print("Body Params:", body_params)
    
    cursor.execute(body_query, body_params)
    students = cursor.fetchall()
    conn.close()
    
    def generate():
        yield header + "\n"
        for student in students:
            yield student[0] + "\n"
    
    return Response(generate(), mimetype='text/plain', headers={'Content-Disposition': 'attachment;filename=ecsi_users_file.txt'})
    
def generate_stipend_file(transaction_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''select 
        'ACc7i|' + convert(nvarchar(4), isnull((select count(st.satransid) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.source = 'R' 
        and st.descrip like '%stipend%' 
        and st.descrip not like '%void%' 
        and st.descrip not like '%refund%'), 0)) + '|0|' + 
        convert(nvarchar(10), isnull((select count(st.satransid) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.source = 'R' 
        and st.descrip like '%stipend%' 
        and st.descrip not like '%void%' 
        and st.descrip not like '%refund%'), 0)) + '|' + 
        convert(nvarchar(12), isnull((select sum(-1 * st.amount) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.source = 'R' 
        and st.descrip like '%stipend%' 
        and st.descrip not like '%void%' 
        and st.descrip not like '%refund%'), 0)) + 'USD|' as header, 
        isnull((select sum(-1 * st.amount) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.source = 'R' 
        and st.descrip like '%stipend%' 
        and st.descrip not like '%void%' 
        and st.descrip not like '%refund%'), 0) as totalamount''', transaction_date, transaction_date, transaction_date, transaction_date)
    header = cursor.fetchone()[0]

    cursor.execute(''' select 
        sy.stunum + '|' + 
        trim(sy.firstname) + '|' + 
        '' + '|' + 
        trim(sy.lastname) + '|' + 
        '' + '|' + 
        trim(sy.otheremail) + '|' + 
        trim(replace(replace(replace(replace(sy.phone, '(', ''), ')', ''), '-', ''), ' ', '')) + '|' + 
        '' + '|' + 
        convert(varchar, sy.dob, 23) + '|' + 
        trim(sy.addr1) + '|' + 
        trim(isnull(sy.addr2, '')) + '|' + 
        trim(sy.city) + '|' + 
        trim(sy.state) + '|' + 
        '' + '|' + 
        trim(sy.zip) + '|' + 
        convert(varchar, st.date, 23) + '|' + 
        convert(nvarchar(20), -1 * st.amount) + 'USD' as body 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.source = 'R' 
        and st.descrip like '%stipend%' 
        and st.descrip not like '%void%' 
        and st.descrip not like '%refund%' ''', transaction_date)
    stipends = cursor.fetchall()
    conn.close()
    
    def generate():
        yield header + "\n"
        for stipend in stipends:
            yield stipend[0] + "\n"
    
    return Response(generate(), mimetype='text/plain', headers={'Content-Disposition': 'attachment;filename=ecsi_stipend_file.txt'})

def generate_tuition_stipend_file(transaction_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''select 
        'ACc7i|' + convert(nvarchar(4), isnull((select count(st.satransid) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.sabillcode = 'TUISTIP'), 0)) + '|0|' + 
        convert(nvarchar(10), isnull((select count(st.satransid) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.sabillcode = 'TUISTIP'), 0)) + '|' + 
        convert(nvarchar(12), isnull((select sum(st.amount) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.sabillcode = 'TUISTIP'), 0)) + 'USD|' as header, 
        convert(nvarchar(12), isnull((select sum(st.amount) 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.sabillcode = 'TUISTIP'), 0) * -1) as totalamount''', transaction_date, transaction_date, transaction_date, transaction_date)
    header = cursor.fetchone()[0]

    cursor.execute('''select 
        sy.stunum + '|' + trim(sy.firstname) + '|' + '' + '|' + trim(sy.lastname) + '|' + 
        '' + '|' + trim(sy.otheremail) + '|' + trim(replace(replace(replace(replace(sy.phone, '(', ''), ')', ''), '-', ''), ' ', '')) + '|' + 
        '' + '|' + convert(varchar, sy.dob, 23) + '|' + trim(sy.addr1) + '|' + 
        trim(isnull(sy.addr2, '')) + '|' + trim(sy.city) + '|' + trim(sy.state) + '|' + 
        '' + '|' + trim(sy.zip) + '|' + convert(varchar, st.date, 23) + '|' + 
        convert(nvarchar(20), st.amount) + 'USD' as body 
        from campusnexus.dbo.systudent sy 
        join campusnexus.dbo.satrans st on sy.systudentid = st.systudentid 
        where convert(date, st.date) = ? 
        and st.sabillcode = 'TUISTIP' ''', transaction_date)
    tuition_stipends = cursor.fetchall()
    conn.close()
    
    def generate():
        yield header + "\n"
        for tuition_stipend in tuition_stipends:
            yield tuition_stipend[0] + "\n"
    
    return Response(generate(), mimetype='text/plain', headers={'Content-Disposition': 'attachment;filename=ecsi_tuition_stipend_file.txt'})
