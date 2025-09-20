import requests

# Список ID интересных компаний
company_ids = [
    4181,
    3529,
    80,
    4233,
    3388,
    205,
    1740,
    208707,
    2460946,
    4219,
]  # Замените на реальные ID

vacancies_data = []

for company_id in company_ids:
    url = f"https://api.hh.ru/vacancies?employer_id={company_id}&per_page=100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies_data.extend(data["items"])

print(vacancies_data)
