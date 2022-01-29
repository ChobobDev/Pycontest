import requests,asyncio,json
from bs4 import BeautifulSoup
from flask import redirect
from functions import stackoverflow as so ,weworkremotely as wwr,remoteok as ro
from datetime import datetime


def requestWithUgerAgent(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.360'}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    return soup

def scrape_all(job_name):
    jobs=asyncio.run(so.get_jobs(job_name))+asyncio.run(wwr.get_jobs(job_name))+asyncio.run(ro.get_jobs(job_name))
    if len(jobs)>0:
        save_json(job_name,jobs)
    return jobs

def return_url(selected_site,job_name):
    site ={"all":"","so":"so","wwr":"wwr","ro":"ro","sowwr":"so&wwr","soro":"so&ro","wwrro":"wwr&ro"}
    return(f"/result/language={job_name}/{site[selected_site]}")

def check_time(language):
    now = datetime.now()
    with open('json/time.json') as json_file:
        data = json.load(json_file)
        if language in data:
            prev_time = datetime.strptime(data[language]["time"], '%Y-%m-%d %H:%M:%S.%f')
            time_dif=int((now-prev_time).total_seconds()//3600)
        else:
            time_dif=10
    return(time_dif)

def load_json(language,sites):
    with open(f'json/{language}.json' , 'r') as f:
        result = json.load(f)
    return result

def save_json(language,jobs):
    now = datetime.now()
    with open(f'json/{language}.json', 'w') as fout:
        json.dump(jobs,fout)
        fout.close()
    with open("json/time.json", "r") as jsonFile:
        data = json.load(jsonFile)
    if language in data:
        data[language]["time"] = str(now)
        with open("json/time.json", "w") as jsonFile:
            json.dump(data, jsonFile)
    else:
        new_language = {f"{language}":{"time":str(now)}}
        with open("json/time.json", "r+") as file:
            data = json.load(file)
            data.update(new_language)
            file.seek(0)
            json.dump(data, file)


