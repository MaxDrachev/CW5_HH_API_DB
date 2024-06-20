from data.config import config
from src.classes.DB_conn import DBConnection
from src.classes.class_DBM import DBManager
from src.classes.class_APIhh import HHApi
from src.func_for_main import get_employees_id_by_input_user, get_id_employees, create_tables, add_employers, \
    add_vacancies, drop_table


def main():
    hh_1 = HHApi()
    db_param = config()
    db_conn = DBConnection(**db_param).conn
    drop_table(db_conn)
    create_tables(db_conn)
    list_eml = get_employees_id_by_input_user()
    eml_id = get_id_employees(list_eml)
    emp_1 = hh_1.get_employers_data(eml_id)
    add_employers(db_conn, emp_1)
    vacancie = hh_1.get_vacancies(eml_id)
    add_vacancies(db_conn, vacancie)
    dbm_1 = DBManager(db_conn)

    print(dbm_1.get_avg_salary())
    for i in dbm_1.get_vacancies_with_higher_salary():
        print(i)
    print(dbm_1.get_companies_and_vacancies_count())
    print(dbm_1.get_vacancies_with_keyword('Водитель'))
    for i in dbm_1.get_all_vacancies():
        print(i)


if __name__ == '__main__':
    main()
