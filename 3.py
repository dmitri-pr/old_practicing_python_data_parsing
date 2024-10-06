import urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('T_bot.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Anecdotes
    (id INTEGER NOT NULL PRIMARY KEY, anecdote TEXT UNIQUE)''')

url = 'https://nekdo.ru/short/'

while True:
    try:
        document = urlopen(url, context=ctx)
        html = document.read()
    except:
        cur.close()
        break

    soup = BeautifulSoup(html, "html.parser")

    whole_text = soup.find_all('div', attrs={'class': 'text'})
    # print(whole_text)

    for tag in whole_text:
        text = tag.text.strip().replace('?-', '?\n-').replace('!-', '!\n-').replace('.-', '.\n-').replace(':-', ':\n-')
        print(text)
        cur.execute('INSERT OR IGNORE INTO Anecdotes (anecdote) VALUES (?)', (text,))

    conn.commit()

    next_link = soup.find('a', attrs={'title': 'Следующая страница'}).get('href')
    next_link_end = next_link.split('/', 2)[2]
    # print(next_link_end)
    url = 'https://nekdo.ru/short/' + next_link_end
    print(url)
