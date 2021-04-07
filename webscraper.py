from selenium import webdriver
import pyinputplus as pyinp
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv

# Experience with multiple testing methods such as: smoke tests, black-box, white-box, gray-box, boundary testing.

class Linkedin():
    def __init__(self):
        url = 'https://www.linkedin.com/jobs/search/?f_E=2&f_WRA=true&geoId=92000000&keywords=software%20engineer&location=Worldwide&sortBy=DD&position=1&pageNum=0'
        options = Options()
        options.headless = True
        #self.driver = webdriver.Firefox(options=options, executable_path=r'C:/geckodriver/geckodriver.exe')
        self.driver = webdriver.Firefox(executable_path=r'C:/geckodriver/geckodriver.exe')
        self.driver.get(url)
        self.targets = ['python', 'django'] # Define targets for jobs
        self.might_jobs = []
        #self.login()        
        #self.csv_path = 'csvpath'
        #self.csvFile = open('output.csv', 'w', newline='')
        #if isfile(self.csv_path) 'Hay que comprobar que el archivo existe':
        #    self.csvDictWriter = csv.DictWriter(csvFile)
        #else:
        #    self.csvDictWriter = csv.DictWriter(csvFile, ['TimeStamp', 'Title', 'Location', 'Company'])
        #    csvDictWriter.writeheader()

    def login(self):
        try:
            session = driver.find_element_by_xpath('/html/body/header/nav/div/a[2]')
            session.click()
            time.sleep(1)
            try:
                username_input = self.driver.find_element_by_id('username')
                password_input = self.driver.find_element_by_id('password')
                login_input = self.driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button')
                username = pyinp.inputStr(prompt='Username: ')
                password = pyinp.inputPassword(prompt='Password: ')
                username_input.send_keys(username)
                password_input.send_keys(password)
                login_input.click()
            except Exception as exc:
                print('%s' % (exc))
        except:
            print('You are already loged')

    # Add new targets
    # def something

    # Check at least the first 100 jobs
    def search(self):
        print('Looking for jobs...')
        html = self.driver.find_element_by_tag_name('html')
        #section = driver.find_element_by_class_name('results__list')
        jobs = self.driver.find_elements_by_class_name('result-card')
        while len(jobs) < 50:
            html.send_keys(Keys.END)
            time.sleep(1)
            jobs = self.driver.find_elements_by_class_name('result-card')

            
        # Look jobs that fit the targets
        print('Filtrando jobs')
        for job in jobs:
            job.click()
            time.sleep(1)
            try:
                detail = self.driver.find_element_by_class_name('results__detail-view')
                description = detail.find_element_by_class_name('description').text.lower()
                topcard = detail.find_element_by_class_name('topcard')
                title = topcard.find_element_by_class_name('topcard__title').text
                company = topcard.find_elements_by_class_name('topcard__flavor')[0].text 
                location = topcard.find_elements_by_class_name('topcard__flavor')[1].text
                #self.csvDictWriter.writerow({'TimetStamp':time.ctime(), 'Title':title, 'Location':location, 'Company':company} )       
            except:
                continue
            score = 0
            for target in self.targets:
                if target in description:
                    score += 1
            if score > 0:
                try:
                    link = topcard.find_element_by_tag_name('a').get_attribute('href')
                    self.might_jobs.append(link)
                except:
                    print(title)
                    print('Without link')
                    continue
        #csvFile.close()
        self.driver.quit()
        print('Search finished! %s might jobs founded' % (len(self.might_jobs)))

    # Open driver with at most n first jobs
    def show(self, n):
        if self.might_jobs:
            self.browser = webdriver.Firefox(executable_path=r'C:/geckodriver/geckodriver.exe')
            #self.browser.get(self.might_jobs[0])
            for i in range(min(n, len(self.might_jobs))):
                self.browser.execute_script("window.open('%s');" %(self.might_jobs[i]))
                self.browser.switch_to_window(self.browser.window_handles[-1])
                if 'que compuebe la url':
                    print('You need to be loged to continue')
                    self.login()
                else:
                    continue
                time.sleep(0.5)                
        else:
            print('Better lucky next time')


