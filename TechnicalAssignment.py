#!/usr/bin/env python
# coding: utf-8
import pandas as pd

data=pd.read_csv('C:/Users/katar/Downloads/TechnicalAssignment.csv')


data.head()

cut_off_secs=[['P0',32400],['P1',39600],['P2',43200]]

cutoff_df=pd.DataFrame(cut_off_secs,columns=['Category','cutofftime'])

data_with_cutoff=pd.merge(data,cutoff_df,how='inner',on=['Category'])

status_col=[]
for index,row in data_with_cutoff.iterrows():
    if row['Time']>row['cutofftime']:
        status=0
        status_col.append(status)
    else:
        status=1
        status_col.append(status)

data_with_cutoff['status']=status_col

data_with_cutoff['date']=data_with_cutoff['DateStamp'].str[0:10]


#Populate a 1/0 (success/failure) against each row, based on the actual sync time and the cutoff defined above. A sync which does not complete before the cutoff time is a failure for that particular day
data_with_cutoff

#Find out the top 10 Org IDs with highest and lowest success rates for EI sync time for the entire period of 31May-04Jul

sucess_status=data_with_cutoff.groupby(['Org ID'])['status'].sum().reset_index()

sucess_status.head()

top_10_orgs=sucess_status.sort_values(by='status', ascending=False)[0:10]

top_10_orgs['Org ID']

lowest_10_orgs=sucess_status.sort_values(by='status', ascending=True)[0:10]


lowest_10_orgs['Org ID']

#List out all the org IDs which have lesser than 35 entries in the data given


orgs_entries=data_with_cutoff.groupby(['Org ID'])['date'].count().reset_index()

cutoff_orgs_less_than_35_entries=orgs_entries[orgs_entries['date']<35]

cutoff_orgs_less_than_35_entries['Org ID']

pd.set_option("display.max_rows", 999)

data_with_cutoff.head()


### Step2

data_with_cutoff['date'] = pd.to_datetime(data_with_cutoff['date']) - pd.to_timedelta(7, unit='d')
output_df=data_with_cutoff.groupby(['Category', pd.Grouper(key='date', freq='W-MON')])['status'].agg(['sum','count']).reset_index()

output_df['percent']=(output_df['sum']/output_df['count'])*100

output_df


data_with_cutoff['date'] = pd.to_datetime(data_with_cutoff['date']) - pd.to_timedelta(7, unit='d')
data_with_cutoff.groupby(['Category', pd.Grouper(key='date', freq='W-MON')])['status'].count()

