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


URL = 'https://en.wikipedia.org/wiki/List_of_Indian_film_actors'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')

##results = soup.find(id='content-2-wide')

results = soup.find('div', id='mw-content-text')

##r=results.find_all('div',class_='div-col columns column-width')

r=results.find_all('li')


##print(r)




   
for celeb in r:
##    print(celeb, end='\n'*2)
    name = celeb.a.text.strip()
##    if name !="Aadhi":
##        continue
##    print(name)

    try :
        new_url = 'https://en.wikipedia.org/wiki/'+name
##        print(new_url)
        new_page = requests.get(new_url)
        new_soup = BeautifulSoup(new_page.content, 'html.parser')
        
        new_results = new_soup.find('div',id="content")
        new_results = new_results.find('div',id='bodyContent')
    ##    new_results = new_results.find('div',id='mw-content-text')
        new_results = new_results.find('table',class_="infobox biography vcard")
    ##    new_results = new_results.find('a',class_='image')
        if None == new_results :
            continue 
        new_results = new_results.find('a',class_="image")

##        print((new_results.img['src']))

        new_results_text = new_soup.find_all('p')
##        print(new_results_text[1].text)

        entities = (name.upper(),(new_results.img['src']),new_results_text[1].text)
        try :
            sql_insert(con, entities)

            con.commit()
        except Exception as e:
##            print(e)
            continue 
    except Exception:
        continue 
    

    
##    new_results = new_soup.find_all('a',class_='image')
    

##    print("\n\n")
    
##    image_elem = celeb.find('div',class_='lister-item-image')
##    info = celeb.find_all('p')[1]
##    print("\n\n")
##    print(title_elem.a.text)
##    print(image_elem.a.img['src'].strip())
##    print(info.text)

##
##

    

