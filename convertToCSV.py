import sys
import pandas as pd
from pandas import DataFrame
import json
import io
import csv


data = 'media - 06-20-18.txt'
print ("This is json data input", data)

def js_r(data):
   with io.open(data, encoding='utf-8') as f_in:
       return(json.load(f_in))

if __name__ == "__main__":
    my_dic_data = js_r(data)
    #print("This is my dictionary", my_dic_data)

keys= my_dic_data.keys()
print ("The original dict keys",keys)
temp_list = []
for key in keys:
	temp_list = my_dic_data[key] + temp_list

#dict_you_want={'my_items':my_dic_data[key]}
#print ("These are the keys to dict_you_want",dict_you_want.keys())

#print ("This is the dictionary of SO_users", dict_you_want)
df=pd.DataFrame(temp_list)
#print ("df:", df)

df2=df.apply(pd.Series)
#print ("df2",df2)
#df3=pd.concat([df2.drop(['hashtags'],axis=1),df2['user'].apply(pd.Series)],axis=1)

df2.to_csv(data[:-4] + ".csv", encoding='utf-8', index=False)