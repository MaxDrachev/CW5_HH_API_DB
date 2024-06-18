import os
import psycopg2
from config import config
from src.classes.DB_conn import DBConnection
from src.classes.class_DBM import DBManager
from src.classes.class_APIhh import HHApi
from src.func_for_main import get_employees_id_by_input_user, get_id_employees, create_tables, add_employers, \
    add_vacancies, truncate_table


def main():
    hh_1 = HHApi()
    db_param = config()
    db_conn = DBConnection(**db_param).conn
    create_tables(db_conn)
    list_eml = get_employees_id_by_input_user()
    eml_id = get_id_employees(list_eml)
    emp_1 = hh_1.get_employers_data(eml_id)
    add_employers(db_conn, emp_1)
    vac = hh_1.get_vacancies(eml_id)
    add_vacancies(db_conn, vac)
    dbm_1 = DBManager(db_conn)

    #print(dbm_1.get_all_vacancies())

    # list_eml = get_employees_id_by_input_user()
    # eml_id = get_id_employees(list_eml)

if __name__ == '__main__':
    main()