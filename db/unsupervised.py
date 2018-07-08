
from os import path
from utils import fix_path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels import robust
from statsmodels.stats.stattools import medcouple


def fx_unsupervised(v_uk_id):

	my_path = "data/"+v_uk_id+"/"
    v_input_json_file = my_path+"details.json"
	
	with open(v_input_json_file, encoding="utf-8") as data_file:
		input_json = json.load(data_file)

    v_input_csv = my_path + input_json['filename']
    
	df = pd.read_csv(v_input_csv)
	
	######################
    v_id = input_json['id'][0]
	v_fact = input_json['fact'][0]
	v_analysis_columns_list = v_fact
	
	v_analysis_columns = ''.join(v_analysis_columns_list)
	df_outliers= fx_ThreeSigmaRule(df[v_id],df[v_analysis_columns], 2 , 1)
	 
	df_outliers['Outlier Type'] = 'Three Sigma Rule'
	df_outliers['Analysis Columns'] = v_analysis_columns
	
	######################

    return df_outliers

def fx_ThreeSigmaRule(series_id, series_data, v_number_of_std , v_masking_Iteration):
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
    v_df['id'] = series_id
    v_df['data'] = series_data
    
    v_Iteration = 0

    while (v_Iteration < v_masking_Iteration):
        #############################
        print (str(v_masking_Iteration))
        v_masking_Iteration = v_masking_Iteration -1
        v_threshold = np.std(v_df['data']) * v_number_of_std
        v_mean = np.mean(v_df['data'])
        print (str(v_mean -v_threshold ))
        print (str(v_threshold + v_mean) )
        where_tuple = (np.abs(v_df['data'] -v_mean)> v_threshold )
        v_df_outliers = v_df[where_tuple]



        #v_outliersList = [ [r[0] , r[1]] for  i,r in v_df.iterrows() if np.abs(r[1]) > v_threshold + v_mean]

        if (len(v_df_outliers) > 0):

                v_df_outliers_final = pd.concat([v_df_outliers_final, v_df_outliers])   

                # Update data - remove otliers from the list
                #list1 = [x for x in list1 if x not in v_outliersList[1]]
                where_tuple = (np.abs(v_df['data'] -v_mean) <= v_threshold )
                v_df = v_df[where_tuple]

        else :

            break
            
        

        ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else :
        print("Three are No Outliers")


		
###############################################################################
def fx_mad_Rule(series_id, series_data, v_number_of_std ):
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
    #np.seterr(invalid='ignore')
    #np.errstate(invalid='ignore')
    #np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data
    

    #############################
    v_threshold = robust.mad(v_df['data'], c=1) * v_number_of_std / 0.6745
    v_median = np.median(v_df['data'])

    print (str(v_median -v_threshold ))
    print (str(v_threshold + v_median) )
    where_tuple = (np.abs(v_df['data'] -v_median)> v_threshold )
    v_df_outliers_final = v_df[where_tuple]


    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else :
        print("Three are No Outliers")



###############################################################################
def fx_boxplot_Rule(series_id, series_data ):
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
    #np.seterr(invalid='ignore')
    #np.errstate(invalid='ignore')
    #np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data
    

    #############################
    q1 = np.percentile(v_df['data'], 25)

    q3 = np.percentile(v_df['data'], 75)

    iqr = q3 - q1

    print (str(q1 - 1.5 * iqr))
    print (str(q3 + 1.5 * iqr) )
    where_tuple1 = (v_df['data'] > q3 + 1.5 * iqr )
    where_tuple2 = (v_df['data'] < q1 - 1.5 * iqr )
    v_df_outliers_final = v_df[where_tuple1 | where_tuple2]


    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else :
        print("Three are No Outliers")


###############################################################################

def fx_adjusted_boxplot_Rule(series_id, series_data ):
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
    #np.seterr(invalid='ignore')
    #np.errstate(invalid='ignore')
    #np.warnings.filterwarnings('ignore')
    v_df = pd.DataFrame({})
    v_df_outliers_final = pd.DataFrame({})
    v_df['id'] = series_id
    v_df['data'] = series_data
    

    #############################
    q1 = np.percentile(v_df['data'], 25)

    q3 = np.percentile(v_df['data'], 75)

    iqr = q3 - q1
    
    mc = medcouple(v_df['data'])

    
    if (mc >= 0) :
        
        lr = q1 - 1.5 * iqr * np.exp(-4 * mc)
        ur = q3 + 1.5 * iqr * np.exp(3 * mc)
    else :
        lr = q1 - 1.5 * iqr * np.exp(-3 * mc)
        ur = q3 + 1.5 * iqr * np.exp(4 * mc)
        
    
    
    
    print (str(lr))
    print (str(ur) )
    
    where_tuple1 = (v_df['data'] > ur )
    where_tuple2 = (v_df['data'] < lr )
    v_df_outliers_final = v_df[where_tuple1 | where_tuple2]


    ############################

    if len(v_df_outliers_final) > 0:

        return (v_df_outliers_final)

    else :
        print("Three are No Outliers")

###############################################################################



###############################################################################



###############################################################################



###############################################################################



###############################################################################
