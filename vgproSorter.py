# import libraries
import strings
import config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# url
webpage = 'https://vgpro.gg/players/' + config.CONFIG['PLAYER_USERNAME_STR']

#---------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------SELENIUM-----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

# Print loading Selenium
print strings.LOAD_SELENIUM_STR

# open url using phantomjs
# browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
browser.get((webpage))

# click view more until it is disabled or for clickViewMore times
clickViewMore = (config.CONFIG['DISPLAY_X_LAST_GAMES'] / 10) - 1
for i in range(0, clickViewMore):
	viewMoreButton = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'View More')]")))
	if viewMoreButton.is_displayed() and viewMoreButton.is_enabled():
		viewMoreButton.click()
	else:
		print 'Done in iteration #' + str(i)
		break

# Print Selenium done
print strings.DONE_SELENIUM_STR


#---------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------BEAUTIFULSOUP--------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

# Print loading BeaufitulSoup
print strings.LOAD_BS_STR

# open html of the page
soup = BeautifulSoup(browser.page_source, 'html.parser')

# find all modes
modesCounter = 0
modes = soup.findAll('h2')
for i in range(0, len(modes)):
	if modes[i].text=="Ranked 3v3":
		modesCounter = modesCounter + 1

# find matches played as anka
heroCounter = 0
heroLink = 'background-image: url("https://vgproassets.nyc3.cdn.digitaloceanspaces.com/heroes/' + config.CONFIG['SPECIFIC_HERO_NAME'] + '.png");'
for i in range(0, len(modes)):
	heroPicture = modes[i].parent
	hero = heroPicture.find_previous_sibling(attrs={'style': heroLink})
	if hero is not None:
		heroCounter = heroCounter + 1

# Print BeaufitulSoup done
print strings.DONE_BS_STR


#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------RESULTS-----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

print
print strings.RESULT_HEADER + str(config.CONFIG['DISPLAY_X_LAST_GAMES']) + ' games:'
print 'Ranked 3v3: ' + str(modesCounter) + ' games.'
print config.CONFIG['SPECIFIC_HERO_NAME'] + ' Played: ' + str(heroCounter) + ' games'