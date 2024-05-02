import pandas as pd
import numpy as np
from api.api_handler import scan_data

def cleanScanData():
    df_scanlog = scan_data()
    # Cleaning/Transforming dataframe ----------------------------------------------
    df_scanlog['refCode'] = df_scanlog['refCode'].astype(str)
    df_scanlog['jobType'] = df_scanlog['refCode'].str[:3]
    df_scanlog['refCode'] = df_scanlog['refCode'].str.slice(start=5)
    df_scanlog['createTime'] = pd.to_datetime(df_scanlog['createTime'], format='mixed') #Converting the 'createTime' column to DateTime format using infer
    df_scanlog['refCode'] = pd.to_numeric(df_scanlog['refCode'])# Conversion to integer
    df_scanlog['fullName'] = df_scanlog['fullName'].astype("string")
    df_scanlog['refCode'] = df_scanlog['refCode'].fillna('')
    df_scanlog = df_scanlog[df_scanlog["jobType"] == 'Job']
    df_scanlog = df_scanlog[df_scanlog["status"] == 'Inserted']
    names_to_find = ['Removed', 'Removed', 'Removed', 'Removed', 'Removed', 'Removed', 'Removed', 'Removed', 'Removed', 'Removed'] #Removed to protect the privacy of my colleagues
    df_scanlog = df_scanlog[df_scanlog["fullName"].isin(names_to_find)]
    df_scanlog['month'] = pd.to_datetime(df_scanlog['createDate']).dt.month_name()
    df_scanlog['barcode'] = pd.to_numeric(df_scanlog['barcode'], errors='coerce')
    df_scanlog['createTime'] = pd.to_datetime(df_scanlog['createTime'])

    #Load excel file discrepancies & positive feedback
    #Removed to protect the privacy of my colleagues
    file_path = 'assets/discrepancy_excel.xlsx' 
    df_excelDiscrepancies = pd.read_excel(file_path, engine='openpyxl')
    file_path = 'assets/positive_feedback.xlsx'
    df_positiveFeedback = pd.read_excel(file_path, engine='openpyxl')

    # Variables
    drop_dupl_orders = df_scanlog[['refCode','month']].drop_duplicates(subset='refCode')
    df_scanlog['month'] = pd.to_datetime(df_scanlog['createDate']).dt.month_name()
    unique_names = df_scanlog['fullName'].unique()
    df_monthlyJobs = df_scanlog.groupby('month', sort=False)['refCode'].nunique().reset_index()

    # Tech Table Dataframe
    tech_table = pd.DataFrame({'fullName': unique_names})
    tech_table = tech_table.merge(df_scanlog.groupby('fullName')['refCode'].nunique().reset_index().rename(columns={'refCode': 'Orders'}), on='fullName', how='left')\
            .merge(df_excelDiscrepancies.groupby('tech_name')['Discrepancies'].count().rename('Discrepancies'), left_on='fullName', right_index=True, how='left')\
            .merge(df_positiveFeedback.groupby('tech_name')['positive_fb'].count().rename(r'+Feedback'), left_on='fullName', right_index=True, how='left')\
            .sort_values(by=['fullName'], ascending=[False])\
            .rename(columns={'fullName': 'Technician'})
    tech_table['Technician'] = [name[:6] + "..." if len(name) > 6 else name for name in tech_table['Technician']]

    # Bar Visual
    df_discrepancies = pd.merge(df_excelDiscrepancies, drop_dupl_orders, left_on='contract_number', right_on='refCode', how='left')
    bar_discrepanciesMonth = df_discrepancies.groupby('month', sort=False)['Discrepancies'].count()
    df_monthlyJobsDiscrepancies = pd.merge(df_monthlyJobs, bar_discrepanciesMonth, left_on='month', right_on='month', how='left')
    #Pie Chart
    df_pieChart = pd.DataFrame(df_excelDiscrepancies['Discrepancies'].value_counts().reset_index())
    df_monthlyJobsDiscrepancies['month']= [name[:3] if len(name) > 3 else name for name in df_monthlyJobsDiscrepancies['month']]

    # Card mistake x days ago
    discrepancies_date = df_discrepancies.merge(df_scanlog.groupby('refCode')['createDate'].max().reset_index(), on='refCode', how='left')
    discrepancies_date['createDate'] = pd.to_datetime(discrepancies_date['createDate'])
    discrepancies_date = discrepancies_date.sort_values(by='createDate')
    discrepancies_date['days_diff'] =  discrepancies_date['createDate'].diff().dt.days
    last_entry_date = discrepancies_date['createDate'].max()
    current_date = pd.Timestamp.now()
    days_without_discrepancies = (current_date - last_entry_date).days

    return df_scanlog, tech_table, df_monthlyJobsDiscrepancies, df_pieChart, days_without_discrepancies