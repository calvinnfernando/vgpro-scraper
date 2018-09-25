# import libraries
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# declare constants
CLICK_VIEW_MORE = 10

# url
webpage = 'https://vgpro.gg/players/calvinfernando'

#---------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------SELENIUM-----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

# open url using phantomjs
browser = webdriver.PhantomJS()
# browser = webdriver.Chrome()
browser.get((webpage))

# click view more until it is disabled or for CLICK_VIEW_MORE times
for i in range(0, CLICK_VIEW_MORE):
	viewMoreButton = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'View More')]")))
	if viewMoreButton.is_enabled():
		viewMoreButton.click()
	else:
		print 'Done in iteration #' + i
		break


#---------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------BEAUTIFULSOUP--------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

# open html of the page