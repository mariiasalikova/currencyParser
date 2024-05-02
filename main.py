import requests
import streamlit as st
import datetime
from bs4 import BeautifulSoup as bs
import sqlite3
from transliterate import translit
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('currencies.db', check_same_thread=False)
cursor = conn.cursor()
d = dict([("Евро", "52170"), ("Доллар США", "52148"), ("Фунт Стерлингов", "52146"), ("Индийская рупия", "52238"), ("Йена", "52246"), ("Китайский юань", "52207"), ("Турецкая лира", "52158")])
fig, ax = plt.subplots()
plt.xlabel("DATE")
plt.ylabel("COURSE")


def main():
    cursor.execute("CREATE TABLE IF NOT EXISTS courses (CURRENCYCODE TEXT(50), DATE TEXT(15), COURSE REAL NOT NULL, COUNTRIES TEXT)")
    beginning, ending = input_data()
    get_main_data(beginning, ending)
    conn.commit()
    countries = getCurrencies()
    conn.commit()
    process(countries)
    
    

'''евро 52170
доллар 52148
фунт 52146
52238 рупия
52246 йена
52207 юань
52158 лира'''


def input_data() -> list[datetime.date, datetime.date]:
    
    jan_1 = datetime.date(2024, 1, 1)
    dec_31 = datetime.date(2024, 4, 4)

    beginning, ending = st.date_input(
        "Select your period",
        (jan_1, datetime.date(2024, 1, 7)),
        jan_1,
        dec_31,
        format="DD.MM.YYYY",
    )
    return beginning, ending

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
            addToDB(args)



def addToDB(args):
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", (args[0], args[1], args[2], '-'))

def getCurrencies():
    url = "https://www.iban.ru/currency-codes"
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    table = soup.find('table', class_="table table-bordered downloads tablesorter")
    tr_tags = table.find_all('tr')
    cache = []
    for tr in tr_tags[1:]:
        td_tags = tr.find_all('td')
        box = []
        
        for td in td_tags[0:2]:
            box.append(td.text.strip())
        if (box[1] in d.keys()) and (box[0] not in cache):
            cache.append(box[0])
            cursor.execute("UPDATE courses SET COUNTRIES = COUNTRIES || ? WHERE CURRENCYCODE = ?;", (box[0] + "-", d.get(box[1])))
    return cache

def process(countries):
    st.button('Add country', on_click=getCountry(countries))
    
def getCountry(countries):
    container = st.empty()
    country = container.selectbox('Country', countries)
    cntName = "analysis_" + translit(country, language_code='ru', reversed=True).replace(" ", "_").replace("\'", "_").replace("-", "_")
    cursor.execute("CREATE TABLE IF NOT EXISTS %s (CURRENCYCODE TEXT(50), DATE TEXT(15), COURSE REAL NOT NULL);" % (cntName))
    cursor.execute("SELECT * FROM courses WHERE COUNTRIES LIKE ?;", ['%' + country + '%'])
    rows = list(cursor.fetchall())
    for row in rows:
        cursor.execute("INSERT INTO %s VALUES (?, ?, ?);" % (cntName), row[:-1])
    st.info(country)
    
    data = pd.read_sql_query("SELECT * FROM %s" % (cntName), conn)
    
    data['COURSE'] = data['COURSE'].str.replace(',', '.')
    data['COURSE'] = pd.to_numeric(data['COURSE'])
    data = data.sort_values('DATE')
    x = data["DATE"]
    y = data["COURSE"]
    
    ax.plot(x, y)
    st.pyplot(fig)
    conn.commit()



main()
conn.close()