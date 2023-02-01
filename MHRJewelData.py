import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

website = "https://mhrise.kiranico.com/data/decorations"
decoPage = requests.get(website, headers=headers)
soup = BeautifulSoup(decoPage.content, "html.parser")

skillTable = soup.find("table")

rows = skillTable.findChildren("tr")

for elem in rows:
    print(elem)