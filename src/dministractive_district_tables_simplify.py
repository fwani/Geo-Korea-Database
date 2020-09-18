import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json
import geopandas as gpd
import pandas as pd


def create_tables(cur, home):
    # create tables
    print("Create tables")
    cur.execute(open(os.path.join(home, 'sql/create_dministractive_district_tables_simplify.sql'), 'r').read())

def insert_datas(cur, home):
    # create tables
    print("insert data")
    cur.execute(open(os.path.join(home, 'sql/insert_dministractive_district_tables_simplify.sql'), 'r').read())

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
