"""imports"""

from flask import Flask, render_template, request
from pythermalcomfort.models import pmv_ppd, set_tmp, pmv
import random
import sys
from xml.etree import ElementTree as ET

import yaml

"""end imports"""

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/', methods=['GET', 'POST'])
def index():
    try: 
        tdb = float(request.form['tdb'])
        tr = float(request.form['tr'])
        vr = float(request.form['vr'])
        v=vr
        rh = float(request.form['rh'])
        met = float(request.form['met'])
        clo = float(request.form['clo'])
        wme = 0
        a_coefficient = float(request.form['a_coefficient'])

        c20= float(request.form['c20'])
        ct = float(request.form['ct'])
        cs = float(request.form['cs'])
        cr = float(request.form['cr'])
        pt = float(request.form['pt'])
        ps = float(request.form['ps'])
        pd = float(request.form['pd'])
    except:
        tdb = 16
        tr = 16
        vr = 0.1
        v=vr
        rh = 50
        met = 1
        clo = 1
        wme = 0
        a_coefficient = 0

        c20= 10000
        ct = 0
        cs = 0
        cr = 0
        pt = 0
        ps = 0
        pd = 0
    if cs>0 and ct>0 and cr>0:
        f_c=(cs*(cr/100))/1.83
        proxycond=cs*0.3*((ct-tdb)/(60-tdb))
    else:
        f_c=0
        proxycond=0
    if pd>0 and pt>0 and ps>0:
        f_r=ps/((4*3.1415)*(pd**2))
        proxyrad=ps*0.95*((pt-tdb)/(90-tdb))
    else:
        f_r=0
        proxyrad=0
    
    shtdb=(f_c*ct)+((1-f_c)*tdb)
    shtr=(f_r*pt)+((1-f_r)*tr)

    centralheating=-7*(20.5-tdb)
    kWhgain= (0.07*(20.5-tdb))*c20
    kWhgain=round(kWhgain,ndigits=None)
    proximityconso=1000*proxycond + 1000*proxyrad
    proximityconso= round(proximityconso,ndigits=None)
    if proximityconso>0:
        hdayproxy=(kWhgain/180)/(proximityconso*3/1000)
        hdayproxy=round(hdayproxy,ndigits=None)
    else:
        hdayproxy="no proximity use @ the moment"

    pmv_value=pmv_ppd(tdb, tr, vr, rh, met, clo,wme)
    pmvpmv=pmv(shtdb, shtr, vr, rh, met, clo,wme)
    color=get_color(pmvpmv)
    sh_pmv=pmv_ppd(shtdb, shtr, vr, rh, met, clo,wme)
    
    set_value=set_tmp(tdb, tr, v, rh, met, clo, wme=0, body_surface_area=1.83, p_atm=101325, body_position='standing', units='SI', limit_inputs=True)
    return render_template('index.html', color=color,kWhgain=kWhgain,hdayproxy=hdayproxy, centralheating=centralheating, proximityconso=proximityconso, sh_pmv=sh_pmv, set_value=set_value, pmv_value=pmv_value, tdb=tdb, tr=tr, vr=vr, rh=rh, met=met,clo=clo, a_coefficient=a_coefficient, ct=ct, cs=cs, cr=cr, pt=pt, ps=ps, pd=pd, c20=c20 )

def get_color(value):
    if value <= -1:
        return "blue"
    elif value >-1 and value <=-0.5:
        return "green"   
    elif value >-0.5 and value <0.5:
        return "#DFFF00"   
    elif value >=0.5 and value <1:
        return "green"
    elif value >=1:
        return "red"
    else:
        return "black"



if __name__ == '__main__':
    app.run(debug=True)
