#!/usr/bin/env python
# coding: utf-8

# (2)  Using Python or Java, write code that uses Selenium to access the URL from (1), click on each of the top-8 most expensive Bored Apes, and store the resulting details page to disk, “bayc_[N].htm” (replace [N] with the ape number).

# In[247]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import re
import time
import json
import pymongo


# In[1037]:


#use driver
driver = webdriver.Chrome(executable_path = '/Users/oscarhui/Desktop/422/HW4/chromedriver')
driver.implicitly_wait(5)
driver.set_script_timeout(5)
driver.set_page_load_timeout(5)


# In[1047]:


def q2():
    try:
        driver = webdriver.Chrome(executable_path = '/Users/oscarhui/Desktop/422/HW4/chromedriver')
        driver.implicitly_wait(5)
        driver.set_script_timeout(5)
        driver.set_page_load_timeout(5)
        URL = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold"
        user_agent = {'User-agent': 'Mozilla/5.0'} 
        driver.get(URL);
        # driver.find_element

        time.sleep(10)

        href_list=[]
        elems = driver.find_elements(By.XPATH,"//a[@href]")
        for elem in elems:
            href_list.append(elem.get_attribute("href"))
        # print(href_list)
        r = re.compile(".*[0-9a-z]{42}/\d{3,4}$")
        item_href_list = list(filter(r.match, href_list)) # Read Note below
        # print(item_href_list)
        global ape_numbers
        ape_numbers = []

        for href in item_href_list[0:8]:
            driver.get(href)
        
            nub = re.findall(r"\b[0-9]{3,4}\b",href)
#             ape_numbers.append(nub)
            with open(f'./bayc_{int(nub[0])}.htm','w')as f:
                f.write(driver.page_source)
#             print(nub)
            ape_numbers.append(nub)
            time.sleep(5)
        print(ape_numbers)
        return(ape_numbers)
    except Exception as ex:
        print("Error:" + str(ex))

q2()


# In[1040]:



def q3():
    try:
        ape_numbers_value = [value[0] for value in ape_numbers]
        # print(ape_numbers_value)
        url_list = item_href_list[0:8]
        names = []
        background =[]
        clothes = []
        earring = []
        eyes = []
        fur = []
        hat = []
        mouth = []
        for j in ape_numbers_value:
            file = f"bayc_{int(j)}.htm"
        
            with open(file,"r",encoding='utf-8') as f:
                page = f.read()

            doc = BeautifulSoup(page,'html.parser')
            ape_name = doc.find("h1", class_="sc-29427738-0 hKCSVX item--title").text
            names.append(ape_name)
            attribute_text = doc.find_all("div",class_="Panel--isContentPadded item--properties")[0].text
            
            for i in range(0,6):
                type_text = doc.find_all("div",class_="Property--type")[i].text
#                 print(type_text)
                value = doc.find_all("div",class_="Property--value")[i].text
