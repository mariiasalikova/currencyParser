import requests
import streamlit as st
import datetime
from bs4 import BeautifulSoup as bs
import sqlite3

conn = sqlite3.connect('currencies.db', check_same_thread=False)
cursor = conn.cursor()

def main():
    cursor.execute("""CREATE TABLE IF NOT EXISTS courses (CURRENCYCODE TEXT(50), DATE TEXT(15), COURSE REAL NOT NULL, COUNTRIES TEXT)""")
    beginning, ending, country = input_data()
    get_main_data(beginning, ending)
    conn.commit()

'''евро 52170
доллар 52148
фунт 52146
52238 рупия
52246 йена
52207 юань
52158 лира'''


def input_data() -> list[datetime.date, datetime.date, str]:
    
    jan_1 = datetime.date(2024, 1, 1)
    dec_31 = datetime.date(2024, 4, 4)

    beginning, ending = st.date_input(
        "Select your period",
        (jan_1, datetime.date(2024, 1, 7)),
        jan_1,
        dec_31,
        format="DD.MM.YYYY",
    )
    country = st.text_input('Country')
    return beginning, ending, country

def get_main_data(beginning: datetime.date, ending: datetime.date):
    urls = []
    
    url_begin = "https://www.finmarket.ru/currency/rates/?id=10148&pv=1&"
    url_end = "&x=24&y=7#archive"
    by, bm, bd = beginning.year, beginning.month, beginning.day
    ey, em, ed = ending.year, ending.month, ending.day
    for code in ['52170', '52148', '52146', '52238', '52246', '52207', '52158']:
        url_mid = f"cur={code}&bd={bd}&bm={bm}&by={by}&ed={ed}&em={em}&ey={ey}"
        url = url_begin + url_mid + url_end
        urls.append(url)
        
        page = requests.get(url)
        soup = bs(page.text, 'html.parser')
        
        table = soup.find('table', class_='karramba')
        tr_tags = table.find_all('tr')
        for tr in tr_tags[1:]:
            td_tags = tr.find_all('td')
            args = [code]
            for td in td_tags[0:3:2]:
                args.append(td.text.strip())
            print(args)
            addToDB(args)
        


def addToDB(lst):
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", (lst[0], lst[1], lst[2], '-'))
main()

conn.close()