from bs4 import BeautifulSoup as bs4
import csv
import os
import json
import requests
import urllib.parse

url = "https://survey.stackoverflow.co/2022/#technology"

raw = requests.get(url).text
title = []
data = []
html = bs4(raw, features="lxml")
technology = [
    "technology-most-popular-technologies",
    "technology-most-loved-dreaded-and-wanted",
    #"technology-worked-with-vs-want-to-work-with",
    "technology-top-paying-technologies",
    "technology-version-control",
    "technology-web-3",
]
for t in technology:
    tech = html.find("section", {"id": t})
    graphs = tech.findAll("article", {"class": "mb96 p-ff-source"})

    languages = []
    for g in graphs:
        title.append(g.find("a", {"class": "s-link__inherit"}).text[1:])
        if t == "technology-most-loved-dreaded-and-wanted":
            d = json.loads(g.find("figure").find("div", {"class": "ds-chart"}).attrs['data-json'])
            key_list = []
            val_list = []
            for h in d:
                key_list.append(h['response'])
                val_list.append(h["percent1"]*100)
            key = key_list
            value = val_list
        else:
            key = g.findAll("td", {"class": "label"})
            value = g.findAll("span", {"class": "js-bar-unit js-bar-unit--label"})
            n = len(key)
            for i in range(0, n):
                key[i] = key[i].text
                value[i] = value[i].text

        languages.append(dict(zip(key, map(str, value))))
    j = 0
    
    for l in languages:
        data.append(l)

types = len(title)

with open("survey-2022.csv", 'w', encoding='utf-8') as f:
    for i in range(0, types):
        f.write(f"{title[i]}\n")
        f.write(f"{data[i]}\n")

with open("survey-2022.json", 'w', encoding='utf-8') as f:
    f.write("{\n")
    for i in range(0, types):
        d =json.dumps(data[i], indent=12)
        json_body = f"\n    \"{title[i]}\": {d}"
        if i == types-1:
            json_body += "\n"
        else:
            json_body += ",\n"
        f.write(json_body)
    f.write("\n}")

