from flask import Flask, render_template, jsonify, request, redirect, url_for
from KPI_Automation import select_query, exec_query
import pandas as pd
import json
import glob
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, IntegerField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

'''
Route pate = "/" "/home"

Displays Usage Instruction of the Dashboard
'''
@app.route('/')
@app.route('/dashboard')
@app.route('/dashboard/<string:name>')
def usage_instructions(name="Guest"):
    df = pd.read_csv('files/csv/instructions.csv')
    usage_payload = {
        'name': name,
        'instructions': df['Instructions'].tolist()
    }
    return render_template('basic/usage.html', data=usage_payload)

''''''
class Param_kpi_select_form(FlaskForm):
    database = SelectField('Database', choices=[('staging','stageing.db',)])
    kpi = SelectField('KPI', choices=[])
    year = IntegerField('Year',[
        validators.DataRequired(),
        validators.NumberRange(min=1950,max=2008)
    ])
class Param_conn_select_form(FlaskForm):
    database = SelectField('Database', choices=[('staging','stageing.db',)])
    conn = SelectField('Connectivity Parameter', choices=[])
    year = IntegerField('Year',[
        validators.DataRequired(),
        validators.NumberRange(min=1950,max=2008)
    ])


'''
Route path = "/dashboard/param_selection"

The below function lets the user select parameters like database, based on which KPI can be selected, and graph connectivity data. (Which already exist)
'''
@app.route('/dashboard/param_selection', methods=['GET','POST'])
def param_selection():
    #db_names = []
    #for file in glob.glob("database/*.db"):
    #    db_names.append(file)
    form_kpi = Param_kpi_select_form()
    form_conn = Param_conn_select_form()
    form_kpi.kpi.choices = exec_query("select distinct `Indicator Code`, `Indicator Name` from staging order by `Indicator Name` ASC")
    form_conn.conn.choices = exec_query("select distinct `Indicator Code`, `Indicator Name` from staging order by `Indicator Name` DESC")
    if form_kpi.validate_on_submit():
        return redirect('/dashboard/{}/{}'.format(form_kpi.kpi.data, form_kpi.year.data))
    if form_conn.validate_on_submit():
        return redirect('/dashboard/{}/{}'.format(form_conn.conn.data, form_conn.year.data))
    return render_template('basic/param_selection.html', form_kpi=form_kpi, form_conn=form_conn)

'''
Route path = "/dashboard/indicator_code/year"

The below function filters the data using the parameters provided and the exec_query function in the KPI_Automation fil
e. To test the function the dashboard_test.html file is created in the templates/ directory. 

Example = "dashboard/SP.POP.DPND/2000"
'''
@app.route("/dashboard/<string:indicator_code>/<string:year>")
def kpi_eda(indicator_code,year):
    filename=''.join(c for c in indicator_code if c not in ".")
    select_query(indicator_code, ['Country Name',year], filename+".csv")
    df = pd.read_csv('files/csv/'+filename+'.csv')
    df = df.dropna()
    dict_payload = {
        "kpi_name": indicator_code,
        "kpi_year": year,
        "coun_kpi": zip(df['Country Name'].tolist(),df[year].tolist())
    }
    print(dict_payload)
    return render_template("basic/kpi_eda.html", data=dict_payload)

if __name__=="__main__":
    app.run(debug=True)