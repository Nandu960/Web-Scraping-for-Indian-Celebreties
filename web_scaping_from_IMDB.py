import requests
import pprint
from bs4 import BeautifulSoup

import sqlite3

con = sqlite3.connect('mydatabase.db')


cursorObj = con.cursor()

from sqlite3 import Error

def sql_connection():

    try:
        con = sqlite3.connect(':memory:')
        print("Connection is established: Database is created in memory")

    except Error:
        print(Error)

    finally:
        con.close()

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE celeb(Name text PRIMARY KEY, Image text,About text)")

    con.commit()


def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO celeb(Name,Image,About) VALUES(?, ?, ?)', entities)
    
    con.commit()
    
sql_connection()

##sql_table(con)


URL = 'https://www.imdb.com/list/ls068010962/'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')



results = soup.find('div', id='content-2-wide')

r=results.find_all('div',class_='lister-item mode-detail')


from bs4 import BeautifulSoup as BSHTML



    
for celeb in r:

    title_elem = celeb.find('h3', class_='lister-item-header')
    image_elem = celeb.find('div',class_='lister-item-image')
    info = celeb.find_all('p')[1]

    
    entities = (title_elem.a.text.upper(),image_elem.a.img['src'].strip(),info.text)
    try :
        sql_insert(con, entities)

        con.commit()
    except Exception as e:
        print(e)
        continue 
##    print(title_elem.a.text)
##    print(image_elem.a.img['src'].strip())
##    print(info.text)




    