#                 print(value)
            
                if i==0: 
                    if type_text is not None:
                        background.append(value)
                    else:
                        background.append("Null")
                    
                elif i==1: 
                    if "Clothes" in attribute_text:
                        clothes.append(value)
                    elif "Clothes" not in attribute_text:
                        clothes.append("Null")
                
                elif i==2: 
                    if "Earring" in attribute_text and "Clothes" in attribute_text:
                        earring.append(value)
                    elif "Earring" in attribute_text and "Clothes" not in attribute_text:
                        earring.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" not in attribute_text:
                        earring.append("Null")
                        
                elif i==3: 
                    if "Earring" in attribute_text and "Clothes" in attribute_text:
                        eyes.append(value)
                    elif "Clothes" not in attribute_text and "Earring" in attribute_text:
                        eyes.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" not in attribute_text and "Clothes" in attribute_text:
                        eyes.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" and "Clothes" not in attribute_text:
                        eyes.append(doc.find_all("div",class_="Property--value")[i-2].text)
                    

                elif i==4: 
                    if "Earring" in attribute_text and "Clothes" in attribute_text:
                        fur.append(value)
                    elif "Clothes" not in attribute_text and "Earring" in attribute_text:
                        fur.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" not in attribute_text and "Clothes" in attribute_text:
                        fur.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" and "Clothes" not in attribute_text:
                        fur.append(doc.find_all("div",class_="Property--value")[i-2].text)
                    

                elif i==5: 
                    if "Earring" in attribute_text and "Clothes" in attribute_text:
                        hat.append(value)
                    elif "Clothes" not in attribute_text and "Earring" in attribute_text:
                        hat.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" not in attribute_text and "Clothes" in attribute_text:
                        hat.append(doc.find_all("div",class_="Property--value")[i-1].text)
                    elif "Earring" and "Clothes" not in attribute_text:
                        hat.append(doc.find_all("div",class_="Property--value")[i-2].text)
            mouth.append(doc.find_all("div",class_="Property--value")[-1].text)
                    
            
            
        print(names)
        print(url_list)

        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongo_client["422_individual_project2"]
        collection_bayc = db["bayc"]
        collection_bayc.drop()
        apes = [[url_list[i], names[i],background[i],clothes[i],earring[i],eyes[i],fur[i],hat[i],mouth[i]] for i in range(len(url_list))]
        for ape in apes:
            
            
            dictionary_ape = {'url':ape[0],'name': ape[1],'background': ape[2], 'clothes':ape[3] ,'earring': ape[4],
                              'eyes':ape[5],'fur':ape[6], 'hat':ape[7],'mouth':ape[8]}
            
            print(dictionary_ape)
            collection_bayc.insert_one(dictionary_ape)

    except Exception as ex:
        print("Error:" + str(ex))
q3()
    


# In[1060]:


def q4():
    try:
        #Open the file for writing the html
        URL = "https://www.yellowpages.com/search"
        #Setup the URL and etc.
        user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'} 
        params = {'search_terms':'Pizzeria','geo_location_terms':'San Francisco, CA'}
        page = requests.get(URL, headers=user_agent, params = params)
        print(page)
        #Create a beautifulsoup object
        web = BeautifulSoup(page.content, "html.parser")
        file = open('sf_pizzeria_search_page.htm',"w")
        #Write the content into the html file
        file.write(str(web))
        
        #Close the file
        file.close()
        
    except Exception as ex:
        print('Error: ' + str(ex))

q4()


# In[1083]:


def q5():
    try:
        with open('sf_pizzeria_search_page.htm','r', encoding='utf-8') as f:
            page = f.read()

        #soup the full search page result
        full_page_doc = BeautifulSoup(page,'html.parser')
        #seperate the ad and list list the non-ad content
        non_ad_main_content = full_page_doc.find("div", class_ = "search-results organic")

        #create empty lists to store in features:
        i = 1
        ranks = []
        names = []
        urls = []
        star_rates = []
        no_reviews = []
        TA_rates = []
        TA_counts = []
        price_ranges =[]
        years = []
        reviews = []
        amenities = []

        URL_1 = "https://www.yellowpages.com"
        #find all info
        infos = non_ad_main_content.find_all("div",class_ = "info")
        links = non_ad_main_content.find_all("a",class_ = "business-name")
        for link in links:
            URL_2 = link.get('href')
#             print(URL_2)
            #Combine the root of URL and rest part together
            URL_Final = URL_1 + URL_2
