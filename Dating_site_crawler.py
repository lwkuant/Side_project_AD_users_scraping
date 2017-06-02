# -*- coding: utf-8 -*-
"""
AD crawler
"""

### data until 2017/5/14
### There are 2001 pages
final = 2001

### load required packages
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import collections
import re
import shutil

### change the current directory
import os
print(os.getcwd())
os.chdir(r'D:\Dataset\AD_scraped')
print(os.getcwd())

### login setting
header = {'Accept':'xxx', 
          'Accept-Encoding':'xxx', 
          'Accept-Language':'xxx', 
          'Connection':'xxx', 
          'Cookie':'xxx', 
          'Host':'xxx', 
          'Origin':'xxx', 
          'Referer':'xxx', 
          'Upgrade-Insecure-Requests':'xxx',
          'User-Agent':'xxx'}

log_url = 'xxx'
email = 'xxx'
password = 'xxx'

### Login
session = requests.Session()
session.post(log_url, {'email':email, 'password':password}, headers=header)

### the data container
profile_dict = {}
#count = 0
id_by_time = []

### Start scraping
url = 'xxx'

#col = ['Membership', 'Name', 'Country', 'City', 'Language', 'Age', 'Height',
#       'Shape', 'Job', 'Eye_color', 'Hair_color', 'Race', 'Education', 'Marital_status',
#       'Smoking', 'Alcohol', 'About_me', 'Budget_type', 'Ideal_daddy', 'Default_picture']

col = ['會員狀態', '暱稱', '國家', '城市', '習慣語系', '年齡', '身高', '體型', '職業', '眼睛顏色',
       '頭髮顏色', '種族', '教育程度', '婚姻狀態', '吸煙習慣', '飲酒習慣', '關於我',
       '零用錢預算', '描述您理想中的約會對象', 'Default_picture']

start_time = time.time()

for ind in range(1, final):
    
    ## get the link
    print('Page:', ind)
    link = session.get(url+str(ind))
    link.encoding = 'utf-8'
    
    page = BeautifulSoup(link.text)
    
    profile_link = page.findAll('a', {'target':'_blank', 'href':re.compile(r'http:\/\/xxx\.com\/xxx-xxx\/.+')})
    profile_link = [link.attrs['href'] for link in profile_link]
    id_by_time.extend([re.findall(r'\d+', link)[0] for link in profile_link])
    
    ## scrap each link on the page 
    for profile in profile_link:
        page = session.get(profile)
        page.encoding = 'utf-8'
        page = BeautifulSoup(page.text)

        Id = re.findall(r'\d+', profile)[0]
        
        info_list = []
        
        try:
            ## get user information
            basic_info = page.findAll('div', {'class':'member_set'})
            
            ## get membership type
            info_list.append(basic_info[0].find('p').get_text())
            
            ## get the second to 16th information
            basic_info_tmp = basic_info[1].findAll('li')
            
            check = 0
            for i in range(1, 17):
                if basic_info_tmp[check].get_text().strip()[:basic_info_tmp[check].get_text().strip().find('：')] != col[i]:
                    info_list.append('NA')
                else:
                    if i == 16:
                        info_list.append(re.sub(r'<.*?>', ' ', str(basic_info_tmp[check])).strip()[6:])
                    else:
                        info_list.append(basic_info_tmp[check].get_text().strip()[basic_info_tmp[check].get_text().strip().find('：')+1: ])
                        check+=1
                        
            ## get budget info
            try:
                info_list.append(basic_info[2].findAll('span')[1].get_text())
            except:
                info_list.append('NA')
            
            ## get ideal daddy
            try:
                info_list.append(re.sub(r'<.*?>', ' ', str(basic_info[2].findAll('span')[2])).strip())
            except:
                info_list.append('NA')
                
            ## get picture type
            pic = page.find('div', {'class':'member_photo clearfix tc'}).find('img')['src']
            if 'def_f2' in pic:
                info_list.append('1')
            else:
                info_list.append('0')
                
                ## get the profile picture
                request_pic = requests.get(pic, stream=True)
                file = open(Id+'.jpg', 'wb')
                shutil.copyfileobj(request_pic.raw, file)
                file.close()
                del request_pic
            
        except:
            print('Error!')
            
        profile_dict[Id] = dict(zip(col, info_list))
        
        
    ## pause for some time 
    print(profile_dict[id_by_time[-1]])
    time.sleep(3)
            
print('Execution time:', (time.time() - start_time))      
# 11087 seconds for 2000 pages 
# Finally get 19985 profiles
# 15 profiles may contain errors
#