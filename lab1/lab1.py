from bs4 import BeautifulSoup
from requests import get
from json import dump

BASE_URL = 'https://lpnu.ua/'
page = get(BASE_URL)
soup = BeautifulSoup(page.content, 'html.parser')

institutes_array = soup.find(class_='navbar-nav').find(class_='expanded dropdown').find('ul').find_all('a')

lpnu = []

with open('lpnu.txt', 'w', encoding='UTF-8') as file:
    for inst in institutes_array:
        file.write(f'{inst.getText()}\n')
        inst_page = get(BASE_URL + inst.get('href'))
        inst_soup = BeautifulSoup(inst_page.content, 'html.parser')
        directors = inst_soup.find(class_='field field--name-field-contact-person field--type-string field--label-hidden field--items').find_all(class_='field--item')
        file.write('  Деканат\n')

        instute = {
            'name': inst.getText(),
            'staff': [],
            'departments': []
        }

        for dir in directors:
            file.write(f'    {dir.getText()}\n')
            instute['staff'].append(dir.getText())

        try:
            departments = inst_soup.find(id='block-views-block-group-subgroups-block-1').find(class_='item-list').find_all('a')
        except AttributeError:
            continue

        file.write('  Кафедри\n')

        for dep in departments:
            file.write(f'    {dep.getText()}\n')

            department = {
                'name': dep.getText(),
                'scientists': []
            }

            dep_page = get(dep.get('href').strip())
            dep_soup = BeautifulSoup(dep_page.content, 'html.parser')
            dep_arr = dep_soup.find(class_="field field--name-field-contact-person field--type-string field--label-hidden field--items").find_all(class_="field--item")

            file.write(f'      Працівники кафедри\n')

            for a in dep_arr:
                file.write(f'        {a.getText()}\n')
                department['scientists'].append(a.getText())

            instute['departments'].append(department)

        lpnu.append(instute)

with open('lpnu.json', 'w', encoding='utf-8') as json:
    dump(lpnu, json, ensure_ascii=False, indent=4)