import pandas as pd
from sklearn import linear_model
import numpy as np
df1=pd.read_excel(r"C:\Users\Ashish\Documents\lab4.xlsx")    #reading data from csv
df=pd.DataFrame(df1)    #converting to dataframe
#x=df['time']    #extracting the feature class. In this case, it is only time column. If we have more features,
#then just form a new dataframe fter dropping the target class
y=df['result']
x=df.drop('result',1)
x_train=x[:9]
x_test=x[9:13]
y_train=y[:9]
y_test=y[9:13]
regr = linear_model.SGDClassifier()    #linear classfication model using SGDClassifier
regr.fit(x_train, y_train)    #fitting to the dataset
print('Coefficients: \n', regr.coef_,regr.intercept_)    #coefficient and intercept
regr.predict(x_test)    #class prediction
