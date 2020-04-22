from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def ccr_calculator():
    return render_template('ccrCalculator.html')


@app.route("/calculate_ccr", methods=['GET', 'POST'])
def ccr_result():

    quantity1 = float(request.form['qty1'])
    quantity2 = float(request.form['qty2'])
    quantity3 = float(request.form['qty3'])

    try:
        lamp_inputs = [quantity1, quantity2, quantity3]
        if lamp_inputs == [0, 0, 0]:
            return "<h1>Error! You must enter at least one set of lamp quantities.</h1>"
        else:
            result = ccr_calc()
            return render_template('ccrResult.html', result=result)
    except:
        return "<h1>Error! Please check all inputs have been entered.</h1>"


def ccr_calc():
    rho_cu = 1.72e-8
    rho_al = 2.65e-8
    efficiency = 0.85
    powerFactor = 0.97

    lamp1 = float(request.form['lr1'])
    lamp2 = float(request.form['lr2'])
    lamp3 = float(request.form['lr3'])

    quantity1 = float(request.form['qty1'])
    quantity2 = float(request.form['qty2'])
    quantity3 = float(request.form['qty3'])

    lp = float(request.form['tplBox'])
    ls = float(request.form['tslBox'])

    i = float(request.form['currentDrop'])

    cable = request.form['cableDrop']
    if cable == 'Copper':
        rho = rho_cu
    else:
        rho = rho_al

    csa1 = float(request.form['primarySizeDrop'])
    csa2 = float(request.form['secondarySizeDrop'])

    R1 = rho * (1 / (csa2 / 1000000))  # Resistance per metre secondary
    R2 = rho * (1 / (csa1 / 1000000))  # Resistance per metre primary
    secondaryLossesPerM = np.power(i, 2) * R1  # Secondary losses per metre
    secondaryLosses = secondaryLossesPerM * ls
    primaryLosses = np.power(i, 2) * R2 * lp

    lampPlusSecondaryLoad = (1.1 * ((lamp1 * quantity1 + lamp2 * quantity2 + lamp3 * quantity3) + secondaryLosses)
                             / efficiency * powerFactor)  # Added 10 % for transformer losses

    ccrLoad = 1.05 * (lampPlusSecondaryLoad + primaryLosses)  # 5 % added for lamp and regulator losses
    ccrLoad = np.round(ccrLoad * 100.0) / 100.0

    voltage = (1.05 * (lampPlusSecondaryLoad + primaryLosses)) / i
    voltage = np.round(voltage * 100.0) / 100.0

    ccrSize = " "
    utilisation = " "

    if ccrLoad <= 0.9 * 2500:
        ccrSize = 2.5
        util(ccrLoad, ccrSize)

    elif 0.9 * 2500 <= ccrLoad <= 0.9 * 4000:
        ccrSize = 4
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 4000 < ccrLoad <= 0.9 * 7500:
        ccrSize = 7.5
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 7500 < ccrLoad <= 0.9 * 10000:
        ccrSize = int(10)
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 10000 < ccrLoad <= 0.9 * 15000:
        ccrSize = int(15)
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 15000 < ccrLoad <= 0.9 * 20000:
        ccrSize = int(20)
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 20000 < ccrLoad <= 0.9 * 25000:
        ccrSize = int(25)
        utilisation = util(ccrLoad, ccrSize)

    elif 0.9 * 25000 < ccrLoad <= 0.9 * 30000:
        ccrSize = int(30)
        utilisation = util(ccrLoad, ccrSize)

    elif ccrLoad > 0.9 * 30000:
        ccrLoad = "Error!"
        voltage = "Error!"
        ccrSize = "Error!"
        utilisation = "Error!"

    ans = [ccrLoad, voltage, ccrSize, utilisation]

    return ans


def util(ccrLoad, ccrSize):
    utilisation = 100 * (ccrLoad / 1000) / ccrSize
    utilisation = np.round(utilisation * 100.0) / 100.0
    return utilisation


if __name__ == "__main__":
    app.run(debug=True)
