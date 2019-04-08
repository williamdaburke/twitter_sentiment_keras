#!/usr/bin/env python

import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
    
def load_combined_df():    
    #script to return combined dataframe of txt csv and json data files.
    csv_df = pd.read_csv('data/csv_file.csv')
    txt_df = pd.read_csv('data/txt_file.txt')
    #check columns are same
    assert(sorted(csv_df.columns)==sorted(txt_df.columns))
    #check sizes
    assert(txt_df.shape==csv_df.shape)
    combined_df = pd.concat([csv_df,txt_df])

    #check for duplicates
    assert(combined_df[combined_df.duplicated(keep=False)].empty)

    with open('data/json_file.json') as data_file:    
        json_df = pd.io.json.json_normalize(json.load(data_file))

    #check columns are same
    assert(sorted(csv_df.columns)==sorted(json_df.columns))
    #check sizes
    assert(txt_df.shape==json_df.shape)
    
    combined_df = pd.concat([combined_df,json_df])
    print('\ndf shape: ',combined_df.shape)

    print('\nrows with null values: ',combined_df[combined_df.isnull().any(axis=1)])

    #delete row 552 which has no good data 
    combined_df = combined_df.drop([552],axis=0)

    #basically all entries platform is twitter,
    print('\ntypes of platforms: ',combined_df['properties.platform'].value_counts())
    print('\nrows that arent twitter: ',combined_df[~(combined_df['properties.platform'] == 'twitter')].shape)

    #therefore this column can be dropped.
    combined_df = combined_df.drop(['properties.platform'],axis=1)

    assert(combined_df[combined_df.isnull().any(axis=1)].empty)

    #convert friends to numeric
    combined_df['author.properties.friends'] = combined_df['author.properties.friends'].astype(int)
    #check to see converted
    print('\ntype of friends col: ',combined_df['author.properties.friends'].infer_objects().dtype)

    #most users are from UK
    print('\n country breakdown: ',combined_df['location.country'].value_counts())
    plt.rcParams['figure.figsize'] = [5,3]
    combined_df['location.country'][combined_df['location.country']!='GB'].value_counts().plot(kind='bar')
    
    return combined_df

def encode_labels(df,cat_columns):
    for col in cat_columns:
        print(col)
        lbl = LabelEncoder()
        lbl.fit(list(df[col].values.astype('str')))
        df[col] = lbl.transform(list(df[col].values.astype('str')))
    return df

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result