#             print(URL_Final)
            urls.append(URL_Final)
        for info in infos:
            ranks.append(i)
            i += 1
            name = info.find('a',class_= "business-name").text
            names.append(name)

            star_rating = info.find('div',class_='result-rating')
            if star_rating is not None:
                rate_value = star_rating.get('class')
                star_rate = rate_value[1:]
                if len(star_rate) == 1:
                    if star_rate[0] == "one" :
                        star_rate = "1"
                    elif star_rate[0] == "two" :
                        star_rate = "2"
                    elif star_rate[0] == "three" :
                        star_rate = "3"
                    elif star_rate[0] == "four" :
                        star_rate = "4"
                    else:
                        star_rate = "5"

                else:
                    if star_rate[0] == "one" :
                        star_rate = "1"
                    elif star_rate[0] == "two" :
                        star_rate = "2"
                    elif star_rate[0] == "three" :
                        star_rate = "3"
                    elif star_rate[0] == "four" :
                        star_rate = "4"
                    else:
                        star_rate = "5"
                    star_rate_half = ".5"
                    star_rate = str(star_rate + star_rate_half)
        #             star_rate = str(star_rate[0] + "." + star_rate[1])
        #         print(type(dollar_sign))
            else:
                star_rate = "Null"
            star_rates.append(star_rate)
        
            count_reviews = info.find('span',class_='count')
            if count_reviews is not None:
                no_review = count_reviews.text
                no_review =  no_review.strip('()') 
            else:
                no_review = "Null"
            no_reviews.append(no_review)


            tripadvisor = info.find('div',{'data-tripadvisor':True})
            if tripadvisor is not None:
                data_ta = tripadvisor.get('data-tripadvisor')
                TA_rating = json.loads(data_ta)["rating"]
                TA_count = json.loads(data_ta)["count"]
            else:
                TA_rating = "Null"
                TA_count = "Null"

            TA_rates.append(TA_rating)
            TA_counts.append(TA_count)


            price_range = info.find('div',class_=('price-range'))
            if price_range is not None:
                dollar_sign = price_range.text
                if dollar_sign == '':
                    dollar_sign = "Null"
                else:
                    dollar_sign = dollar_sign
            else:
                dollar_sign = "Null"
            price_ranges.append(dollar_sign)

            year_in_business = info.find('div',class_= "years-in-business")
            if year_in_business is not None:
                year = year_in_business.text
            else:
                year = "Null"
            years.append(year)

            review_body = info.find('p',class_= "body with-avatar")
            if review_body is not None:
                review = review_body.text
            else:
                review = "Null"
            reviews.append(review)

            amenities_icons = info.find('div',class_= "amenities-info")
            if amenities_icons is not None:
                amenity = amenities_icons.text
            else:
                amenity = "Null"
            amenities.append(amenity)
        print(urls)
        print(ranks)
        print(names)
        print(link)
        print(star_rates)
        print(no_reviews)
        print(TA_rates)
        print(TA_counts)
        print(price_ranges)
        print(years)
        print(reviews)
        print(amenities)
        return(ranks, names, links, star_rates, no_reviews, TA_rates,TA_counts,price_ranges,years,reviews,amenities)
    except Exception as ex:
        print("Error:" + str(ex))
q5()
    
    


# # (6)

# In[1177]:




def q6():
    try:
        
        with open('sf_pizzeria_search_page.htm','r', encoding='utf-8') as f:
            page = f.read()

        #soup the full search page result
        full_page_doc = BeautifulSoup(page,'html.parser')
        #seperate the ad and list list the non-ad content
        non_ad_main_content = full_page_doc.find("div", class_ = "search-results organic")

        #create empty lists to store in features:
        i = 1
        ranks = []
        names = []
        urls = []
        star_rates = []
        no_reviews = []
        TA_rates = []
        TA_counts = []
        price_ranges =[]
        years = []
        reviews = []
        amenities = []

        URL_1 = "https://www.yellowpages.com"
        #find all info
        infos = non_ad_main_content.find_all("div",class_ = "info")
        links = non_ad_main_content.find_all("a",class_ = "business-name")
        for link in links:
            URL_2 = link.get('href')
#             print(URL_2)
            #Combine the root of URL and rest part together
            URL_Final = URL_1 + URL_2
#             print(URL_Final)
            urls.append(URL_Final)
        for info in infos:
            ranks.append(i)
            i += 1
            name = info.find('a',class_= "business-name").text
            names.append(name)

            star_rating = info.find('div',class_='result-rating')
            if star_rating is not None:
                rate_value = star_rating.get('class')
                star_rate = rate_value[1:]
                if len(star_rate) == 1:
                    if star_rate[0] == "one" :
                        star_rate = "1"
                    elif star_rate[0] == "two" :
                        star_rate = "2"
                    elif star_rate[0] == "three" :
                        star_rate = "3"
                    elif star_rate[0] == "four" :
                        star_rate = "4"
                    else:
                        star_rate = "5"

                else:
                    if star_rate[0] == "one" :
                        star_rate = "1"
                    elif star_rate[0] == "two" :
                        star_rate = "2"
                    elif star_rate[0] == "three" :
                        star_rate = "3"
                    elif star_rate[0] == "four" :
                        star_rate = "4"
                    else:
                        star_rate = "5"
                    star_rate_half = ".5"
                    star_rate = str(star_rate + star_rate_half)
        #             star_rate = str(star_rate[0] + "." + star_rate[1])
        #         print(type(dollar_sign))
            else:
                star_rate = "Null"
            star_rates.append(star_rate)
