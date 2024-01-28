from selenium import webdriver
import pandas as pd
#import unidecode
import time


driver = webdriver.Chrome(executable_path = 'C:/Users/Katie/Downloads/chromedriver.exe')
driver.get("https://casesearch.courts.state.md.us/casesearch/inquiry-index.jsp")
agree_button = driver.find_element_by_xpath("/html/body/div[2]/form[@id='frmCasesearchdisclaimer']/table/tbody/tr[7]/td/input")
agree_button.click()

agree_button = driver.find_element_by_xpath("/html/body/div[2]/form[@id='frmCasesearchdisclaimer']/table/tbody/tr[8]/td/input[@id='btnDisclaimerAgree']")
agree_button.click()


driver.find_element_by_xpath("/html/body/div/span[@class='pagelinks'][1]/a[1]").click()

driver.find_element_by_xpath("/html/body/div/table[@id='row']/tbody/tr[@class='odd'][1]/td[1]/a").click()
time.sleep(5)
caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']").text
driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']/div[@class='Subheader']/a").click()
time.sleep(3)
# cycle to even, through 13, but no even on 13
cases = []
xtracases = []
casenums = []
backup = cases.copy()

for i in range(13):
    print(i)
    pathx = "/html/body/div/table[@id='row']/tbody/tr[@class='" + "odd'][" + str(i+1) + "]/td[1]/a"
    casenums.append(driver.find_element_by_xpath(pathx).text)
    driver.find_element_by_xpath(pathx).click()
    time.sleep(6)
    caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']").text
    cases.append(caseinfo)
    driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']/div[@class='Subheader']/a").click()
    time.sleep(8)
    if i != 12:
        pathx = "/html/body/div/table[@id='row']/tbody/tr[@class='" + "even'][" + str(i+1) + "]/td[1]/a"
        casenums.append(driver.find_element_by_xpath(pathx).text)
        driver.find_element_by_xpath(pathx).click()
        time.sleep(6)
        caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']").text
        cases.append(caseinfo)
        driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']/div[@class='Subheader']/a").click()
        time.sleep(8)

driver.find_element_by_xpath("/html/body/div/span[@class='pagelinks'][1]/a[14]").click()

for i in range(10):
    for i in range(13): # 7, 
        print(i) 
        pathx = "/html/body/div/table[@id='row']/tbody/tr[@class='" + "odd'][" + str(i+1) + "]/td[1]/a"
        casenums.append(driver.find_element_by_xpath(pathx).text)
        print(casenums[-1])
        driver.find_element_by_xpath(pathx).click()
        time.sleep(15)
        try:
            caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']").text
            cases.append(caseinfo)
            print(len(cases))
            driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']/div[@class='Subheader']/a").click()
            time.sleep(15)
        except:
            caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindowDcCivil']").text
            xtracases.append(caseinfo)
            driver.find_element_by_xpath("/html/body/div[@class='BodyWindowDcCivil']/div[2]/center/a").click()
            time.sleep(20)
        if i != 12:
            pathx = "/html/body/div/table[@id='row']/tbody/tr[@class='" + "even'][" + str(i+1) + "]/td[1]/a"
            casenums.append(driver.find_element_by_xpath(pathx).text)
            print(casenums[-1])
            driver.find_element_by_xpath(pathx).click()
            time.sleep(15)
            try:
                caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']").text
                cases.append(caseinfo)
                print(len(cases))
                driver.find_element_by_xpath("/html/body/div[@class='BodyWindow']/div[@class='Subheader']/a").click()
                time.sleep(15)
            except:
                caseinfo = driver.find_element_by_xpath("/html/body/div[@class='BodyWindowDcCivil']").text
                xtracases.append(caseinfo)
                driver.find_element_by_xpath("/html/body/div[@class='BodyWindowDcCivil']/div[2]/center/a").click()
                time.sleep(8)
    driver.find_element_by_xpath("/html/body/div/span[@class='pagelinks'][1]/a[16]").click()
    time.sleep(40)


casenumcol = []
systemcol = []
locationcol = []
filingcol = []
statuscol = []

casenumsfordefmap = []
deffullnamecol = []
defaddresscol = []
citycol = []
statecol = []
zipcol = []

