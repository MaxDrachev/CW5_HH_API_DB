import requests
from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def get_vacancies(self, employee_id):
        pass


class HHApi(Parser):
    """
    Класс для работы с API HeadHunter
    """
    url: str
    headers: dict
    __params: dict
    vacancies: list

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {
            'text': '',
            'employer_id': '',
            'area': 113,
            'only_with_salary': True,
            'page': 0,
            'per_page': 100
        }
        self.vacancies = []

    def get_vacancies(self, employees_id: list[str]) -> list[dict]:
        """
        Функция получения списка вакансий с api hh, по основному параметру 'text'
        """
        self.__params['employer_id'] = employees_id
        while self.__params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.__params)
            if response.status_code != 200:
                print(f"Ошибка запроса к API: Статус {response.status_code}")
                break
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.__params['page'] += 1

        return self.vacancies

    def get_employers_data(self, employees_id: list[str]) -> list[dict]:
        employers_info = []
        for employer in employees_id:
            url = f'https://api.hh.ru/employers/{employer}'
            response = requests.get(url, headers=self.headers)
            employer_info = {
                'employer_id': response.json()['id'],
                'name': response.json()['name'],
                'alternate_url': response.json()['alternate_url'],
                'open_vacancies': response.json()['open_vacancies']

            }
            employers_info.append(employer_info)
        return employers_info
