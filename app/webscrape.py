import requests
from bs4 import BeautifulSoup as bs

def getProductUpdates():

    url="https://kalimatimarket.gov.np/index.php/lang/en"

    response=requests.get(url)
    beautify=bs(response.text,"html.parser") 

    data_table=beautify.find('table',{'id':'commodityDailyPrice'} ) 
    body=data_table.find('tbody')
    data_rows=body.findAll('tr')

    products_Dict={}

    for row in data_rows:
        data=row.findAll("td")
        name=data[0].text.strip()
        maxPrice=data[3].text.strip()
       
        products_Dict[name]=maxPrice 
        
        
    return products_Dict 

    

