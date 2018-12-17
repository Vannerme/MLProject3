#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Load packages
import urllib2, sys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')



# In[2]:


# Identify the URL of the Website to scrape
site = "http://www.loc.gov/standards/iso639-2/php/code_list.php"

hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)


# In[3]:


#Let's grab the column headers from the table. 
#In this case, the headers start in row 1 (hence limit 1)
column_headers = [th.getText() for th in 
                  soup.findAll('tr', limit=1)[0].findAll('th')]
print column_headers


# In[4]:


#Now let's get the data to fill in the table. 
#The data is table format so a 2 dimensional list is needed. 
#Use 2: to skip the first row (headers)
data_rows = soup.findAll('tr')[2:]  


# In[5]:


# now we have a list of table rows
print type(data_rows)  


# In[6]:


#Now we combine the column_header list with the data_row list
lang_cd = [[td.getText() for td in data_rows[i].findAll(['td','th'])] for i in range(len(data_rows))] 


# In[7]:


# Create an empty list to hold all the data
langcd_ls = []


# In[8]:


# Now pass the list to the empty list
for i in range(len(data_rows)):  # for each table row
    code_row = []  # create an empty list for each pick/player

    # for each table data element from each table row
    for td in data_rows[i].findAll('td'):        
        # get the text content and append to the player_row 
        code_row.append(td.getText())        

    # then append each pick/player to the player_data matrix
    langcd_ls.append(code_row)

print lang_cd == langcd_ls


# In[9]:


#Now we can create the data frame named df for the data extracted from the Website

lang_df = pd.DataFrame(lang_cd, columns=column_headers)


# In[10]:


lang_df.head()


# In[ ]:

pd.concat([pd.Series(row
                     ['ISO 639-1 Code'],
            ['English name of Language'],
            ['French name of Language'],
            ['German name of Language'], 
    row['ISO 639-2 Code'].split(')'))              
                    for _, row in lang_df.iterrows()]).reset_index()





# In[11]:


#Finally, save the dataframe as a CSV
lang_df.to_csv("C:\Users\Jon\Desktop", index=False)

