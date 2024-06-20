from typing import Any
import requests


def create_tables(db_conn) -> None:
    """
    данная функция создает таблички в уже созданной базе данных на локальном компьютере
    :param db_conn:
    :return:
    """
    with db_conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
        id INT PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        url VARCHAR(200) NOT NULL,
        open_vacancies INT);
        """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                id INT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                url VARCHAR(200) NOT NULL,
                employer_id INT NOT NULL REFERENCES employers(id),
                salary_min INT,
                salary_max INT);
                """)

        db_conn.commit()


def drop_table(db_conn) -> None:
    """
    данная функция создает таблички в уже созданной базе данных на локальном компьютере
    :param db_conn:
    :return:
    """
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            DROP TABLE IF EXISTS employers, vacancies CASCADE;
            """)

        db_conn.commit()


def get_employees_id_by_input_user() -> list[str]:
    """
    Получает список работодателей для поиска их вакансий
    """
    employees = []
    while len(employees) < 10:
        param_text = input('Введите желаемых работодателей:  ')
        employees.append(param_text)

    return employees


def get_id_employees(employees: list[str]) -> list[str]:
    headers = {'User-Agent': 'HH-User-Agent'}
    params = {'text': '', 'sort_by': 'by_vacancies_open'}
    url = 'https://api.hh.ru/employers'
    employees_id = []
    for employer in employees:
        params['text'] = employer
        response = requests.get(url, params, headers=headers)
        search_result = response.json().get('items', [])
        if search_result:
            employees_id.append(search_result[0].get('id', ''))

    return employees_id


def add_vacancies(db_conn, vacancies_list: list[dict]):
    with db_conn.cursor() as cursor:
        for vac in vacancies_list:
            cursor.execute(
                """
                INSERT INTO vacancies(id, name, url, employer_id, salary_min, salary_max)
                VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    vac['id'],
                    vac['name'],
                    vac['url'],
                    vac['employer']['id'],
                    vac['salary']['from'],
                    vac['salary']['to'],
                )
            )
            db_conn.commit()


def add_employers(db_conn, employers_list: list[dict]):
    with db_conn.cursor() as cursor:
        for employer in employers_list:
            cursor.execute(
                """
                INSERT INTO employers(id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s);
                """, (
                    employer['employer_id'],
                    employer['name'],
                    employer['alternate_url'],
                    employer['open_vacancies'],
                )
            )
            db_conn.commit()
