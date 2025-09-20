import psycopg2

from src.hh_api import vacancies_data

# Настройки подключения к БД
conn = psycopg2.connect(
    dbname="courseproject3",
    user="postgres",
    password="191979",
    host="localhost",
    port="5432",
)

cursor = conn.cursor()

# Сохранение компаний
for company in vacancies_data:
    cursor.execute(
        "INSERT INTO company (company_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        (
            company["employer"]["id"],
            company["employer"]["name"],
            company["employer"]["url"],
        ),
    )

# Сохранение вакансий
for vacancy in vacancies_data:
    if vacancy.get("salary") is not None:
        cursor.execute(
            "INSERT INTO vacancy (title, salary_min, salary_max, currency, company_id, url) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                vacancy["name"],
                vacancy.get("salary", {}).get("from"),
                vacancy.get("salary", {}).get("to"),
                vacancy.get("salary", {}).get("currency"),
                vacancy["employer"]["id"],
                vacancy["alternate_url"],
            ),
        )

# Фиксация изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()
