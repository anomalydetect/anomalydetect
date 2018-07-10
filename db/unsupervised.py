from os import path
from utils import fix_path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels import robust
from statsmodels.stats.stattools import medcouple
import json

def fx_unsupervised(v_uk_id):
	#v_uk_id= 123456
	my_path = "data/" + v_uk_id + "/"
	v_input_json_file = my_path + "details.json"

	with open(v_input_json_file, encoding="utf-8") as data_file:
		input_json = json.load(data_file)

	v_input_csv = my_path + input_json['filename']

	df = pd.read_csv(v_input_csv)
	df['anomalydetectid']=df.index
	######################
	v_id = 'anomalydetectid'
	v_analysis_columns_list = input_json['dimension'] 
	df_outliers = pd.DataFrame({})
	#v_analysis_columns = ''.join(v_analysis_columns_list)
	for my_analysis_column in v_analysis_columns_list:
		v_df_temp = fx_ThreeSigmaRule(df[v_id], df[my_analysis_column], 2, 1)
		v_df_temp['Outlier Type'] = 'Three Sigma Rule'
		v_df_temp['Analysis Column'] = my_analysis_column
		df_outliers = pd.concat([df_outliers, v_df_temp])
	######################
	v_output_result_csv = my_path+"result_individual_columns.csv"
	df_outliers.to_csv(v_output_result_csv, encoding="utf-8", index=False, header=True)

	x_groupby_type = df1.groupby(['Analysis Column'])
	df2 = x_groupby_type.count()
	df2.reset_index(inplace=True)
	df3 = df2.sort_values(['data'], ascending=True).head(4)

	for i, r in df3.iterrows():
		v_filename = 'image'+str(i)
		v_list = df.loc[:, [r['Analysis Column']]]
		v_title = 'Outliers for '+r['Analysis Column']
		fx_box_plot (v_uk_id,v_list , v_title,v_filename )


	return df_outliers


def fx_unsupervised_plot(v_uk_id):
	my_path = "data/" + v_uk_id + "/"
	v_input_json_file = my_path + "details.json"

	with open(v_input_json_file, encoding="utf-8") as data_file:
		input_json = json.load(data_file)

	v_input_csv = my_path + input_json['filename']

	df = pd.read_csv(v_input_csv)

	######################


	v_output_json_contents = {
		"image_title1": "nish1",
		"image_title2": "jfbgcjshhgsj",
		"image_title3": "jfbgcjshhgsj",
		"image_title4": "jfbgcjshhgsj",
		"image_name1": "image1.png",
		"image_name2": "image2.png",
		"image_name3": "image3.png",
		"image_name4": "image4.png",
		"image_desc1": "jfbgcjshhgsj",
		"image_desc2": "jfbgcjshhgsj",
		"image_desc3": "jfbgcjshhgsj",
		"image_desc4": "jfbgcjshhgsj",
		"model": [{"model_desc": "ssss", "model_file": "ssss"}, {"model_desc": "ssss", "model_file": "ssss"}]
	}
	######################

	return v_output_json_contents

def fx_box_plot (v_uk_id,v_list , v_title,v_filename ):
    my_path = "data/" + v_uk_id + "/"
    fig, ax = plt.subplots()
    jpg_filename = my_path + v_filename+'.jpg'
    png_filename = my_path + v_filename+'.png'
    x = range(len(v_list))
    ax.boxplot(v_list, patch_artist=True)
    ax.set_title(v_title)
    fig.tight_layout()
    #fig.show()
    fig.savefig(jpg_filename, dpi=1000)
    fig.savefig(png_filename+'.png', dpi=1000)
	
def fx_ThreeSigmaRule(series_id, series_data, v_number_of_std, v_masking_Iteration):
	'''
	value should be in +- range of -->mean + n * std
	Probability
	n =1 --> 68
	n =2 -->  95
	n= 3  --> 99.7
	Usage : 
	df_outliers= fx_ThreeSigmaRule(df['myid'],df['series1'], 2,2)
	df_outliers
	Good for normal distributed data ---series or sequences
	Drawback :
	Not good when data is not normal distribution 
	Sensitive to extreme points  ---Masking effect. If extreme value is too large then it overshadow other values
	-->iteration solves this issue
	'''

	v_df = pd.DataFrame({})
	v_df_outliers_final = pd.DataFrame({})
	v_df['anomalydetectid'] = series_id
	v_df['data'] = series_data

	v_Iteration = 0

	while (v_Iteration < v_masking_Iteration):
		#############################
		print(str(v_masking_Iteration))
		v_masking_Iteration = v_masking_Iteration - 1
		v_threshold = np.std(v_df['data']) * v_number_of_std
		v_mean = np.mean(v_df['data'])
		print(str(v_mean - v_threshold))
		print(str(v_threshold + v_mean))
		where_tuple = (np.abs(v_df['data'] - v_mean) > v_threshold)
		v_df_outliers = v_df[where_tuple]

		# v_outliersList = [ [r[0] , r[1]] for  i,r in v_df.iterrows() if np.abs(r[1]) > v_threshold + v_mean]

		if (len(v_df_outliers) > 0):

			v_df_outliers_final = pd.concat([v_df_outliers_final, v_df_outliers])

			# Update data - remove otliers from the list
			# list1 = [x for x in list1 if x not in v_outliersList[1]]
			where_tuple = (np.abs(v_df['data'] - v_mean) <= v_threshold)
			v_df = v_df[where_tuple]

		else:

			break

		############################

	if len(v_df_outliers_final) > 0:

		return (v_df_outliers_final)

	else:
		return (pd.DataFrame({}))
		print("Three are No Outliers")


