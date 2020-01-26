import os
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from subprocess import call

def start_browser(directory):
	display = Display(visible=0, size=(800, 600))
	display.start()

	options = Options()
	options.add_experimental_option("prefs", {
	  "download.default_directory": directory,
	  "download.prompt_for_download": False,
	  "download.directory_upgrade": True,
	  "safebrowsing.enabled": True
	})

	return webdriver.Chrome(chrome_options=options)


def get_available_subs(query, browser):
	url = "http://www.rentanadviser.com/en/subtitles/subtitles4songs.aspx?"+urllib.parse.urlencode({'src':query})
	browser.get(url)
	soup = BeautifulSoup(browser.page_source, 'html5lib')
	subs = [{'name':table.a.text.replace('\n','').strip(), 'url':table.a['href']} for table in soup.findAll('table')]
	return subs


def download_sub(sub, browser):
	url = "http://www.rentanadviser.com/en/subtitles/" + sub['url']
	browser.get(url)
	browser.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$btnSub','')")
