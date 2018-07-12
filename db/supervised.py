
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import json
import mpu.io
import pickle
from sklearn.externals import joblib

def fx_supervised(v_uk_id):
    # 
    my_path = "data/"+v_uk_id+"/"
    v_input_json_file = my_path+"details.json"
    v_output_json_file = my_path+"result_desc.json"
    
    
    input_json = mpu.io.read(v_input_json_file)
    output_json = mpu.io.read(v_output_json_file)
    
    v_input_csv = my_path + input_json['filename']
    #v_input_csv = my_path + 'demo.csv'
    
    data = pd.read_csv(v_input_csv)
    ######################
    # Get labels for outliers and normal from dataset 
    ######################
    v_label = input_json['label'][0]
    v_amount = input_json['fact'][0]
    v_time = input_json['time_series'][0]
    outlier = data[v_label].max()
    print('outlier label is ' + str(outlier))
    normal = data[v_label].min()
    print('normal label is ' + str(normal))
    ######################
    # Get counts and pct of outlier records compared with general population
    ######################
    countOutliers = len(data[(data[v_label]==outlier)])
    countNormal = len(data[(data[v_label]==normal)])
    #
    count_classes = pd.value_counts(data[v_label], sort = True).sort_index()
    fig = plt.figure() 
    count_classes.plot(kind = 'bar')
    plt.title("Fraud class histogram")
    plt.xlabel("Class")
    plt.ylabel("Frequency")
    fig.savefig(my_path + "image1.png")    
    
    pctOutliers = countOutliers/(countOutliers+countNormal)*100
    print("Percent of outliers is " + str(pctOutliers))
    
    ######################
    # Normalize amount and remove time series data
    ######################
    from sklearn.preprocessing import StandardScaler
    data['normAmount'] = StandardScaler().fit_transform(data[v_amount].values.reshape(-1, 1))
    data = data.drop([v_time,v_amount],axis=1)
   
    X = data.iloc[:, data.columns != v_label]
    y = data.iloc[:, data.columns == v_label]
    
    # Whole dataset
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 0)
    print("Number transactions train dataset: ", len(X_train))
    print("Number transactions test dataset: ", len(X_test))
    print("Total number of transactions: ", len(X_train)+len(X_test))
    
    ######################
    # if pctOutliers less than 50 percent of population use under sampling of normal datset
    ######################
    if pctOutliers < 50:
        print("it is less than 50% so data is skewed")
        fraud_indices = np.array(data[data[v_label] == outlier].index)
        # Picking the indices of the normal classes
        normal_indices = data[data[v_label] == 0].index
        # Reduce normal sample size to match outlier size so machine learning is better
        random_normal_indices = np.random.choice(normal_indices, countOutliers, replace = False)
        print(type(random_normal_indices))
        # Append the two samples
        under_sample_indices = np.concatenate([fraud_indices,random_normal_indices])
        # Under sample dataset
        under_sample_data = data.iloc[under_sample_indices,:]
        X_undersample = under_sample_data.iloc[:, under_sample_data.columns != v_label]
        y_undersample = under_sample_data.iloc[:, under_sample_data.columns == v_label]
        
        X_train_undersample, X_test_undersample, y_train_undersample, y_test_undersample = train_test_split(X_undersample,y_undersample,test_size = 0.3, random_state = 0)
        print("Number transactions train undersample dataset: ", len(X_train_undersample))
        print("Number transactions test undersample dataset: ", len(X_test_undersample))
        print("Total number of undersample transactions: ", len(X_train_undersample)+len(X_test_undersample))

        from sklearn.linear_model import LogisticRegression
        #from sklearn.cross_validation import KFold, cross_val_score
        from sklearn.metrics import confusion_matrix
        
        # Use this C_parameter to build the dataset
        best_c = 0.01
        lr = LogisticRegression(C = best_c, penalty = 'l1')
        lr.fit(X_train_undersample,y_train_undersample.values.ravel())
        y_pred_undersample = lr.predict(X_test_undersample.values)

        # Compute confusion matrix using the undersampled predictor set
        # over the undersampled test data
        cnf_matrix = confusion_matrix(y_test_undersample,y_pred_undersample)
        np.set_printoptions(precision=2)

        print("Recall metric in the undersampled testing dataset: ", cnf_matrix[1,1]/(cnf_matrix[1,0]+cnf_matrix[1,1]))

        # Plot non-normalized confusion matrix
        class_names = [0,1]
        plt.figure()
        plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='Confusion matrix')
        fig.savefig(my_path + "image2.png")
        
        # again train logistic Regression model with undersampled dataset
        lr = LogisticRegression(C = best_c, penalty = 'l1')
        lr.fit(X_train_undersample,y_train_undersample.values.ravel())
        
        # now predict over original test dataset with skewed values
    
        y_pred = lr.predict(X_test.values)
       
        cnf_matrix = confusion_matrix(y_test,y_pred)
        np.set_printoptions(precision=2)
        
        print("Recall metric in the original testing dataset: ", cnf_matrix[1,1]/(cnf_matrix[1,0]+cnf_matrix[1,1]))
        # Plot non-normalized confusion matrix
        class_names = [0,1]
        plt.figure()
        plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='Confusion matrix')
        fig.savefig(my_path + "image3.png")       
    best_c = 10
    # Use this C_parameter to build the final model with the whole training dataset and predict the classes in the test
    # dataset
    lr = LogisticRegression(C = best_c, penalty = 'l1')
    lr.fit(X_train,y_train.values.ravel())
    y_pred_undersample = lr.predict(X_test.values)

    # Save the trained model as a pickle string.
    saved_model = pickle.dumps(lr)
        
    # Save the model as a pickle in a file
    joblib.dump(lr, 'supervise.pkl')
                
    # now predict over original test dataset with skewed values
    
    y_pred = lr.predict(X_test.values)
    
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_test,y_pred_undersample)
    np.set_printoptions(precision=2)

    print("Recall metric in the testing dataset: ", cnf_matrix[1,1]/(cnf_matrix[1,0]+cnf_matrix[1,1]))

    # Plot non-normalized confusion matrix
    class_names = [0,1]
    plt.figure()
    plot_confusion_matrix(cnf_matrix
                      , classes=class_names
                      , title='Confusion matrix')
    fig.savefig(my_path + "image4.png")
    
    
import itertools
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print("Normalized confusion matrix")
    else:
        1#print('Confusion matrix, without normalization')

    #print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


