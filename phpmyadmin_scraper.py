import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


url_base = "http://185.244.219.162/phpmyadmin"
login_url = f"{url_base}/index.php"
table_url = (
    f"{url_base}/index.php?route=/sql&server=1&db=testDB&table=users&pos=0"
)

username = "test"
password = "JHFBdsyf2eg8*"

session = requests.Session()

# Получаем токен
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, "html.parser")
token_input = soup.find("input", {"name": "token"})
token = token_input["value"] if token_input else ""

# Логинимся
payload = {
    "pma_username": username,
    "pma_password": password,
    "server": 1,
    "target": "index.php",
    "token": token
}
response = session.post(login_url, data=payload)

if "phpMyAdmin" not in response.text:
    print("Ошибка входа")
    exit()
print("Успешный вход")

# Запрос таблицы
table_page = session.get(table_url)
soup = BeautifulSoup(table_page.text, "html.parser")

headers = [th["data-column"] for th in soup.select(
    "table.data thead th"
    ) if th.has_attr("data-column")]

# Выводим содержимое таблицы
rows = soup.select("table.data tbody tr")
print("📋 Содержимое таблицы users:")
table_data = []
for row in rows:
    columns = [td.text.strip() for td in row.select("td")][4:]
    if columns:
        table_data.append(columns)

if table_data:
    print(tabulate(
        table_data,
        headers=headers,
        tablefmt="grid"
    ))
else:
    print("Данные не найдены")