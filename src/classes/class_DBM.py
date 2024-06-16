import psycopg2
from abc import ABC, abstractmethod
from src.func_for_main import create_tables
from src.classes.DB_conn import DBConnection


class AbstractDBM(ABC):


    @abstractmethod
    def get_companies_and_vacancies_count(self):  # получает список всех компаний и количество вакансий у каждой компании
        pass

    @abstractmethod
    def get_all_vacancies(
            self):  # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        pass

    @abstractmethod
    def get_avg_salary(self):  # получает среднюю зарплату по вакансиям
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(
            self):  # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        pass

    @abstractmethod
    def get_vacancies_with_keyword(
            self):  # получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        pass


class DBManager(AbstractDBM):

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass




if __name__ == '__main__':
    db_conn = DBConnection(
        name='CW5_Drachev',
        user='postgres',
        port=5432,
        host='localhost',
        password='173O613cc,'
        ).conn

    create_tables(db_conn)

