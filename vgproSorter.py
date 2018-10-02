# import libraries
import strings
import config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def sortHeroes():
	# check if the hero names inputted are correct
	validHeroNames = [0 for i in range(len(config.CONFIG['SPECIFIC_HERO_NAMES']))]
	for i in range(len(config.CONFIG['SPECIFIC_HERO_NAMES'])):
		# DIVIDE AND CONQUER
		low = 0
		high = len(strings.HEROES_ARR) - 1
		mid = int(low + high) / int(2)
		while low <= high and mid >= low and mid <= high:
			if (config.CONFIG['SPECIFIC_HERO_NAMES'])[i].lower() < strings.HEROES_ARR[mid]:
				high = mid - 1
			elif (config.CONFIG['SPECIFIC_HERO_NAMES'])[i].lower() > strings.HEROES_ARR[mid]:
				low = mid + 1
			else:
				validHeroNames[i] = 1
				break
			mid = int(low + high) / int(2)

	# url
	webpage = strings.WEB_URL + config.CONFIG['PLAYER_USERNAME_STR'].lower()

	#---------------------------------------------------------------------------------------------------------------------------------------
	#--------------------------------------------------------------SELENIUM-----------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------------------------

	# Print loading Selenium
	print strings.LOAD_SELENIUM_STR

	# open url using phantomjs
	# browser = webdriver.PhantomJS('./driver/phantomjs')
	#----------------FOR DEBUG PURPOSES-------------------
	browser = webdriver.Chrome('./driver/chromedriver')
	#-----------------------------------------------------
	browser.get((webpage))

	# click view more until it is disabled or for clickViewMore times
	clickViewMore = (config.CONFIG['DISPLAY_X_LAST_GAMES'] / 10) - 1
	for i in range(clickViewMore):
		viewMoreButton = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'View More')]")))
		if viewMoreButton.is_displayed() and viewMoreButton.is_enabled():
			viewMoreButton.click()
		#----------------FOR DEBUG PURPOSES-------------------
		else:
			print 'Done in iteration #' + str(i)
			break
		#-----------------------------------------------------

	# close browser
	browser.quit()

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
	modes = soup.find_all('h2')
	modesArrCounter = [0 for i in range(len(strings.MODES_ARR))]
	for i in range(len(modes)):
		if modes[i].text == strings.MODES_ARR[0]:				# Ranked 3v3
			modesArrCounter[0] = modesArrCounter[0] + 1
		elif modes[i].text == strings.MODES_ARR[1]:			# Ranked 5v5
			modesArrCounter[1] = modesArrCounter[1] + 1
		elif modes[i].text == strings.MODES_ARR[2]:			# Casual 3v3
			modesArrCounter[2] = modesArrCounter[2] + 1
		elif modes[i].text == strings.MODES_ARR[3]:			# Casual 5v5
			modesArrCounter[3] = modesArrCounter[3] + 1
		elif modes[i].text == strings.MODES_ARR[4]:			# Blitz
			modesArrCounter[4] = modesArrCounter[4] + 1
		elif modes[i].text == strings.MODES_ARR[5]:			# Battle Royale
			modesArrCounter[5] = modesArrCounter[5] + 1

	# find matches played as SPECIFIC_HERO_NAMES and the details needed (KDA, items)
	heroLinkArr = []
	modesArr = []		# Modes array (parallel array)
	KArr = []			# Kill array (parallel array)
	DArr = []			# Death array (parallel array)
	AArr = []			# Assist array (parallel array)
	KDAArr = []			# KDA array (parallel array)
	winLossArr = []		# Win/Loss array (parallel array)
	itemsArr = []		# Items array (parallel array)
	for i in range(len(config.CONFIG['SPECIFIC_HERO_NAMES'])):
		heroLinkArr.append(strings.BG_IMAGE_URL_STR + strings.HEROES_STR + (config.CONFIG['SPECIFIC_HERO_NAMES'])[i].lower() + strings.PNG_STR)
		modesArr.append([])
		KArr.append([])
		DArr.append([])
		AArr.append([])
		KDAArr.append([])
		winLossArr.append([])
		itemsArr.append([])
	for i in range(len(modes)):
		heroDetails = modes[i].parent
		for j in range(len(heroLinkArr)):
			if validHeroNames[j] != 0:
				hero = heroDetails.find_previous_sibling(attrs={'style': heroLinkArr[j]})
				if hero is not None:
					modesArr[j].append(modes[i].text)
					heroDeath = heroDetails.find('span', class_='death')
					DArr[j].append(heroDeath.text)
					KArr[j].append(heroDeath.previous_sibling.previous_sibling.text)
					AArr[j].append(heroDeath.next_sibling.next_sibling.text)
					KDAArr[j].append("{0:.2f}".format((int(heroDeath.previous_sibling.previous_sibling.text) + int(heroDeath.next_sibling.next_sibling.text)) / float(heroDeath.text)))
					winLossArr[j].append("{:<4}".format(heroDetails.find_previous_sibling('div', class_='sc-jVODtj').text))
					
					itemsInGameArr = []
					item = heroDetails.next_sibling.find('div', class_='PlayerMatch-Item')
					for k in range(6):
						# DIVIDE AND CONQUER
						low = 0
						high = len(strings.ITEMS_ARR) - 1
						mid = int(low + high) / int(2)
						while low <= high and mid >= low and mid <= high:
							itemLink = strings.BG_IMAGE_URL_STR + strings.ITEMS_STR + strings.ITEMS_ARR[mid] + strings.PNG_STR
							if item.has_attr('style'):
								if item['style'] < itemLink:
									high = mid - 1
								elif item['style'] > itemLink:
									low = mid + 1
								else:
									itemsInGameArr.append(strings.ITEMS_ARR[mid].replace('-', ' ').title())
									break
							else:
								break
							mid = int(low + high) / int(2)
						item = item.next_sibling
					itemsArr[j].append(itemsInGameArr)

	# calculate average KDA for each hero
	avgKDAArr = []
	for i in range(len(heroLinkArr)):
		if len(KArr[i]) == 0:
			avgKDAArr.append("{0:.2f}".format(0.0))
		else:
			totalK = 0.0
			totalD = 0.0
			totalA = 0.0
			for j in range(len(KArr[i])):
				totalK = totalK + float(KArr[i][j])
				totalD = totalD + float(DArr[i][j])
				totalA = totalA + float(AArr[i][j])
			if totalD == 0.0:
				totalD = float(1.0)
			avgKDAArr.append("{0:.2f}".format((totalK + totalA) / float(totalD)))

	# enter all the results into a dict
	resultDict = {
		'hero_names_arr' : config.CONFIG['SPECIFIC_HERO_NAMES'],
		'valid_hero_names_arr' : validHeroNames,
		'avg_kda_arr' : avgKDAArr,
		'kills_arr' : KArr,
		'deaths_arr' : DArr,
		'assists_arr' : AArr,
		'kda_arr' : KDAArr,
		'win_loss_arr' : winLossArr,
		'modes_arr' : modesArr,
		'items_arr' : itemsArr
	}

	# Print BeaufitulSoup done
	print strings.DONE_BS_STR


	#---------------------------------------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------PANDAS-----------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------------------------------------------

	# print loading pandas
	print strings.LOAD_PANDAS_STR

	# convert resultDict in JSON format
	resultInJSONFormat = pd.Series(resultDict).to_json()

	# print pandas done
	print strings.DONE_PANDAS_STR

	# return from function
	return resultInJSONFormat


