"""
#THIS CODE IS DEVELOPED BY AND BELONGS TO "SHWETA SHARAD KATKAR" IP-ID:-2502 FOR INTERNSHIP LIVE PROJECT AT CLOUDCOUNSELAGE
#THIS FILE EXTRACTS INFORMATION ABOUT ALMOST ALL ENGINEERING COLLEGES BELONGING TO THREE CITIES".
#THIS CODE IS EXECIUTED IN JUPYTER NOTEBOOK AND THEN DOWNLOADED AS .PY FILE FROM JUPYTER
"""
#!/usr/bin/env python
# coding: utf-8
# In[ ]:
import selenium
from selenium import webdriver
from getpass import getpass
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Login in website using selenium
# In[ ]:
uname=input('username :')
pswd=getpass('Password :')

# In[ ]:
driver= webdriver.Chrome('C:\\Drivers\\WebDriver\\chromedriver.exe')

# In[ ]:
driver.get('https://www.collegesearch.in/student-login.php#')

# In[ ]:
loginpage= driver.find_element_by_xpath('//*[@id="login"]')

# In[ ]:
loginpage.click()

# In[ ]:
username_txtbox= driver.find_element_by_id('student_email')
username_txtbox.send_keys(uname)

# In[ ]:
password_txtbox= driver.find_element_by_id('student_password')
password_txtbox.send_keys(pswd)

# In[ ]:
#login_btn=driver.find_element_by_xpath('//*[@id="student_login_frm"]/div[2]/div/div[5]/input')
login_btn=driver.find_element_by_name('Sign In')
login_btn.text
login_btn.submit()

# In[ ]:
clg_btn=driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/a/div[2]')
clg_btn.text
clg_btn.click()

# In[ ]:
btech_clg_btn=driver.find_element_by_xpath('//*[@id="engineering_cat"]/div/div[1]/div/div/a/div/div[2]')
btech_clg_btn.text
btech_clg_btn.click()

# Extracting all college links in one list or .csv file
# In[ ]:
for page in range(1,300,1):
    page=requests.get('https://www.collegesearch.in/engineering-colleges-india?page={}'.format(page))
    soup= BeautifulSoup(page.content, 'html.parser')
    week=soup.find(id='results')
    items=week.find_all(class_='well mg-5-0 search_result_card')
    
    for item in items:
        clist.append(item.find(class_='media-heading mg-0').find('a').attrs['href'])

# In[ ]:
clg_details1=pd.DataFrame({

    'Contact Links': clist
})

clg_details1.to_csv('clg__list.csv')
# In[ ]:

# clist=[]
# c=pd.read_csv('clg__list.csv')
# clist=c['Contact Links']
# print(len(clist))

# In[ ]:
# Extracting details of each college
# In[ ]:
MobileNos=[[] for i in range(2992)]
Websites=[[] for i in range(2992)]
Emails=[[] for i in range(2992)]
Address=[[] for i in range(2992)]
ClgNames=[[] for i in range(2992)]
TPOnames=[[] for i in range(2992)]
TPOContactnos=[[] for i in range(2992)]
TPOEmails=[[] for i in range(2992)]
State=[[] for i in range(2992)]
City=[[] for i in range(2992)]
Companies=[[] for i in range(2992)]

# In[ ]:
for i in range(0,2992):
    driver.get(clist[i])
    pg=requests.get(clist[i])
    sp= BeautifulSoup(pg.content, 'html.parser')
    
    try:
        clg_div=driver.find_elements_by_tag_name('h1')[0].text
        clglists=clg_div.split('\n')
        ClgNames[i]=clglists[0].strip()
        
        loc=clglists[1].split(',')
        City[i]=loc[0].strip()
        State[i]=loc[1].strip()
    except:
        pass
    
    try:
        MobileNos[i]=driver.find_element_by_xpath('//*[@id="contactDiv"]/div[1]/div[2]/span').text.strip()
    except:
        pass
    try:
        Emails[i]=driver.find_element_by_xpath('//*[@id="contactDiv"]/div[2]/div[2]/span').text.strip()
    except:
        pass
    try:
        Websites[i]=driver.find_element_by_xpath('//*[@id="contactDiv"]/div[3]/div[2]/span/a').text.strip()
    except:
        pass
    try:
        Address[i]=driver.find_element_by_xpath('//*[@id="contact"]/div/div[1]/div[2]/div[2]').text.strip()
    except:
        pass
