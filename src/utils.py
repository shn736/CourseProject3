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
        "INSERT INTO companies (name, url) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (company["employer"]["name"], company["employer"]["url"]),
    )

# Сохранение вакансий
for vacancy in vacancies_data:
    if vacancy.get("salary") is not None:
        cursor.execute(
            "INSERT INTO vacancies (title, salary_min, salary_max, currency, company_id, url) VALUES (%s, %s, %s, %s, (SELECT id FROM companies WHERE name=%s LIMIT 1), %s)",
            (
                vacancy["name"],
                vacancy.get("salary", {}).get("from"),
                vacancy.get("salary", {}).get("to"),
                vacancy.get("salary", {}).get("currency"),
                vacancy["employer"]["name"],
                vacancy["alternate_url"],
            ),
        )

# Фиксация изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()
