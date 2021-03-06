from flask import Flask, render_template, jsonify, request, redirect, url_for
from KPI_Automation import select_query, exec_query
import pandas as pd
from forms import Param_conn_select_form, Param_kpi_select_form
from config import Config
import matplotlib.pyplot as plt
import numpy as np
from Graph_Automation import GSP

app = Flask(__name__)
app.config.from_object(Config)

data = {
    'kpi':0,
    'conn':0,
}

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
        data['kpi'] = 1
        data['conn'] = 0
        return redirect('/dashboard/{}/{}'.format(form_kpi.kpi.data, form_kpi.year.data))
    if form_conn.validate_on_submit():
        data['kpi'] = 0
        data['conn'] = 1
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
    if data['kpi']==1:
        data['kpi_data'] = zip(df['Country Name'].tolist(),df[year].tolist())

    if data['conn']==1:
        data['conn_data'] = zip(df['Country Name'].tolist(),df[year].tolist())

    ## NEEDS TO CHANGE
    bp = plt.figure()
    boxplot = df.boxplot(column=[year])
    bp.savefig("static/images/eda/boxplot.svg", format="svg")

    df['Country Code'] = np.arange(1,len(df)+1)
    print(df)
    scatterplot = df.plot.scatter(x = 'Country Code',y = year, c = 'DarkBlue')
    sp = scatterplot.get_figure()
    sp.savefig("static/images/eda/scatterplot.svg", format="svg")

    return render_template("basic/kpi_eda.html", data=dict_payload)

'''
Route path = "/dashboard/gspboard"

This endpoint performs GSP based functions on the data submitted to param_selection. The data is accessed from the 
'data' dictionary
'''
@app.route("/dashboard/gspboard")
def dashboard():
    gsp = GSP(data['kpi_data'], data['conn_data'])
    print(gsp.conn_dict)
    print(gsp.kpi_dict)
    gsp.graph_signal()
    gsp.gsp_plots()
    return render_template("basic/gspboard.html")\

'''
Route path = "/dashboard/gspboard/new"

To reload GSP page. Overcomes Caching issue.
'''
@app.route("/dashboard/gspboard/new")
def dashboard_new():
    return render_template("basic/gspboard.html")


if __name__=="__main__":
    app.run(debug=True)