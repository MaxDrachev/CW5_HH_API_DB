import os
import psycopg2
from abc import ABC, abstractmethod
from src.func_for_main import create_tables
from src.classes.DB_conn import DBConnection


class AbstractDBM(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):  # получает список всех компаний и количество вакансий у каждой компании
        pass

    @abstractmethod
    def get_all_vacancies(self):  # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        pass

    @abstractmethod
    def get_avg_salary(self):  # получает среднюю зарплату по вакансиям
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(
            self):  # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):  # получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        pass


class DBManager(AbstractDBM):
    def __init__(self, params: dict):
        self.conn = psycopg2.connect(
            database=params['name'],
            user=params['user'],
            password=params['password'],
            host=params['host'],
            port=params['port']
        )

    def get_companies_and_vacancies_count(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                """
        SELECT employer_id, COUNT(*) FROM vacancies
        GROUP BY employer_id
        ORDER BY COUNT(*) DESC
        """)

            return cursor.fetchall()

    def get_all_vacancies(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM vacancies;
                """
            )

            return cursor.fetchall()

    def get_avg_salary(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(salary_min) as avg_salary_min, AVG(salary_max) as avg_salary_max FROM vacancies;
                """
            )

            return cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                """
        SELECT * FROM vacancies
        WHERE salary_min IS NOT NULL 
        ORDER BY salary_min DESC
        LIMIT 10;
        """)

            return cursor.fetchall()

    def get_vacancies_with_keyword(self):
        keyword = input()
        with self.db_conn.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM vacancies WHERE name LIKE ('%{keyword}%');""")

            return cursor.fetchall()


if __name__ == '__main__':
    db_conn = DBConnection(
        name='CW5_Drachev',
        user='postgres',
        port=5432,
        host='localhost',
        password='173O613cc,'
        ).conn

    dbm_1 = DBManager(db_conn)
    print(dbm_1.get_companies_and_vacancies_count())

