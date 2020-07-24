import requests, os, zipfile, shutil, datetime
import pandas as pd

try:
    os.mkdir('Data')
except FileExistsError:
    pass

def download(url):
    get_response = requests.get(url,stream=True)
    file_name  = url.split("/")[-1]
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    with zipfile.ZipFile('./ga_covid_data.zip', 'r') as zip_ref:
        zip_ref.extractall('.')

    os.remove('./ga_covid_data.zip')

    for f in os.listdir():
        if (f.endswith("csv")):
            try:
                shutil.move(f, './Data')
            except shutil.Error:
                os.remove('./Data/{}'.format(f))
                shutil.move(f, './Data')

def getDeaths():
    with open('./Data/deaths.csv', newline='') as csvfile:
        df = pd.read_csv(csvfile)    
        return str(len(df) - 1)

def getTimeStamp():
    time = str(datetime.datetime.now())
    return time[:-7]

def getCases():
    with open('./Data/demographics.csv', newline='') as csvfile:
        df = pd.read_csv(csvfile)
        thing = [i for i in df['Confirmed_Cases']]
        return str(sum(thing))

def logAll(cases, deaths, time):
    with open('./Data/GA_Total_Cases_Log.txt', 'a') as caselog:
        caselog.write(cases + ' Cases :: ' + time + '\n')
    with open('./Data/GA_Deaths_Log.txt', 'a') as deathlog:
        deathlog.write(deaths + ' Deaths :: ' + time + '\n')

def printFormatted(cases, deaths, time):
    returnstr = f"""\n
Georgia Coronavirus Stats \t {time}
Total Cases \t\t\t {cases}
Total Deaths \t\t\t {deaths}
\n"""
    return returnstr

def main():
    download('https://ga-covid19.ondemand.sas.com/docs/ga_covid_data.zip')
    time, deaths, cases = getTimeStamp(), getDeaths(), getCases()
    logAll(cases, deaths, time)
    print(printFormatted(cases, deaths, time))

    with open('./Present_Day_Statistics.txt', 'w') as f:
        f.write(printFormatted('\n' + cases, '\n' + deaths, '\r' + time))


# print('\n\n' + getCases() + getDeaths() + '\n')
if __name__ == '__main__':
    main()