#         print(star_rates)

        for info in infos:
            count_reviews = info.find('span',class_='count')
            if count_reviews is not None:
                no_review = count_reviews.text
                no_review =  no_review.strip('()') 
            else:
                no_review = "Null"
            no_reviews.append(no_review)

            tripadvisor = info.find('div',{'data-tripadvisor':True})
            if tripadvisor is not None:
                data_ta = tripadvisor.get('data-tripadvisor')
                TA_rating = json.loads(data_ta)["rating"]
                TA_count = json.loads(data_ta)["count"]
            else:
                TA_rating = "Null"
                TA_count = "Null"

            TA_rates.append(TA_rating)
            TA_counts.append(TA_count)

            price_range = info.find('div',class_=('price-range'))
            if price_range is not None:
                dollar_sign = price_range.text
                if dollar_sign == '':
                    dollar_sign = "Null"
                else:
                    dollar_sign = dollar_sign
            else:
                dollar_sign = "Null"
            price_ranges.append(dollar_sign)

            year_in_business = info.find('div',class_= "years-in-business")
            if year_in_business is not None:
                year = year_in_business.text
            else:
                year = "Null"
            years.append(year)

            review_body = info.find('p',class_= "body with-avatar")
            if review_body is not None:
                review = review_body.text
            else:
                review = "Null"
            reviews.append(review)

            amenities_icons = info.find('div',class_= "amenities-info")
            if amenities_icons is not None:
                amenity = amenities_icons.text
            else:
                amenity = "Null"
            amenities.append(amenity)

#         return(ranks, names, links, star_rates, no_reviews, TA_rates,TA_counts,price_ranges,years,reviews,amenities)
        print(urls)
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongo_client["422_individual_project2"]
        collection_sf_pizza = db["sf_pizzerias"]

        collection_sf_pizza.drop()

        for i in range(0,30):
            data_list = [{"ranks":ranks[i], "names":names[i], "urls":urls[i],"star_rates":star_rates[i],
                          "no_reviews":no_reviews[i],"TA_rates":TA_rates[i],"TA_counts":TA_counts[i], 
                          "price_ranges":price_ranges[i], "years": years[i],"reviews": reviews[i],"amenities":amenities[i]}]
            collection_sf_pizza.insert_many(data_list)
    except Exception as ex:
        print("Error:" + str(ex))

q6() 


# In[1176]:


def q7():
    try:
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongo_client["422_individual_project2"]
        collection_sf_pizza = db["sf_pizzerias"]
        url_list = collection_sf_pizza.find({},{'urls':1})
        index = 1
        # print(url_list)
        for urls in url_list:
            url = urls["urls"]
            print(url)
            user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'} 

            page = requests.get(url, headers=user_agent)
        #         print(page)
            #Create a beautifulsoup object
            web = BeautifulSoup(page.content, "html.parser")
            filename = "sf_pizzeria_{:d}.htm".format(index)
            index +=1
            file = open(filename,"w")
            #Write the content into the html file
            file.write(str(web))

            #Close the file
            file.close()
    except Exception as ex:
        print("Error:" + str(ex))

q7()
    
        


# In[1130]:


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["422_individual_project2"]
collection_sf_pizza = db["sf_pizzerias"]
url_list = collection_sf_pizza.find({},{'urls':1})
index = 1
# print(url_list)
for urls in url_list:
    url = urls["urls"]
    print(url)
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'} 

    page = requests.get(url, headers=user_agent)
#         print(page)
    #Create a beautifulsoup object
    web = BeautifulSoup(page.content, "html.parser")
    filename = "sf_pizzeria_{:d}.htm".format(index)
    index +=1
    file = open(filename,"w")
    #Write the content into the html file
    file.write(str(web))

    #Close the file
    file.close()
    
    
    
#     file = open(filename,"w")
        
