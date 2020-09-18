import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json


def create_tables(cur, home):
    # create tables
    print("Start to create building tables")
    cur.execute(open(os.path.join(home, 'sql/create_building_tables.sql'), 'r').read())


def insert_datas(cur, home):
    downloaded_files = glob.glob(os.path.join(home, 'data/building/*.txt'))

    prefix = {
        0: 'road_code_',
        1: 'build_',
        2: 'jibun_',
    }

    sorted_files = []
    for f in downloaded_files:
        for k, v in prefix.items():
            if re.search(v, f) is not None:
                sorted_files.append((k, f))

    sorted_files = sorted(sorted_files, key=lambda x: x[0])

    base_insert_sql = "INSERT INTO {0} VALUES {1}"

    for k, f_path in sorted_files:
        print("Read data from [{}]".format(f_path))
        if k == 0:
            table = '도로명코드'
        elif k == 1:
            table = '건물정보'
        elif k == 2:
            table = '관련지번'
        else:
            continue

        csv_reader = csv.reader(open(f_path, 'r', encoding='cp949'), delimiter='|')
        all_rows = []
        print("Create sql query ...")
        for row in csv_reader:
            row = [None if r == '' else r.strip() for r in row]
            value_format = "(" + ', '.join(['%s'] * len(row)) + ")"
            all_rows.append(cur.mogrify(value_format, row).decode('utf-8'))
            if len(all_rows) % 100000 == 0:
                print("Sample data: {}".format(all_rows[:5]))
                print("Insert data ...")
                cur.execute(base_insert_sql.format(table, ','.join(all_rows)))
                all_rows = []
        if len(all_rows) != 0:
            print("Sample data: {}".format(all_rows[:5]))
            print("Insert data ...")
            cur.execute(base_insert_sql.format(table, ','.join(all_rows)))

    # 세종특별자치시는 시군구 단위가 없기 때문에 None 으로 들어가지만, 다른 시도와 데이터를 맞추기 위해서 string 으로 변경
    cur.execute("""
        UPDATE 도로명코드
        SET 시군구명 = ''
        WHERE 시도명 = '세종특별자치시'
    """)


def run(args):
    dbname = args.database
    print("Connect Database [{}]".format(dbname))
    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=dbname)
    cur = conn.cursor()
    conn.autocommit = True

    home = os.getenv('GEO_KR_DATABASE')

    op = args.op
    if op == 1:
        create_tables(cur, home)
    elif op == 2:
        insert_datas(cur, home)
    elif op == 3:
        create_tables(cur, home)
        insert_datas(cur, home)

    cur.close()
    conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Insert juso data to PostgreSQL')

    parser.add_argument('--op',
                        required=True,
                        type=int,
                        help='What do you want to do?\nInsert number. (1. create table, 2. insert datas, 3. create&insert)')
    parser.add_argument('--host',
                        required=True,
                        type=str,
                        help='PostgreSQL host')
    parser.add_argument('--port',
                        required=True,
                        type=str,
                        help='PostgreSQL port')
    parser.add_argument('--user',
                        required=True,
                        type=str,
                        help='PostgreSQL user')
    parser.add_argument('--password',
                        required=True,
                        type=str,
                        help='PostgreSQL password')
    parser.add_argument('--database',
                        required=True,
                        type=str,
                        help='PostgreSQL database name')

    parsed_args = parser.parse_args()
    print(parsed_args)
    run(parsed_args)
