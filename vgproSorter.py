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
browser = webdriver.PhantomJS('./driver/phantomjs')
#----------------FOR DEBUG PURPOSES------------------
# browser = webdriver.Chrome('./driver/chromedriver')
#----------------------------------------------------
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
modes = soup.findAll('h2')
modesArrCounter = []
for i in range(0, len(strings.MODES_STR)):
	modesArrCounter.append(0)
for i in range(0, len(modes)):
	if modes[i].text==strings.MODES_STR[0]:				# Ranked 3v3
		modesArrCounter[0] = modesArrCounter[0] + 1
	elif modes[i].text==strings.MODES_STR[1]:			# Ranked 5v5
		modesArrCounter[1] = modesArrCounter[1] + 1
	elif modes[i].text==strings.MODES_STR[2]:			# Casual 3v3
		modesArrCounter[2] = modesArrCounter[2] + 1
	elif modes[i].text==strings.MODES_STR[3]:			# Casual 5v5
		modesArrCounter[3] = modesArrCounter[3] + 1
	elif modes[i].text==strings.MODES_STR[4]:			# Blitz
		modesArrCounter[4] = modesArrCounter[4] + 1
	elif modes[i].text==strings.MODES_STR[5]:			# Battle Royale
		modesArrCounter[5] = modesArrCounter[5] + 1

# find matches played as anka
heroArrCounter = []
heroLinkArr = []
for i in range(0, len(config.CONFIG['SPECIFIC_HERO_NAMES'])):
	heroArrCounter.append(0)
	heroLinkArr.append('background-image: url("https://vgproassets.nyc3.cdn.digitaloceanspaces.com/heroes/' + (config.CONFIG['SPECIFIC_HERO_NAMES'])[i] + '.png");')
for i in range(0, len(modes)):
	heroPicture = modes[i].parent
	for j in range(0, len(heroArrCounter)):
		hero = heroPicture.find_previous_sibling(attrs={'style': heroLinkArr[j]})
		if hero is not None:
			heroArrCounter[j] = heroArrCounter[j] + 1

# Print BeaufitulSoup done
print strings.DONE_BS_STR


#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------RESULTS-----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

print
print strings.BORDER_TOP_BOT
print strings.INDENT_STR + strings.RESULT_HEADER + str(config.CONFIG['DISPLAY_X_LAST_GAMES']) + ' games:'
print
for i in range(0, len(modesArrCounter)):
	print strings.INDENT_STR + strings.MODES_STR[i] + ': ' + str(modesArrCounter[i]) + ' games.'
print
for i in range(0, len(heroArrCounter)):
	print strings.INDENT_STR + (config.CONFIG['SPECIFIC_HERO_NAMES'])[i].capitalize() + ' Played: ' + str(heroArrCounter[i]) + ' games.'
print strings.BORDER_TOP_BOT