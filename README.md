# Wiki_Cities

## Introduction

This assignment aims at scraping data from [Wikipedia](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population) using Python. The unstructured data on the top cities in the United States ,ranked by population, was scraped and stored into a structured format one that can be used for future data analysis.   

## Technologies

This code is compatible with both Python 2.7 and Python 3.6. The libraries imported are:
  * requests
  * BeautifulSoup
  * Pandas
  * Numpy
  * Regex
  
## Data

The data collected for the top 314 cities mentioned in Wikipedia includes:

  * Rank
  * City
  * State
  * Estimate Population for 2018
  * Census Population for 2010
  * Percentage change between 2010-2018 
  * Land area in square mile for 2016
  * Population density in square mile for 2016
  * City website 
  * Time Zones
  * Location urls
  
 ## Program-Code
 
The program uses requests library to query the website and then parse the HTML document with BeautifulSoup.
inspecting the web page will give us further information on the classes for the tables. The class under observation, in this case is "wikitable sortable".
The code iterates through the rows within the table and stores the elements within these rows into the variable "data". Similarly, I extracted the links within the <a> tag for each of the cities and their respective locations.
The data collcted through these steps is stored into lists and then a dataframe is created for each of these lists. the dataframes are joined and then data is cleaned and filtered.
To extract the timezone for individual cities, the code iterated through each site to fetch the timezone data.

**Note:** Line 36 is commented to fetch data for all the cities. If one is interested in finding the data for just the top 50 cities they can uncomment the line. 

## Overview

This data generates a CSV file that can be uploaded to BigQuery Table (file format is compatible)

Schema: Rank:string,City:string,State:string,Estimate_2018:integer,Census_2010:integer,Percentage_Change:string,Land_area_2016_sqmi:float,Population_density_2016_sqmi:integer,City_Website:string,Time_Zone:string,Location_urls:string

This data can allow for further analysis of these cities by comparing the data of these cities and answer questions like why is New York City more Populated then e.g: Orlando
