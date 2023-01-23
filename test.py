from flask import Flask, render_template, request
from pythermalcomfort.models import pmv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tdb = float(request.form['tdb'])
        tr = float(request.form['tr'])
        vr = float(request.form['vr'])
        rh = float(request.form['rh'])
        met = float(request.form['met'])
        clo = float(request.form['clo'])
        wme = 0
        pmv_value = pmv(tdb, tr, vr, rh, met, clo,wme)
        return render_template('index.html', pmv_value=pmv_value)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)