#     try:
#         TPOnames[i]=driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[5]/div/div[1]/div[19]/div[1]/div[2]/div[1]').text.strip()
#     except:
#         pass
#     try:
#         TPOContactnos[i]=driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[5]/div/div[1]/div[19]/div[1]/div[2]/div[2]').text.strip()
#     except:
#         pass
#     try:
#         TPOEmails[i]=driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[5]/div/div[1]/div[19]/div[1]/div[2]/div[3]').text.strip()
#     except:
#         pass
    try:
        wk=sp.find(class_='col-xs-10 colmd-11')
    except:
        pass
    try:
        TPOnames[i]=wk.find(class_="col-md-4 col-xs-12").get_text().strip()
    except:
        pass
    try:
        TPOContactnos[i]=wk.find(class_='col-xs-12 col-md-3').get_text().strip()
    except:
        pass
    try:
        TPOEmails[i]=wk.find(class_='col-xs-12 col-md-4').get_text().strip()
    except:
        pass
    print(i)

# In[ ]:
#Extracting city and state names from address of each college
for i in range(0,2992):
    if State[i]=='[]':  # or []
        State[i]=City[i]
        City[i]=[]
        print(i)
    
for i in range(0,2992):
    try:
        if City[i]=='[]': # or []
            lst=str(Address[i]).split(',')
            City[i]=lst[-2].strip()
    except:
        pass

# In[ ]:
#Handle error1
#Shifting Websites names of Email list into website list
for i in range(0,2992):
    if ("http" in Emails[i]  or "www" in Emails[i]) and "@" not in Emails[i]:
        Websites[i]=Emails[i]
        Emails[i]=[]
        print(Emails[i])

# In[ ]:
#Handle error2
#Shifting Emails names in telephone no. list into Emails list
for i in range(0,2992):
    if "@" in MobileNos[i]:
        Emails[i]=MobileNos[i]
        MobileNos[i]=[]
        print(MobileNos[i])

# In[ ]:
#Handle error3
#Shifting websites in telephone no. list into website list

for i in range(0,2992):
    if "http" in MobileNos[i] or "www" in MobileNos[i]:
        Websites[i]=MobileNos[i]
        MobileNos[i]=[]
        print(MobileNos[i])

# In[ ]:
#Handle error3
for i in range(0,2992):
    if MobileNos[i]=='[]' and Emails[i]=='[]' and TPOContactnos[i]=='[]' and TPOEmails[i]=='[]':
        Emails.pop(i)
        MobileNos.pop(i)
        Websites.pop(i)
        ClgNames.pop(i)
        State.pop(i)
        City.pop(i)
        Address.pop(i)
        TPOnames.pop(i)
        TPOContactnos.pop(i)
        TPOEmails.pop(i)
        print(i)

# Export data in .csv file
# In[ ]:
data=pd.DataFrame({
    'College Name': ClgNames,
    'State': State,
    'City': City,
    'Telephone No.': MobileNos,
    'Email ID':Emails,
    'Website':Websites,
    'Address':Address,
    'TPO Name': TPOnames,
    'TPO Mobile No.': TPOContactnos,
    'TPO Email ID': TPOEmails
})
data.to_csv('scrapped_data_final.csv')

# Data visualization
# In[ ]:
clg=pd.read_csv('scrapped_data_final.csv',index=False)
email=clg['Email ID']
mob=clg['Telephone No.']
web=clg['Website']
cname=clg['College Name']
state=clg['State']
city=clg['City']
add=clg['Address']
tname=clg['TPO Name']
tmob=clg['TPO Mobile No.']
temail=clg['TPO Email ID']

# In[ ]:
get_ipython().run_line_magic('matplotlib', 'inline')

# In[ ]:
d=Counter(state)
d.pop("[]")

# In[ ]:
plt.style.use('seaborn')
fig, ax=plt.subplots(figsize=(50,40),tight_layout=True)
ax.bar(d.keys(),d.values(),align='center', width=0.9);
ax.set_title('Data visualization', fontsize=50)
ax.set_xlabel('State', fontsize='medium')
ax.set_ylabel('No. Of Colleges', fontsize='medium')
ax.tick_params(axis='both', rotation=70,labelsize=40)
plt.savefig('State.png')


# In[ ]:
g=Counter(city)
g.pop("[]")

for i in list(g):
    if g.get(i)<5:
        g.pop(i)
# x=list(f)
# y=list(d.values())


# In[ ]:
x = np.arange(len(g.keys()))
plt.style.use('seaborn')
fig1, ax1=plt.subplots(figsize=(150,80))
ax1.bar(x,g.values(),align='edge',width=0.9)
ax1.set_title('Data visualization', fontsize=100,fontweight='bold')
ax1.set_xlabel('District', fontsize=100)
ax1.tick_params(axis='both', rotation=80,labelsize=60)
plt.xticks(x, g.keys())
plt.xlim(0, 121) 
plt.ylim(0, 110) 
plt.savefig('District.png')
