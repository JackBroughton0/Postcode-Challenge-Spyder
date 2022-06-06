# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:41:18 2022

@author: Admin
"""

import pandas as pd
from string import punctuation
from collections import defaultdict


def cleanInput(input_data):
    """Function that applies essential cleaning to user input."""
    df = input_data.applymap(lambda x: x.upper() if type(x) == str else x) #Make values upper case
    df = df.apply(lambda x: x.str.strip()) #Strip string values
    df = df.apply(lambda x: x.str.strip(punctuation)) #Strip punctuation
    df.fillna('', inplace=True)   
    Postcode = df['Postcode'] 
    df.pop('Postcode') #Temporarily remove postcode to apply regex replace methods

    df = df.replace(r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}', '',
                    regex=True).astype('string') #Remove redundant postcode in address line columns
    df = df.replace(' RD', ' ROAD', regex=True).astype('string') #Normalise street names

    df['Single_Line_Address'] = df.apply(lambda x: ', '.join(x[x != '']), axis=1)
    df.drop(['Address_Line_1', 'Address_Line_2', 'Address_Line_3',
             'Address_Line_4', 'Address_Line_5'], axis=1, inplace=True) #Remove extra columns    
    df.insert(1, 'Postcode', Postcode) #Reinsert postcode
    return df


def flagStreetInPostcode(df_database, clean_df):
    "Function to map streets from example database to input postcodes"
    post_street = defaultdict(list)    
    post_list = df_database.POSTCODE.tolist()    
    street_list = df_database.STREET_NAME.tolist()    
    
    for k, v in zip(post_list, street_list):
        if v not in post_street[k]:
            post_street[k].append(v)
    post_street = {key:tuple(lst) for key, lst in post_street.items()}
    clean_df['Expected_Street'] = clean_df['Postcode'].map(post_street) #Add expected street column
    clean_df['Expected_Street'] = clean_df['Expected_Street'].fillna('')
    
    #Apply lambda function for matching
    clean_df['Street_In_Postcode'] = clean_df.apply(lambda x: 'Yes' if any(str(street) 
                                        in x.Single_Line_Address for street in 
                                        x.Expected_Street) else 'No', axis=1)
    clean_df.drop('Expected_Street', axis=1, inplace=True)
    df_output = clean_df 
    return df_output


if __name__=='__main__':
    df = pd.read_csv("C://Users/Admin/IDenteqSpyder/example_input_data.csv") #Read input data
    example_abp_data = pd.read_csv("C://Users/Admin/IDenteqSpyder/example_abp_data.csv") #Read example database
    df = cleanInput(input_data=df)
    df_output = flagStreetInPostcode(df_database=example_abp_data, clean_df=df)
    df_output.to_csv("C:/Users/Admin/IDenteqSpyder/example_output_data1.csv",
               sep=',', encoding='utf-8', index=False) #Save output csv