#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------RESULTS-----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	resultJSON = sortHeroes()
	resultDictionary = pd.read_json(resultJSON)
	print
	print strings.BORDER_TOP_BOT
	print
	print strings.INDENT_STR + strings.RESULT_HEADER + str(config.CONFIG['DISPLAY_X_LAST_GAMES']) + ' games:'
	# print
	# for i in range(len(modesArrCounter)):
	# 	print strings.INDENT_STR + strings.MODES_ARR[i] + ': ' + str(modesArrCounter[i]) + ' games.'
	print
	for i in range(len(resultDictionary['hero_names_arr'])):
		print strings.BORDER_HEROES
		print
		if resultDictionary['valid_hero_names_arr'][i] == 0:
			print strings.INDENT_STR + resultDictionary['hero_names_arr'][i].capitalize() + ' is not a valid hero name in VainGlory!'
		else:
			print strings.INDENT_STR + resultDictionary['hero_names_arr'][i].capitalize() + ' Played: ' + str(len(resultDictionary['kills_arr'][i])) + ' games (Average KDA: ' + str(resultDictionary['avg_kda_arr'][i]) + ')'
			if len(resultDictionary['kills_arr'][i]) == 0:
				print
			for j in range(len(resultDictionary['kills_arr'][i])):
				print strings.DOUBLE_INDENT_STR + 'Game ' + str(j + 1) + ' - ' + resultDictionary['win_loss_arr'][i][j] + ' : ' + str(resultDictionary['kda_arr'][i][j]) + ' KDA (' + str(resultDictionary['kills_arr'][i][j]) + '/' + str(resultDictionary['deaths_arr'][i][j]) + '/' + str(resultDictionary['assists_arr'][i][j]) + ') - ' + resultDictionary['modes_arr'][i][j]
				k = 0
				while k < len(resultDictionary['items_arr'][i][j]):
					if k == (len(resultDictionary['items_arr'][i][j]) - 1):
						print strings.DOUBLE_INDENT_STR + strings.DOUBLE_INDENT_STR + 'Items : ' + "{:<20}".format(resultDictionary['items_arr'][i][j][k])
					else:
						print strings.DOUBLE_INDENT_STR + strings.DOUBLE_INDENT_STR + 'Items : ' + "{:<20}".format(resultDictionary['items_arr'][i][j][k]) + strings.INDENT_STR + "{:<20}".format(resultDictionary['items_arr'][i][j][k + 1])
					k = k + 2
				print
	print strings.BORDER_TOP_BOT