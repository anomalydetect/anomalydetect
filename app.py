# import necessary libraries
import os
import numpy as np
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from config import config

#sys.path.insert(0, './db')
from db.analysis import fx_analysis, fx_result

#from flask.ext.cors import CORS
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#config_name = os.getenv("FLASK_ENV", "default")
config_name = "development"
app.config.from_object(config[config_name])

#CORS(app, headers=['Content-Type'])


######################################################

@app.route('/submit_form', methods=['GET', 'POST'])
def model_upload():
    if request.method == 'POST':
        id = request.form.get('id')
        time_series = request.form.get('time-series')
        dimension = request.form.get('dimension')
        label = request.form.get('label')
        fact = request.form.get('fact')
        model = request.form.get('model')

        # to debug
        form = dict(request.form)
        for k, v in form.items():
            print(str(k) + ":" + str(v))

        # call model, do magic and return to template
        return ('Got: id={}, time_series={}, dimension={}, label={}, fact={}, model={}'
                .format(id, time_series, dimension, label, fact, model))

    else:
        return "Nothing to see here."

######################################################

# create route that renders index.html template
@app.route("/")
def home():
    """Return the dashboard homepage"""
    return render_template("index.html")


#########################################

@app.route('/upload')
def upload_complete():
    """
	create directory /uk_id on server
	upload the file to ./uk_id directory on server
	Get first row from the file and parse the data
    Show appropiate data
    """


    return render_template("index.html")


#########################################
@app.route('/submit/<v_uk_id>')
def submit_complete(v_uk_id):
    """
	a. JSON file of the column type allocation saved to ./uk_id folder
	b. python function has been called like  (uk_id)
	c. Calls fx_result(uk_id) that return 'Processing' or 'Ready'
	d. if processing then show processing else show result in graph section.
	   Template (submit_complete.html) can use jpeg file saved for 6 graphs and json files for any data.
    """


    return render_template("submit_complete.html")


#################################################
if __name__ == "__main__":
    app.run(debug=True)