ct = 0
for case in cases:
    ct += 1
    for val in case.split("\n"):
        if 'Case Number: ' in val:
            casenum = val.split(": ")[1]
            print(casenum)
            casenumcol.append(casenum)
        if 'Court System: ' in val:
            systemcol.append(val.split(": ")[1])
        if 'Location: ' in val:
            locationcol.append(val.split(": ")[1])
        if 'Filing Date: ' in val:
            filingcol.append(val.split(": ")[1])
        if 'Case Status: ' in val:
            statuscol.append(val.split(": ")[1])
    datlist = case.split("\n")
    for i in range(len(datlist)):
        if 'Defendant' in datlist[i]:
            if 'Name: ' in datlist[i+1]:
                casenumsfordefmap.append(casenum)
                deffullnamecol.append(datlist[i+1].split(": ")[1])
                if 'Address' not in datlist[i+2]:
                    defaddresscol.append('')
                    citycol.append('')
                    statecol.append('')
                    zipcol.append('')
                elif 'City' not in datlist[i+3]:
                    defaddresscol.append(datlist[i+2].split(": ")[1] + ' ' + datlist[i+3])
                    citystzip = datlist[i+4]
                    citycol.append(citystzip.split('State:')[0].split(': ')[1])
                    statecol.append(citystzip.split('State:')[1].split('Zip Code:')[0])
                    zipcol.append(citystzip.split('State:')[1].split('Zip Code:')[1])
                else:
                    defaddresscol.append(datlist[i+2].split(": ")[1])
                    citystzip = datlist[i+3]
                    citycol.append(citystzip.split('State:')[0].split(': ')[1])
                    statecol.append(citystzip.split('State:')[1].split('Zip Code:')[0])
                    zipcol.append(citystzip.split('State:')[1].split('Zip Code:')[1])
    
cases[ct-1].split('\n')

# fix names
lasts = []
firsts = []
mids = []
suff = []
for name in deffullnamecol:
    if len(name.split(', ')) == 1:
        firsts.append(name.split(', ')[0])
        lasts.append('')
        mids.append('')
        suff.append('')
    if len(name.split(', ')) == 2:
        lasts.append(name.split(', ')[0])
        firsts.append(name.split(', ')[1].split(' ')[0])
        if len(name.split(', ')[1].split(' ')) == 1:
            mids.append('')
            suff.append('')
        if len(name.split(', ')[1].split(' ')) == 3:
            mids.append(name.split(', ')[1].split(' ')[1])
            suff.append(name.split(', ')[1].split(' ')[2])
        if len(name.split(', ')[1].split(' ')) == 2:
            if '.' in name.split(', ')[1].split(' ')[1]:
                suff.append(name.split(', ')[1].split(' ')[1])
                mids.append('')
            else:
                mids.append(name.split(', ')[1].split(' ')[1])
                suff.append('')

casenumcol.extend(['010100102112022', '010100047522022'])
systemcol.extend(['DISTRICT COURT FOR BALTIMORE CITY - CIVIL SYSTEM','DISTRICT COURT FOR BALTIMORE CITY - CIVIL SYSTEM'])
locationcol.extend(['501 E. FAYETTE STREET BALTIMORE 21202-4092', '501 E. FAYETTE STREET BALTIMORE 21202-4092'])
filingcol.extend(['06/16/2022', '03/23/2022'])
statuscol.extend(['ACTIVE', 'ACTIVE'])

casenumsfordefmap.extend(['010100102112022', '010100047522022'])
lasts.extend(['AUSTIN', 'FINDLEY'])
firsts.extend(['ELLIOTT', 'NICOLE'])
mids.extend(['', ''])
suff.extend(['', ''])
defaddresscol.extend(['4303 ADELLE TERRACE APT 101', '2737 E CHASE STREET'])
citycol.extend(['BALTIMORE', 'BALTIMORE'])
statecol.extend(['MD', 'MD'])
zipcol.extend(['21229', '21213'])

              
defs = pd.DataFrame(
    {"case_number" : casenumsfordefmap,
     "first_name" : firsts,
     "last_name" : lasts,
     "middle" : mids,
     "suffix" : suff,
    "address" : defaddresscol,
    "city" : citycol,
    "state" : statecol,
    "zip" : zipcol}
    )


cases = pd.DataFrame(
    {"case_number" : casenumcol,
     "system" : systemcol,
     "location" : locationcol,
     "filing_date" : filingcol,
     "status" : statuscol}
    )

final = pd.merge(cases, defs, how='left', on='case_number')
final = final.drop_duplicates()

final.to_csv("tuscany_woods_cases.csv", index = False)