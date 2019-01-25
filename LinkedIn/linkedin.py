import csv
from selenium import webdriver
from parsel import Selector
import parameters
from time import sleep
from selenium.webdriver.common.keys import Keys

writer = csv.writer(open(parameters.file_name, 'w+'))
writer.writerow(['Name', 'Job Title', 'Location', 'URL'])

driver = webdriver.Chrome('C:/Users/VATSAL AJMERA/Desktop/Scrapy Course/chromedriver')

driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(5)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = [url.text for url in linkedin_urls]
del linkedin_urls[-1]
sleep(0.5)

for linkedin_url in linkedin_urls:
	driver.get(linkedin_url)
	sleep(5)

	sel = Selector(text=driver.page_source)
	name = sel.xpath('//h1/text()').extract_first()
	job_title = sel.xpath('//h2/text()').extract_first()
	location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

	linkedin_url = driver.current_url

	print ('\n')
	print ('Name' + name)
	print ('Job Title' + job_title)
	print ('Location' + location)
	print ('URL' + linkedin_url)
	print ('\n')

	writer.writerow([name.encode('utf-8'),
					job_title.encode('utf-8'),
					location.encode('utf-8'),
					linkedin_url.encode('utf-8')])
	try:
		driver.find_element_by_xpath('//span[text()="Connect"]').click()
		sleep(3)
		driver.find_element_by_class_name('button-primary-large ml1').click()
		sleep(3)
	except:
		pass
driver.quit()