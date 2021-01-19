from bs4 import BeautifulSoup
import urllib,os,urllib.request,re,sys
from xml.dom import minidom
import csv
# parse an xml file by name
mydoc = minidom.parse('sitemap-1500099-en_IN-hotel_review-1588271354.xml')
locs = mydoc.getElementsByTagName('loc')
quotes=[]
filename = 'data.csv'
with open(filename, 'w', newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,['Continent','Country','City','Name','Firm','Amenities','Price','Rating','Review'])

    w.writeheader()

    c=0
    for elem in locs:
        print(c)
        c=c+1
        quote = {}
        # print("---------")
        # print(elem.firstChild.data)
        hotel_site_URL=elem.firstChild.data
        #hotel_URL='https://www.tripadvisor.in/'
        hotel_site=urllib.request.urlopen(hotel_site_URL)
        #getting the entire data
        data=hotel_site.read()
        hotel_site.close()
        #creating a soup
        html_soup=BeautifulSoup(data,"html.parser")
        #finding all the hotel cards
        
        hotel_continent=''
        hotel_country=''
        hotel_city=''
        location_thread=html_soup.find("ul",{"class":"breadcrumbs"})
        if(location_thread!=None):
            locations=location_thread.findAll("li",{"class":"breadcrumb"})

            if(locations!=None):

                hotel_continent=locations[0].a.span.text
                hotel_country=locations[1].a.span.text
                hotel_city=locations[2].a.span.text
                quote['Continent']=hotel_continent
                quote['Country']=hotel_country
                quote['City']=hotel_city
                
        
        hotel_name=''
        hotel_name=html_soup.find("h1",{"class":"_1mTlpMC3"}).text
        quote['Name']=hotel_name
        hotel_booking=html_soup.find("div",{"class":"ui_column _1EtJ-1tF"})
        hotel_b_firm=''
        if(hotel_booking!= None):
           if(hotel_booking.find("img",{"class":"Vjc6RdcL"})!=None):
               hotel_b_firm=hotel_booking.find("img",{"class":"Vjc6RdcL"}).attrs['alt'] #hotel booking firm
               quote['Firm']=hotel_b_firm
        else:
            quote['Firm']=''
        str1=''
        hotel_cur_price=html_soup.find("div",{"class":"CEf5oHnZ"})
        if(hotel_cur_price!=None):
            str1=hotel_cur_price.text.replace("\u20b9", " ")

            quote['Price']=str1
        else:
            quote['Price']=''
        hotel_amenities=[]
        amenities=html_soup.find("div",{"class":"_1nAmDotd"})

        stramt=''
        if(amenities!=None):
            amenities_list=amenities.findAll("div")
            
            for amt in amenities_list:
               hotel_amenities.append(amt.text)

            stramt = ','.join(hotel_amenities)
            quote['Amenities']=stramt
        rating=html_soup.find("span",{"class":"_3cjYfwwQ"})
        if(rating!=None):
            quote['Rating']=rating.text
        else:
            quote['Rating']=''
        review=''
        reviews=html_soup.find("div",{"class":"_2wrUUKlw _3hFEdNs8"})
        if(reviews!=None):
            review=reviews.find("div",{"class":"_3hDPbqWO"}).div.div.q.span.text
        quote['Review']=review
        quotes.append(quote)
        w.writerow(quote)
    
