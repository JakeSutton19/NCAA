#Imports
import csv
import requests
import urllib
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time

class Data_Bot:
    def __init__(self, *start_date, **end_date):
        #URLS
        self.current_url = None
        self.past_url = None

        #CSV
        self.csv_current = None
        self.csv_past = None
        self.csv_future = None

        #Initalize
        self.response = None
        self.soup = None

        #Dates
        self.start_date = start_date
        self.end_date = end_date
        self.today = 0

        #Schedule
        self.years = [2018, 2019, 2020]
        self.months = ['11', '12', '01', '02', '03', '04']
        self.days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
        '22', '23', '24', '25', '26', '27', '28','29', '30', '31']

        #Tests
        self.current_season = '2019/'

        #Status
        self.status = None
        self.attempt = 0
        self.fails = 0
        self.fail_files = [] 


    def Run(self):
        for mon in self.months:
            for i in self.days:
                self.today = self.Make_Date(self.years[1], mon, i)

                #Go to Page
                url = 'https://www.espn.com/mens-college-basketball/schedule/_/date/{}/group/50'.format(self.today)
                self.Access_Page(url)

                #Scrape page
                self.Scrape()

                #Check for errors
                if (self.fails > 2):
                    quit()

                print("Date: {},  Errors: {}".format(self.today, self.fails))
                time.sleep(.3)



    def Make_Date(self, year, month, day):
        date = str(year) + month + day
        return date


    def Access_Page(self, url):
        req = urllib.request.Request(url=url)
        try:
            content = urllib.request.urlopen(req).read()
        except HTTPError as error:
            content = error.read()
        self.soup = BeautifulSoup(content, "html.parser")
        time.sleep(.5)


    def Scrape(self):
        #Find data
        table = self.soup.find('table')
        time.sleep(.2)

        #Check for data
        if (table != None):
            rows = table.select('tbody > tr')
            header = [th.text.rstrip() for th in rows[0].find_all('th')]

            #Save Data
            self.save_folder = self.current_season + str(self.today)
            s = str(self.save_folder)

            #Write to CSV
            with open(s, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)
                for row in rows[1:]:
                    data = [th.text.rstrip() for th in row.find_all('td')]
                    writer.writerow(data)
        else:
            self.fails += 1
            
            




# if __name__ == '__main__':
#     bot = Data_Bot()
#     bot.Run()