import sqlite3
import requests
import json
import sys


conn = sqlite3.connect('carbis_db.db')
cur = conn.cursor()

def find_address(resource, query):
    select = '''SELECT * FROM secret_data'''
    cursor = conn.cursor()
    cursor.execute(select)
    conn.commit()
    show_data = cursor.fetchall()
    cursor.close()
    for i in show_data:
        BASE_URL = i[1]
        API_KEY = i[2]
        language = i[3]
    url = BASE_URL + resource
    headers = {
        'Authorization': 'Token ' + API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'query': query,
        'language': language
    }
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return result.json()

# Сортировка найденых адресов
def sort_address(data):
    sorted_addresses = {}
    a = 1
    try:
        for row in data['suggestions']:
            addresses = {}
            addresses['value'] = str(row['value'])
            addresses['geo_lat'] = row['data']['geo_lat']
            addresses['geo_lon'] = row['data']['geo_lon']
            sorted_addresses[a] = addresses
            a += 1
    except KeyError as e:
        print(f"Возникла ошибка {e}")

    return sorted_addresses
while True:
    print('Выход - exit')
    print('-----------------------------------------------------------------')
    print('Введите адрес ниже ')
    stdin_fileno = sys.stdin
    for line in stdin_fileno:
        if line.strip() == 'exit':
            conn.close()
            exit(0)
        else:
            data = find_address('address', line)
            result = sort_address(data)
            for i in result:
                print(str(i) + ' - ' + str(result[i]['value']))
            while True:
                try:
                    number = int(input("Введите порядковый номер вашего адреса => "))
                    if number in result:
                        print(str(result[number]['value'] + ': широта - ' + str(
                            result[number]['geo_lat']) + '; долгота - ' + str(result[number]['geo_lon']) + '\n'))
                        break
                    else:
                        print("Порядковый номер отсутствует в списке")
                except ValueError:
                    print("Введите порядковый номер вашего адреса => ")
    break
