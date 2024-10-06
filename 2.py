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

cur.execute('''CREATE TABLE IF NOT EXISTS Thoughts
    (id INTEGER NOT NULL PRIMARY KEY, tought TEXT UNIQUE)''')

url = 'https://fishki.net/3459433-na-vse-vremena-100-vdohnovljajuwih-citat.html'
document = urlopen(url, context=ctx)
html = document.read()

soup = BeautifulSoup(html, "html.parser")

whole_text = soup.find_all('div', attrs={'class': 'container_gallery_description'})
# whole_text = soup.find_all(lambda tag: tag.name=='div' and tag.has_attr('class') and tag.get('class')=='container_gallery_description' and tag.find(lambda ttag: ttag.name=='br'))
whole_text = whole_text[1:]
# print(whole_text)
for tag_div in whole_text:
    raw_text = tag_div.text.strip()
    text = re.split('[0-9]+\.', raw_text)
    text.remove(text[0])
    # print(text)
    for item in text:
        text_final = item.strip()
        # print(text_final)
        cur.execute('INSERT OR IGNORE INTO Thoughts (tought) VALUES (?)', (text_final,))

conn.commit()
cur.close()
