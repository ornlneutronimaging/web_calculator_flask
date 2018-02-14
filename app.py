from model import InputForm
from flask import Flask, render_template, request
from compute import init_reso, add_layer

import io
import matplotlib.pyplot as plt
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


# try:
#     template_name = sys.argv[1]
# except IndexError:
#     template_name = 'view_plain'
#
# if template_name == 'view_flask_bootstrap':
#     from flask_bootstrap import Bootstrap
#
#     Bootstrap(app)


# @app.route('/template', methods=['GET', 'POST'])
# def template():
#     form = InputForm(request.form)
#     if request.method == 'POST' and form.validate():
#         result = compute(form.A.data, form.b.data,
#                          form.w.data, form.T.data)
#     else:
#         result = None
#
#     return render_template('view.html', form=form, result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    # sample_form = SampleForm(request.form)
    if request.method == 'POST' and form.validate():
        o_reso = init_reso(form.e_min.data,
                           form.e_max.data,
                           form.e_step.data)
        o_reso.add_layer(form.formula.data,
                         form.thickness.data,
                         form.density.data)
        # if init_form.validate() and sample_form.validate():
        #     o_reso = init_reso(init_form.e_min.data,
        #                        init_form.e_max.data,
        #                        init_form.e_step)
        #     result = add_layer(o_reso,
        #                        sample_form.formula.data,
        #                        sample_form.thickness.data,
        #                        sample_form.density.data)
        result = o_reso.stack
        plot = o_reso.plot()
    else:
        result = None
        plot = None

    return render_template('view.html', form=form, result=result, plot=plot)


@app.route('/plot')
def build_plot():
    img = io.BytesIO()

    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


@app.route('/main')
def main():
    return render_template('index.html')


@app.route("/hello")
def hello():
    return render_template('hello.html')


@app.route("/sample")
def sample():
    return render_template('sample.html')


@app.route("/members")
def members():
    return "Members"


@app.route("/members/<string:name>/")
def getMember(name):
    return name


if __name__ == '__main__':
    app.run(debug=True)
