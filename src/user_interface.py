from typing import Any


def user_interface(db_manager: Any) -> None:
    while True:
        print("\nДобро пожаловать в систему управления вакансиями!")
        print("Выберите команду:")
        print("1 - Получить количество вакансий по компаниям")
        print("2 - Получить все вакансии")
        print("3 - Получить среднюю зарплату")
        print("4 - Получить вакансии с зарплатой выше средней")
        print("5 - Найти вакансии по ключевому слову")
        print("0 - Выйти")

        choice = input("Введите номер команды: ")

        if choice == "1":
            companies_count = db_manager.get_companies_and_vacancies_count()
            for company, count in companies_count:
                print(f"Компания: {company}, Количество вакансий: {count}")

        elif choice == "2":
            all_vacancies = db_manager.get_all_vacancies()
            for company, title, salary_min, salary_max, url in all_vacancies:
                print(
                    f"Компания: {company}, Вакансия: {title}, Зарплата: {salary_min} - {salary_max}, Ссылка: {url}"
                )

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "4":
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                for company, title, salary_min, salary_max in higher_salary_vacancies:
                    print(
                        f"Компания: {company}, Вакансия: {title}, Зарплата: {salary_min} - {salary_max}"
                    )
            else:
                print("Вакансий с зароботной платой выше средней не найдено.")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                for company, title, salary_min, salary_max in keyword_vacancies:
                    print(
                        f"Компания: {company}, Вакансия: {title}, Зарплата: {salary_min} - {salary_max}"
                    )
            else:
                print("Вакансий с указанным ключевым словом не найдено.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