###############################################################################
def fx_mad_Rule(series_id, series_data, v_number_of_std):
    '''
    value should be in +- range of -->median + n * MAD/.6745
    Usage : 
    df_outliers= fx_mad_Rule(df['myid'],df['series1'], 2)
    df_outliers
    Good for not normal distributed data
    No issue with extreme points
    Drawback :
    Not good when data is normal distribution 
    Too agressive

    '''
    # warning ignore for verylarge values 
    # np.seterr(invalid='ignore')
    # np.errstate(invalid='ignore')
    # np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data

    #############################
    v_threshold = robust.mad(v_df['data'], c=1) * v_number_of_std / 0.6745
    v_median = np.median(v_df['data'])

    print(str(v_median - v_threshold))
    print(str(v_threshold + v_median))
    where_tuple = (np.abs(v_df['data'] - v_median) > v_threshold)
    v_df_outliers_final = v_df[where_tuple]

    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else:
        print("Three are No Outliers")


###############################################################################
def fx_boxplot_Rule(series_id, series_data):
    '''
    value should be in +- range of -->(y > q3 + 1.5 * iqr) or (y < q1 - 1.5 * iqr
    Usage : 
    df_outliers= fx_boxplot_Rule(df['myid'],df['series1'])
    df_outliers
    For presense of outliers --less sensitive than 3 sigma but more sensitive to MAD test 
    No depenedence of median and mean
    better for moderately asymmetric distribution
    Drawback :
    Too agressive

    '''
    # warning ignore for verylarge values 
    # np.seterr(invalid='ignore')
    # np.errstate(invalid='ignore')
    # np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data

    #############################
    q1 = np.percentile(v_df['data'], 25)

    q3 = np.percentile(v_df['data'], 75)

    iqr = q3 - q1

    print(str(q1 - 1.5 * iqr))
    print(str(q3 + 1.5 * iqr))
    where_tuple1 = (v_df['data'] > q3 + 1.5 * iqr)
    where_tuple2 = (v_df['data'] < q1 - 1.5 * iqr)
    v_df_outliers_final = v_df[where_tuple1 | where_tuple2]

    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else:
        print("Three are No Outliers")


###############################################################################

def fx_adjusted_boxplot_Rule(series_id, series_data):
    '''
    value should be in +- range of -->(y > q3 + 1.5 * iqr) or (y < q1 - 1.5 * iqr
    Usage : 
    df_outliers= fx_boxplot_Rule(df['myid'],df['series1'])
    df_outliers
    For presense of outliers --less sensitive than 3 sigma but more sensitive to MAD test 
    No depenedence of median and mean
    better for moderately asymmetric distribution
    Drawback :
    Too agressive

    '''
    # warning ignore for verylarge values 
    # np.seterr(invalid='ignore')
    # np.errstate(invalid='ignore')
    # np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data

    #############################
    q1 = np.percentile(v_df['data'], 25)

    q3 = np.percentile(v_df['data'], 75)

    iqr = q3 - q1

    mc = medcouple(v_df['data'])

    if (mc >= 0):

        lr = q1 - 1.5 * iqr * np.exp(-4 * mc)
        ur = q3 + 1.5 * iqr * np.exp(3 * mc)
    else:
        lr = q1 - 1.5 * iqr * np.exp(-3 * mc)
        ur = q3 + 1.5 * iqr * np.exp(4 * mc)

    print(str(lr))
    print(str(ur))

    where_tuple1 = (v_df['data'] > ur)
    where_tuple2 = (v_df['data'] < lr)
    v_df_outliers_final = v_df[where_tuple1 | where_tuple2]

    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else:
        print("Three are No Outliers")

###############################################################################


###############################################################################


###############################################################################


###############################################################################


###############################################################################
