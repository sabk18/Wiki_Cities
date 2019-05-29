#Data Engineering intern Assignment-2019 for Topos
#User: Saba Khalid
#Python version:compatible with 2.7 & 3.6

#import required libraries:
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

website = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")   #query the website                                  
soup = BeautifulSoup(website.content, 'html.parser')                          #parse the HTML 
table =soup.find('table',{'class':'wikitable sortable'})    #Extract information from the table with class "wikitable sortable"

rows=table.findAll('tr')                                    #iterate through the rows in the table and assign them to the variable 'rows'
urls_list =[]               #empty list to store websites
data_list =[]               #empty list to store table info   
location_list=[]             
for row in rows:                          
    data =row.find_all('td')                                 #element of 'td' from each row is stored in the variable 'data'
    if len(data)>1:                                                     
        city_data = [info.text.strip('\n') for info in data]  #extract data for teh columns within the table into city_data
        city_links = data[1].find('a')                        #find the links stored in <a> tag for City column
        urls_list.append(city_links.get('href'))                   #extracts the link using the attribute 'href' and append to the empty list for websites              
        data_list.append(city_data)                              #appends the city info into the table list
        location = data[10].find('a')
        location_list.append(location.get('href'))

urls_list =['https://en.wikipedia.org'+ i for i in urls_list]   #links within the "url" are in the format /wiki/New_York_City so we add the initial part of URL to each 
location_list=['https:'+ i for i in location_list]               #adds https: to the links

#extracting "Time zone" from the city websites for TOP 20 ONLY:
def get_TimeZone(urls):
    Timezone = []
    #urls = urls[:50] #comment out to fetch data for all 314 cities
    for link in urls:   #query the top 50 cities websites
        web = requests.get(link)      #query the top 20 cities websites 
        read_data =False                                
        b = BeautifulSoup(web.content, 'html.parser')      #parse the HTML
        try:
            table =b.find('table',{'class':'infobox geography vcard'})  #find the table with class infobox geography vcard
            for row in table.findAll('tr'):                              #iterates over the rows in the table
                    if ((row.get('class') == ['mergedtoprow']) and not read_data): #finds the class:mergedtoprow within the rows
                        link = row.find('a')                                          #stores the links within the a tag into variable link
                        #print link
                        if (link and (link.get_text().strip() == 'Time zone')):           #if value within the tag is equal to Time zone, it will pass on True
                            read_data =True
                            Timezone.append(row.find('td').get_text().strip('\n'))  #appends the data from into Timezone-empty list
                            #print row                
                        if (link and (link.get_text().strip() == 'Zip code')):     #if encounters Zip code it will read False
                            read_data =False            
        except:         #if timezone is not found then it will continue to the next
             continue    
    return Timezone
print ("Extracting Data: ")
Time_Zone =get_TimeZone(urls_list)   #calls the function

df_timezone=pd.DataFrame({'Time_Zone':Time_Zone})         #create a dataframe using pandas for :Time_zone, urls_list , data_table & location_list
df_urls =pd.DataFrame({'City_Website':urls_list})                                                                                      
df_dataset =pd.DataFrame(data_list)  
df_location=pd.DataFrame({'location_urls':location_list})                               

df_dataset.columns =['0','1','2','3','4','5','6','7','8','9','10']  #assigns each column in the dataframe df_dataset with a number
df_dataset.drop(['7','9'],axis =1,inplace =True)                    #drop the columns 7 and 9, for they contain the same information as columns 6 and 8 respectively but in different units of km^2

#extract headers from table
headers =rows[0].find_all('th')                    
headers =[th.getText().strip() for th in headers]  #extracts the text in between html tags for table headers
df_dataset.columns =headers                        #assigns new column headers to our dataframe

df =df_dataset.join(df_urls)                       #joins the  dataframes:  dataset , df_url , df_location into one df 
df =df.join(df_timezone)
df =df.join(df_location)

#remove the 'Location' column :
df =df.drop(['Location'],axis =1)

#change the name of the columns to meet the CSV schema requirements for BigQuery:'only letters,numbers and underscore':
df =df.rename(columns ={"State[c]":"State","2018rank":"Rank","2018estimate":"Estimate_2018","2010Census":"Census_2010","Change":"Percentage_Change","2016 land area":"Land_area_2016_sqmi","2016 population density":"Population_density_2016_sqmi"})

#<--clean the data within dataframe-->:
df["Percentage_Change"]= df["Percentage_Change"].str.replace(r"[^\d.]+", "")   #removes alphabets,%,+,-, signs
df["City"]=df["City"].str.replace(r"\[.*?]", "")  #replaces parenthesis [x] with nothing

df=df.apply(lambda x: x.str.replace(',',''))      #replaces the comma with nothing

df["Land_area_2016_sqmi"]=df["Land_area_2016_sqmi"].str.replace(r'[^0-9.]+','')#remove any characters except 0-9 and "."
df["Population_density_2016_sqmi"]=df["Population_density_2016_sqmi"].str.replace(r'[^0-9.]+','')     #remove any characters except 0-9 and "."
#to convert obj to integer/float as needed:
df[["Estimate_2018","Census_2010","Land_area_2016_sqmi","Population_density_2016_sqmi"]]= df[["Estimate_2018","Census_2010","Land_area_2016_sqmi","Population_density_2016_sqmi"]].apply(pd.to_numeric)

df =df.replace('^\s*$',np.nan,regex=True).fillna("No Data") #replaces missing values with 'No Data'

print (df.head(15))    
print (df.info())
print ("\nCSV file is generated\n")
#saves df into a csv file:
df.to_csv('webscraping_cities_SK.csv',encoding='utf-8', index=False)

#end
