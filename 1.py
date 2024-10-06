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

cur.execute('''CREATE TABLE IF NOT EXISTS Prophecies
    (id INTEGER NOT NULL PRIMARY KEY, prophecy TEXT UNIQUE)''')

url = 'https://woman-gu.ru/dlya-prazdnika/pozhelaniya/365-predskazanij-spisok/'
document = urlopen(url, context=ctx)
html = document.read()

soup = BeautifulSoup(html, "html.parser")

whole_text = soup.find(lambda tag: tag.name == 'ol' and tag.find(lambda ttag: ttag.name == 'li'))

tags_li = whole_text.find_all('li')
# print(tags_li)
for tag in tags_li:
    prophecy = tag.text.strip()

    cur.execute('INSERT OR IGNORE INTO Prophecies (prophecy) VALUES (?)', (prophecy,))

conn.commit()
cur.close()
