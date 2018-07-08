
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
    
    
    ##################### Temp code
    df = pd.read_csv(v_input_csv)
    df_result=df.head(50)
    df_result.to_csv(v_output_result_csv, encoding="utf-8", index=False, header=True)
    
    v_output_json_contents = {
    "image_title1":  "nish1" ,
    "image_title2":  "jfbgcjshhgsj" ,
    "image_title3":  "jfbgcjshhgsj" ,
    "image_title4":  "jfbgcjshhgsj" ,
    "image_name1":  "image1.png" ,
    "image_name2":  "image2.png" ,
    "image_name3":  "image3.png" ,
    "image_name4":  "image4.png" ,
    "image_desc1":  "jfbgcjshhgsj" ,
    "image_desc2":  "jfbgcjshhgsj" ,
    "image_desc3":  "jfbgcjshhgsj" ,
    "image_desc4":  "jfbgcjshhgsj" ,
    "model":  [ {"model_desc" : "ssss" ,"model_file" : "ssss" } , {"model_desc" : "ssss" ,"model_file" : "ssss" } ] 
    }
    with open(v_output_json_file, 'w') as outfile:
        json.dump(v_output_json_contents, outfile)
    

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
		
		
