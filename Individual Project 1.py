#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
import re


# # 1.2.a.Use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

# In[35]:


def getpageinfo():
    try:
        headers ={'User-Agent': "Mozilla/5.0"}

        url='https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1'

        response = requests.get(url=url, headers = headers)

        page_content = response.content
        print(page_content)

        filename1='amazon_gift_card_01.htm'.format()
        with open(filename1,'wb') as fp:
                fp.write(page_content) 
                
                fp.close()
    except:
        print("Problem with the connection...")


# In[36]:


if __name__ == '__main__':
    getpageinfo()


# # 1.2.b.Take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

# In[37]:


def getpages():
    try:
        url='https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1'  


        for _pgn in range(1,10):
            url_list = url+ '&_pgn='+str(_pgn)
            headers ={'User-Agent': "Mozilla/5.0"}


            page_content = requests.get(url=url_list, headers = headers).content
            
            filename2="amazon_gift_card_{:02d}.html".format(_pgn)
            _pgn += 1
            with open(filename2,'wb') as fp:
                fp.write(page_content) 
                fp.close()
        
                time.sleep(10)
        return(filename2)
            
    except:
        print("Problem with the connection...")


# In[38]:


if __name__ == '__main__':
    getpages()


# # 1.2.c.Write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.
# 

# In[124]:


def inpages():
    try:
        filename2 = getpages()
    
        with open(filename2,'r',encoding = 'utf-8') as file:
        
            content = file.read()
            soup = BeautifulSoup(content,'html.parser')
            
        return(soup)
    except:
        print("Problem with the connection...")
    


# # 1.2.d.Using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

# In[39]:


def listprice():
    try:
        Title = []
        Price = []
        shipping_price_list = []
        for _pgn in range (1,11):
            filename2 = "amazon_gift_card_{:02d}.html".format(_pgn)
    
            with open(filename2,'r',encoding = 'utf-8') as file:
        
                content = file.read()
                soup = BeautifulSoup(content,'html.parser')      
        

                items = soup.find_all("div", class_="s-item__info clearfix")
            # Extract the title and price for each item
            #and list them into column matirxs
                for item in items:
                    title = item.find("div", class_="s-item__title")
            
                    for title_ in title:
                        title_ = title_.text
                        title_ = title_.replace('New Listing','').strip()
                        Title.append(title_)
                        price = item.find("span", class_="s-item__price").text
                        Price.append(price)
                  
                for ship in items:
                    ship_price = ship.find('span', class_ = 's-item__shipping s-item__logisticsCost')
                    if ship_price is None:
                        shipping_price_list.append('Free shipping')
                            
                    else:
                        shipping_price_list.append(ship_price.text)
                            
            
            dfTitle = pd.DataFrame(Title)
            dfPrice = pd.DataFrame(Price)
            dfShipping = pd.DataFrame(shipping_price_list)
        
            df1 = pd.concat([dfTitle,dfPrice],axis=1)
            dfDetails = pd.concat([df1,dfShipping],axis=1)
            
        print(dfDetails)
        return(items)
        
    except:
        print("Problem with the connection...")
        


# In[40]:


if __name__ == '__main__':
    listprice()


# # 1.2.e.Using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

# In[224]:


for _pgn in range (1,11):
    filename2 = "amazon_gift_card_{:02d}.html".format(_pgn)
    
    with open(filename2,'r',encoding = 'utf-8') as file:
        
        content = file.read()
        soup = BeautifulSoup(content,'html.parser')      
        
#     def listsoldinfo(soup):
        items = soup.find_all("div", class_="s-item__info clearfix")
            # Extract the title and price for each item
            #and list them into column matirxs
        Title = []
        Price = []
        shipping_price_list = []
        for _pgn in range (1,11):
            filename2 = "amazon_gift_card_{:02d}.html".format(_pgn)
    
            with open(filename2,'r',encoding = 'utf-8') as file:
        
                content = file.read()
                soup = BeautifulSoup(content,'html.parser')      
        

                items = soup.find_all("div", class_="s-item__info clearfix")
            # Extract the title and price for each item
            #and list them into column matirxs
                for item in items:
                    title = item.find("div", class_="s-item__title")
            
                    for title_ in title:
                        title_ = title_.text
                        title_ = title_.replace('New Listing','').strip()
                        Title.append(title_)
                        price = item.find("span", class_="s-item__price").text
                        Price.append(price)
                  
                for ship in items:
                    ship_price = ship.find('span', class_ = 's-item__shipping s-item__logisticsCost')
                    if ship_price is None:
                        shipping_price_list.append('Free shipping')
                            
                    else:
                        shipping_price_list.append(ship_price.text)
                            

            dfPrice = pd.DataFrame(Price)
    

        piT = []
        for titles in Title:
            priceInTitle = re.findall(r".?(\d+).*?", titles)
            if priceInTitle is None:
                priceInTitle = 0
                piT.append(priceInTitle)
            else:
                for i in priceInTitle:
                    i = int(i)
                piT.append(i)
        

        piS = []    
        for shipps in shipping_price_list:
            if shipps == "Free shipping":
                shipps = 0
                piS.append(shipps)
            else:
                shipps = re.findall(r".?(\d+\.\d{0,2}).*?", shipps)
                for i in shipps:
                    i = float(i)
                piS.append(i)

        
        piS = pd.DataFrame(piS)
        piT = pd.DataFrame(piT)
        dfCombine1 = pd.concat([piT,piS],axis=1)
        dfCombined = pd.concat([dfCombine1,dfPrice],axis=1)
        

        dfCombined.columns = ['title','shipping','price']
        dfCombined['price'] = dfCombined['price'].apply(lambda x: pd.np.nan if "to" in str(x) else x)
        dfCombined['price'] = dfCombined['price'].str.strip('$')
        dfCombined['price'] = dfCombined['price'].astype(float)
print(dfCombined)


dfsells_above_face_value= dfCombined['price'] + dfCombined['shipping'] - dfCombined['title'] 
print(dfsells_above_face_value)
print((dfsells_above_face_value>0).sum())


# # 1.2.f.What fraction of Amazon gift cards sells above face value? Why do you think this is the case?

# In[225]:


p = (dfsells_above_face_value>0).sum()
print(p)
n =len(dfsells_above_face_value)
print(n)
print(p/n)


# # 2.2.a

# In[1]:


from bs4 import BeautifulSoup
import requests
import time

URL = "https://www.fctables.com/user/login/"
page1 = requests.get(URL)     
        
       
time.sleep(5); 
session_requests = requests.session()      
res = session_requests.post(URL, 
                                data = {"referer" : "https://www.fctables.com/",
                                  "login_action" : "1",
                                  "login_username": "oscarhui9525@gmail.com",
                                  "login_password" : "Xjr19980729!",
                                  "user_remeber" : "1",
                                  "submit" : "1"},
                                  headers = dict(referer = "https://www.fctables.com/"),
                                  timeout = 15)
                                  
print(res.text)


# # 2.2.b

# In[4]:


URL = "https://www.fctables.com/tipster/my_bets/"
cookies = session_requests.cookies.get_dict()
page2 = session_requests.get(URL,  cookies = cookies)
# print(page2.text)
if 'wolfsburg'  in page2.text:
    print("I found my bet")
else:
    print("Error")
    

