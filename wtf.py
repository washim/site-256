from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, SelectField

class MangeSymbol(FlaskForm):
    symbols = StringField('Symbol', validators=[validators.DataRequired()])
    capital = StringField('Capital', validators=[validators.DataRequired()])
    quantity = StringField('Quantity', validators=[validators.DataRequired()])
    sma = StringField('SMA', validators=[validators.DataRequired()])
    lma = StringField('LMA', validators=[validators.DataRequired()])
    interval = SelectField('Interval', choices=[('day', 'Day'), ('minute', 'Minute'),
                                                ('5minute', '5 Minutes'), ('10minute','10 Minutes'), ('15minute','15 Minutes')], default="day")
    startdt = StringField('Start Date', validators=[validators.DataRequired()])
    enddt = StringField('End Date', validators=[validators.DataRequired()])

class MangeHistoricalData(FlaskForm):
    capital = StringField('Capital', validators=[validators.DataRequired()])
    quantity = StringField('Quantity', validators=[validators.DataRequired()])
    sma = StringField('SMA', validators=[validators.DataRequired()])
    lma = StringField('LMA', validators=[validators.DataRequired()])
    interval = SelectField('Interval', choices=[('day', 'Day'), ('minute', 'Minute'),
                                                ('5minute', '5 Minutes'), ('10minute','10 Minutes'), ('15minute','15 Minutes')], default="day")
    startdt = StringField('Start Date', validators=[validators.DataRequired()])
    enddt = StringField('End Date', validators=[validators.DataRequired()])