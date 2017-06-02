# -*- coding: utf-8 -*-
"""
This is the analysis part of the "Dating site users scraping side project"
"""

###
### Data processing
###

# \r in the text should be removed 

import pandas as pd 
import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 
%matplotlib inline 
import seaborn as sns 
import re

df = pd.DataFrame(profile_dict)
df = df.T
print(df.head())

### change the orders of the columns 
df = df.copy().ix[:, col]
print(df.head())
    
### rename the column names in English 
col_eng = ['Membership', 'Name', 'Country', 'City', 'Language_used', 'Age', 'Height',
       'Shape', 'Job', 'Eye_color', 'Hair_color', 'Race', 'Education', 'Marital_status',
       'Smoking', 'Alcohol', 'About_me', 'Budget_type', 'Ideal_daddy', 'Default_picture']

df.columns = col_eng
print(df.head())

### remove the profiles that were not scraped
missed_profiles = np.setdiff1d(id_by_time, list(df.index)) # weird?
print(len(np.unique(id_by_time))) # the number of unique values is 19985

ind = pd.Series(id_by_time).isin(list(df.index))
len(np.array(id_by_time)[ind]) # 20000, which means that some values are duplicate

### Order the dataframe by the time of appearance (new to old)
df = df.copy().ix[id_by_time, :]
print(df.shape)
print(df.head())

### Drop the duplicate values
df['Id'] = list(df.index)
df = df.drop_duplicates(subset=['Id'])
print(df.shape)
print(df.head())

### Remove the \r from the texts
df['Name'] = df['Name'].astype(str)
df['About_me'] = df['About_me'].astype(str)
df['Ideal_daddy'] = df['Ideal_daddy'].astype(str)

df['Name'] = df['Name'].apply(lambda x: re.sub('\r', ' ', x))
df['About_me'] = df['About_me'].apply(lambda x: re.sub('\r', ' ', x))
df['Ideal_daddy'] = df['Ideal_daddy'].apply(lambda x: re.sub('\r', ' ', x))

###
df.to_csv('profile.csv')

###
### Data analysis
###

import os
print(os.getcwd())
os.chdir(r'D:\Dataset\Dating_site_scraping_data')

import pandas as pd 
import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 
%matplotlib inline 
import seaborn as sns 
import re

df = pd.read_csv('profile.csv', encoding='utf-8', index_col=False, na_values='NA')
df.head()
df.info()

os.chdir(r'D:\Project\Side_project_Dating_site_users_scraping')

### Remove the first column
df.drop(['Unnamed: 0'], axis = 1, inplace=True)
df.info()

### Remove the examples with NA in Membership
df = df.ix[~df['Membership'].isnull(), :]

### Check NAs for each column
np.sum(df.isnull())

plt.figure(figsize=[8, 8])
np.sum(df.isnull()).sort_values().plot.barh(edgecolor='none', color='#ED4144')
plt.title('The Number of NAs in Each Column', fontsize=15)
plt.xlabel('Frequency')

# in ratio
plt.figure(figsize=[12, 8])
(np.sum(df.isnull())*100/len(df)).sort_values().plot.barh(edgecolor='none', color='#ED4144')
plt.title('The Percentage of NAs in Each Column', fontsize=15)
plt.xlabel('Ratio of total data (%)')
plt.savefig('ratio_of_NAs.png', dpi=300)

### The distribution of membership
df['Membership'].value_counts()

df['Membership'].value_counts()*100/(len(df))

import matplotlib.font_manager as fm
myfont = fm.FontProperties(fname='D:/Downloads/Microsoft_JH_6.12/msjh.ttc')

plt.figure(figsize=[15, 8])
ax = (df['Membership'].value_counts()*100/(len(df))).sort_values().plot.barh(edgecolor='none', color='#ED4144')
yticklabel = list((df['Membership'].value_counts()*100/(len(df))).sort_values().index)
ax.set_yticklabels(labels = yticklabel, fontproperties = myfont, size=10)
plt.title('The Distribution of Membership Type (in %)', fontsize=15)
plt.xlabel('Ratio of total data (%)')
plt.savefig('distribution_of_membership.png', dpi=300)

Conversion_rate = np.sum(df['Membership'] == 'VIP 會員')/len(df)*100
# The conversion rate is very low 

### The distribution of Name
df['Name'].value_counts().head(10)

###
df['City'].value_counts()

### 
sns.distplot(df['Age'])
sns.boxplot(df['Age'])


### 
df['Shape'].value_counts()


###
df['Marital_status'].value_counts()
