#!/usr/bin/env python3

URL = 'https://support.google.com/chromeosflex/answer/11513094'

import csv
from typing import List
import bs4
import requests
import logging

class Model:
    def __init__(self, name: str, status: str, year: int):
        self.name = name
        self.status = status
        self.year = year

    def __lt__(self, other: 'Model'):
        return self.name < other.name

# Get the list of models from the Google support page
# Note: This was completely auto-generated by Copilot 🤯
def get_models_list() -> List[Model]:
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    models: List[Model] = []
    
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 3:
                model = columns[0].text.strip()
                status = columns[1].text.strip()
                year = int(columns[2].text)
                models.append(Model(model, status, year))
    return models

def write_to_file(models: List[Model]) -> None:
    models.sort()
    certified_models = [model for model in models if model.status == 'Certified']
    certified_models_names = [model.name for model in certified_models]
    # We write certified models
    with open('models.txt', 'w') as f:
        f.write("\n".join(certified_models_names))

    # We write all models
    with open('models.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Model', 'Status', 'Year'])
        for model in models:
            writer.writerow([model.name, model.status, model.year])

def main():
    models = get_models_list()
    write_to_file(models)

if __name__ == '__main__':
    main()
