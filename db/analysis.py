
from os import path
from utils import fix_path
from db.unsupervised import fx_unsupervised
from db.supervised import fx_supervised
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def fx_analysis(v_uk_id):


    my_path = "data/"+v_uk_id+"/"
    v_input_json_file = my_path+"details.json"
    v_output_result_csv = my_path+"result.csv"
    v_output_json_file = my_path+"result_desc.json"


    with open(v_input_json_file, encoding="utf-8") as data_file:
        input_json = json.load(data_file)

    v_input_csv = my_path + input_json['filename']
    
    v_learning_type = input_json['learning_type']
    

    if v_learning_type == 'unsupervised' :
        fx_unsupervised(v_uk_id)
    else :
        fx_unsupervised(v_uk_id)
    

    return 'Success'

def fx_result(v_uk_id):
    my_path = "data/"+v_uk_id+"/"
    v_input_json_file = my_path+"details.json"
    v_output_result_csv = my_path+"result.csv"
    v_output_json_file = my_path+"result_desc.json"
    my_file = Path(v_output_json_file)
    if my_file.is_file():
        return 'COMPLETED'
    else:
        return 'PROCESSING'
		
		
