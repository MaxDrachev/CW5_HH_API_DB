from abc import ABC, abstractmethod


class AbstractDBM(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword):
        pass


class DBManager(AbstractDBM):

    def __init__(self, db_conn):
        self.conn = db_conn

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT employers.name, COUNT(*) FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.id
                GROUP BY employers.name
                ORDER BY COUNT(*) DESC
                """)

            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
        ссылки на вакансию
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """SELECT employers.name as employer_name , vacancies.name as vacancie_name, vacancies.url, 
                vacancies.salary_min, vacancies.salary_max  FROM vacancies INNER JOIN employers ON 
                vacancies.employer_id = employers.id;"""
            )

            return cursor.fetchall()

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям # среднюю по min и max
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(salary_min) as avg_salary_min, AVG(salary_max) as avg_salary_max FROM vacancies;
                """
            )

            return cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM vacancies
                WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies)
                ORDER BY salary_min DESC;
                """)

            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python
        :param keyword:
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM vacancies WHERE name LIKE ('{keyword}%');""")

            return cursor.fetchall()
