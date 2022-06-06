# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 23:39:02 2022

@author: Admin
"""

import pandas as pd
import IDenteqSpyder

if __name__ == '__main__':
    df = pd.read_csv("C://Users/Admin/IDenteqSpyder/example_input_data.csv") #Read input data
    example_abp_data = pd.read_csv("C://Users/Admin/IDenteqSpyder/example_abp_data.csv") #Read example database
    df = IDenteqSpyder.cleanInput(input_data=df)
    df_output = IDenteqSpyder.flagStreetInPostcode(df_database=example_abp_data, clean_df=df)
    df_output.to_csv("C:/Users/Admin/IDenteqSpyder/example_output_data2(test).csv",
               sep=',', encoding='utf-8', index=False) #Save output csv