#         #Setup the URL and etc.
#         user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'} 
#         page = requests.get(html, headers=user_agent)
        
#         #Create a beautifulsoup object
#         web = BeautifulSoup(page.content, "html.parser")
        
#         #Write the content into the html file
#         file.write(str(web))
        
#         #Close the file
#         file.close()


# In[1132]:


def q8():
    try:

        address_list = []
        phone_number_list = []
        website_list = []

        for i in range (1,30):
            file = f"sf_pizzeria_{i}.htm"
            with open(file,"r",encoding='utf-8') as f:
                page = f.read()

            doc = BeautifulSoup(page,'html.parser')

            address = doc.find("span", class_="address").text
            phone_number = doc.find("a", class_= "phone dockable").text

            website = doc.find("a", class_="website-link dockable")
            if website is not None:
                website = website.get("href")
                if website is None:
                    website = "Null"
                else:
                    website 
            else:
                website = "Null"

            address = address.replace('San Francisco', ', SF')
            address = address.replace('san francisco', ', SF')
            address_list.append(address)
            phone_number_list.append(phone_number)
            website_list.append(website)
        print(address_list)
        print(phone_number_list)
        print(website_list)
    except Exception as ex:
        print("Error:" + str(ex))
q8()


# # 9
# 

# In[1181]:


def q9():
    try:
        
        address_list = []
        phone_number_list = []
        website_list = []
        index = 1
        for i in range(1,31):
            file = f"sf_pizzeria_{i}.htm"

            with open(file,"r",encoding='utf-8') as f:
                page = f.read()

            doc = BeautifulSoup(page,'html.parser')

            address = doc.find("span", class_="address").text
            phone_number = doc.find("a", class_= "phone dockable").text

            website = doc.find("a", class_="website-link dockable")
            if website is not None:
                website = website.get("href")
                if website is None:
                    website = "Null"
                else:
                    website 
            else:
                website = "Null"

            address = address.replace('San Francisco', ', SF')
            address = address.replace('san francisco', ', SF')
            address_list.append(address)
            phone_number_list.append(phone_number)
            website_list.append(website)
        print(address_list)
        api_http = "https://api.positionstack.com/v1/forward?"
        access_key = "8f3d48207770be39a3658c3f087c6ce3"
        geo_list = []
        # longitude_list = []
        for i in range(0,30):
            para = {"access_key":access_key,"query":address_list[i]}
            api_web = requests.get(url = api_http,headers = user_agent, params = para)
        #     print(api_web.text)

            api_text = json.loads(api_web.text)
        #     print(api_text)
            latitude = api_text['data'][0]["latitude"]
            longitude = api_text['data'][0]["longitude"]
            geo_list.append(str(latitude) + ',' + str(longitude))
        # print(geo_list)

        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongo_client["422_individual_project2"]
        collection_sf_pizza = db["sf_pizzerias"]

        address_list
        for i in range(0,30):

        #     data_list = {"ranks":i+1},{"address":address_list[i],"phone_number":phone_number_list[i],"website":website_list[i],"geolocation":geo_list[i]}
            collection_sf_pizza.update_many({"ranks":i+1},{'$set':{"address":address_list[i],"phone_number":phone_number_list[i],"website":website_list[i],"geolocation":geo_list[i]}})


#         mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
#         db = mongo_client["422_individual_project2"]
#         collection_sf_pizza = db["sf_pizzerias"]
#         collection_sf_pizza.drop()

#         for i in range(0,30):
#             data_list = [{"ranks":ranks[i], "names":names[i], "urls":urls[i],"star_rates":star_rates[i],
#                           "no_reviews":no_reviews[i],"TA_rates":TA_rates[i],"TA_counts":TA_counts[i], 
#                           "price_ranges":price_ranges[i], "years": years[i],"reviews": reviews[i],"amenities":amenities[i],
#                           "address":address_list[i],"phone_number":phone_number_list[i],"website":website_list[i],"geolocation":geo_list[i]}]
#             collection_sf_pizza.insert_many(data_list)
    except Exception as ex:
        print("Error:" + str(ex))
        q9()
q9()      
        


# In[1180]:


q2()
q3()
q4()
q5()
q6()
q7()
q8()
q9()

