from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, IntegerField

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
