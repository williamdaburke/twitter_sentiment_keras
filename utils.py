#!/usr/bin/env python

import json, re
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
   
    return combined_df

def preprocess_values(df):
    print('\nrows with null values: ',df[df.isnull().any(axis=1)].index)

    #delete row 552 which has no good data 
    df = df.drop([552],axis=0)
    
    #basically all entries platform is twitter,
    #print('\ntypes of platforms: ',df['properties.platform'].value_counts())
    print('rows that arent twitter: ',df[~(df['properties.platform'] == 'twitter')].shape[0])

    #therefore this column can be dropped.
    df = df.drop(['properties.platform'],axis=1)
    
    print('\ndropped one row, fixed other null by dropping platform col, as unneeded')

    assert(df[df.isnull().any(axis=1)].empty)

    #convert friends to numeric
    df['author.properties.friends'] = df['author.properties.friends'].astype(int)
    #check to see converted
    print('\ntype of friends col: ',df['author.properties.friends'].infer_objects().dtype)

    #most users are from UK
    print('\n country breakdown: ',df['location.country'].value_counts())

    print('\ndf shape: ',df.shape)
    return df
    

def encode_labels(df,cat_columns):
    for col in cat_columns:
        print('encoded:',col)
        lbl = LabelEncoder()
        lbl.fit(list(df[col].values.astype('str')))
        df[col] = lbl.transform(list(df[col].values.astype('str')))
    return df

def normalize(df,cols_to_normalize=None):
    cols = cols_to_normalize if cols_to_normalize else df.columns
    for feature_name in cols:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return df


