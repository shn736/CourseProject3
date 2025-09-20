from typing import Any

import psycopg2


class DBManager:
    def __init__(self, dbname: Any, user: Any, password: Any, host: str ="localhost", port: str ="5432") -> None:
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> Any:
        """получает список всех компаний и количество вакансий у каждой компании"""
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.id)
            FROM company c
            LEFT JOIN vacancy v ON c.company_id  = v.company_id
            GROUP BY c.name
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> Any:
        """получает список всех вакансий"""
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancy v
            JOIN company c ON v.company_id = c.id
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Any:
        """получает среднюю зарплату по вакансиям"""
        self.cursor.execute(
            """
            SELECT AVG((v.salary_min + v.salary_max)/2)
            FROM vacancy v
            WHERE v.salary_min IS NOT NULL AND v.salary_max IS NOT NULL
        """
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> Any:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_min, v.salary_max
            FROM vacancy v
            JOIN company c ON v.company_id = c.id
            WHERE (v.salary_min + v.salary_max) / 2 > %s
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: Any) -> Any:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_min, v.salary_max
            FROM vacancy v
            JOIN company c ON v.company_id = c.company_id
            WHERE v.title ILIKE %s
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()
