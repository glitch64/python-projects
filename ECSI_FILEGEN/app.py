from flask import Flask, request, render_template, send_file, Response
import pyodbc
from utils import generate_users_file, generate_stipend_file, generate_tuition_stipend_file

app = Flask(__name__)

# create an odbc connection on your server: <your dbserver>
def get_db_connection():
    connection = pyodbc.connect("DSN=<your dbserver>;UID=<your sql userid>;PWD=<your sql user password")
    return connection

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''select   
        trim(code) + ' : ' + trim(descrip) + ' : ' +  convert(varchar, adt.startdate, 101) as label, adt.adtermid  
        from campusnexus.dbo.adterm adt  
        where startdate >= '1/1/2022' and startdate <= '12/31/2024' 
        and adtermid in (select parentadtermid from campusnexus.dbo.adtermrelationship) 
        order by startdate''')
    terms = cursor.fetchall()

    cursor.execute('''select  
        convert(varchar,date,101) as [date], 
        count(z.satransid) as count, 
        sum(z.amount) * -1 as amount 
        from campusnexus.dbo.zzzzz_satransview3 z 
        where z.source = 'R' 
        and z.descrip like '%Stipend%' 
        and z.descrip not like '%void%' 
        and z.date >= dateadd(day, -1095, convert(date, getdate()))  
        group by convert(varchar,date,101)   
        order by convert(Date,convert(varchar,date,101)) desc ''')
    transaction_dates_stipend = cursor.fetchall()

    cursor.execute('''select  
        convert(varchar,date,101) as [date], 
        count(z.satransid) as count, 
        sum(z.amount) as amount 
        from campusnexus.dbo.zzzzz_satransview3 z 
        where z.sabillcode = 'TUISTIP' 
        and z.date >= dateadd(day, -1095, convert(date, getdate()))  
        group by convert(varchar,date,101)   
        order by convert(Date,convert(varchar,date,101)) desc ''')
    transaction_dates_tuition_stipend = cursor.fetchall()

    conn.close()
    
     # Debug print to check the structure of terms
    #for term in terms:
    #    print(term)
    
    return render_template('index.html', terms=terms, transaction_dates_stipend=transaction_dates_stipend, transaction_dates_tuition_stipend=transaction_dates_tuition_stipend)

@app.route('/generate_users_file', methods=['POST'])
def generate_users_file_route():
    adtermid = request.form.get('adtermid')
    if adtermid:
      print("adtermid:", adtermid)  # Debug print to verify adtermid
    else:
       print("adtermid is blank")
    return generate_users_file(adtermid)

@app.route('/generate_stipend_file', methods=['POST'])
def generate_stipend_file_route():
    transaction_date = request.form.get('transaction_date')
    return generate_stipend_file(transaction_date)

@app.route('/generate_tuition_stipend_file', methods=['POST'])
def generate_tuition_stipend_file_route():
    transaction_date = request.form.get('transaction_date')
    return generate_tuition_stipend_file(transaction_date)

if __name__ == '__main__':
    app.run(debug=True)
