from flask import Flask, render_template, request, jsonify, flash
from pythermalcomfort.models import pmv_ppd, a_pmv, body_surface_area, set_tmp

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/', methods=['GET', 'POST'])
def index():
    ct = float(request.form['ct'])
    cs = float(request.form['cs'])
    pt = float(request.form['pt'])
    ps = float(request.form['ps'])
    pd = float(request.form['pd'])
    if cs>0 and ct>0:
        f_c=cs/1.83
        proxycond=cs*0.3*((ct-tdb)/(60-tdb))
    else:
        f_c=0
        proxycond=0
    if pd>0 and pt>0 and ps>0:
        f_r=ps/((4*3.1415)*(pd**2))
        proxyrad=ps*0.8*((pt-tdb)/(90-tdb))
    else:
        f_r=0
        proxyrad=0
    
    tdb = float(request.form['tdb'])
    tr = float(request.form['tr'])
    vr = float(request.form['vr'])
    v=vr
    rh = float(request.form['rh'])
    met = float(request.form['met'])
    clo = float(request.form['clo'])
    wme = 0
    a_coefficient = float(request.form['a_coefficient'])
    body_surface_area = float(request.form['body_surface_area'])

    shtdb=(f_c*ct)+((1-f_c)*tdb)
    
    shtr=(f_r*pt)+((1-f_r)*tr)

    centralheating=-0.07*(22-ta)
    proximityconso=proxycond + proxyrad

    pmv_value=pmv_ppd(tdb, tr, vr, rh, met, clo,wme)
    apmv_value=a_pmv(tdb, tr, vr, rh, met, clo, a_coefficient, wme)
    sh_pmv=pmv_ppd(shtdb, shtr, vr, rh, met, clo,wme)
    set_value=set_tmp(tdb, tr, v, rh, met, clo, wme=0, body_surface_area=body_surface_area, p_atm=101325, body_position='standing', units='SI', limit_inputs=True)
    return render_template('index.html',centralheating=centralheating, proximityconso=proximityconso, sh_pmv=sh_pmv, set_value=set_value, pmv_value=pmv_value, apmv_value=apmv_value, tdb=tdb, tr=tr, vr=vr, rh=rh, met=met,clo=clo, a_coefficient=a_coefficient, body_surface_area=body_surface_area, ct=ct, cs=cs, pt=pt, ps=ps, pd=pd )

if __name__ == '__main__':
    app.run(debug=True)