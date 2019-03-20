from flask import Flask, render_template, jsonify
from KPI_Automation import select_query, exec_query
import pandas as pd
import json

app = Flask(__name__)

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
    return render_template("dashboard_test.html", data=dict_payload)

if __name__=="__main__":
    app.run(debug=True)