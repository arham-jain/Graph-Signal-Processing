from flask import Flask, render_template, jsonify, request
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
    return render_template('basic/usage.html', data=name)

''''''
class Param_select_form(FlaskForm):
    database = SelectField('Database', choices=[('staging','stageing.db',)])
    kpi = SelectField('KPI', choices=[])
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
    form = Param_select_form()
    form.kpi.choices = exec_query("select distinct `Indicator Code`, `Indicator Name` from staging")

    if request.method == "POST":
        if form.validate_on_submit():
            return '<h1>DB: {}, KPI: {}, YEAR: {}</h1>'.format(form.database.data, form.kpi.data, form.year.data)
    return render_template('basic/param_selection.html', form=form)

'''
Route path = "/dashboard/indicator_code/year"

The below function filters the data using the parameters provided and the exec_query function in the KPI_Automation fil
e. To test the function the dashboard_test.html file is created in the templates/ directory. 

Example = "dashboard/SP.POP.DPND/2000"
'''
@app.route("/dashboard/<string:indicator_code>/<string:year>")
def dashboard(indicator_code,year):
    filename=''.join(c for c in indicator_code if c not in ".")
    select_query(indicator_code, ['Country Name',year], filename+".csv")
    df = pd.read_csv('files/csv/'+filename+'.csv')
    df = df.dropna()
    dict_payload = {
        "name": indicator_code,
        "countries": df['Country Name'].tolist(),
        "kpivalues": df[year].tolist()
    }
    print(dict_payload)
    return render_template("basic/home.html", data=dict_payload)

if __name__=="__main__":
    app.run(debug=True)