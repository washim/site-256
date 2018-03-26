from flask import Flask,request,render_template,url_for,flash,redirect
from models import *
from wtf import *
import tradelight as market
import sqlite3, os
import pandas as pd

app = Flask(__name__)

app.config.from_object("config.%sConfig" % os.environ.get("FLASK_ENV", "Dev"))

@app.route("/")
def index():
    res = []
    data = tblsymbols.query.all()
    for item in data:
        research = market.tradelight()
        research.getCandles(item.symbols,item.interval,item.startdt,item.enddt)
        mydata = research.getChart(item.capital,item.quantity,item.sma,item.lma)
        res.append(mydata)
    return render_template("index.html",graphs=res)

@app.route("/dumphistoricaldata", methods=["GET","POST"])
def dumphistoricaldata():
    form = MangeHistoricalData()
    if form.validate_on_submit():
        research = market.tradelight()
        if request.form['dump'] == "yes":
            research.dumpInstrumentHistoricalData(request.form['interval'],request.form['startdt'],request.form['enddt'])
        research.symbolsGetReturns(int(request.form['capital']),int(request.form['quantity']),
                                   int(request.form['sma']),int(request.form['lma']))
        flash("Historical data dumped successfully.","success")
        return redirect(url_for("getreturn"))
    return render_template('dumphistoricaldata.html', form=form)

@app.route("/deletesymbol/<symbol>", methods=["GET"])
def deletesymbol(symbol):
    me = tblsymbols.query.filter_by(symbols=symbol).first()
    db.session.delete(me)
    db.session.commit()
    flash("Symbol deleted successfully.","success")
    return redirect(url_for("index"))

@app.route("/getreturn", methods=["GET"])
def getreturn():
    df = pd.read_csv(os.path.join(app.root_path, 'static\\resources\\data', 'stockreturn.csv'))
    return render_template("getreturn.html", data=df.to_html())

@app.route("/managesymbol", methods=["GET", "POST"])
@app.route("/managesymbol/<symbol>", methods=["GET", "POST"])
def managesymbol(symbol=None):
    me = None
    if symbol:
        me = tblsymbols.query.filter_by(symbols=symbol).first()
    form = MangeSymbol()
    if form.validate_on_submit():
        if me is not None:
            me.capital = request.form['capital']
            me.quantity = request.form['quantity']
            me.sma = request.form['sma']
            me.lma = request.form['lma']
            me.interval = request.form['interval']
            me.startdt = request.form['startdt']
            me.enddt = request.form['enddt']
            db.session.commit()
            flash("Symbol updated successfully.","success")
        else:
            me = tblsymbols(request.form['symbols'],request.form['capital'],request.form['quantity'],request.form['sma'],
                         request.form['lma'],request.form['interval'],request.form['startdt'],request.form['enddt'])
            db.session.add(me)
            db.session.commit()
            flash("Symbol added successfully.","success")
        return redirect(url_for("index"))
    return render_template('managesymbol.html', form=form, data=me)

if __name__ == "__main__":
    db.init_app(app)
    app.run()