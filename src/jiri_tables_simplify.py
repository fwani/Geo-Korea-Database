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
    cur.execute(open(os.path.join(home, 'sql/create_jiri_tables_simplify.sql'), 'r').read())


def insert_table(cur, df, base_insert_sql, table_name):
    df = df.dropna(subset=['geometry'])
    df['geometry'].crs = 5179
    df['geometry'] = df['geometry'].to_crs(4326)
    all_rows = []
    print("Create sql query ...")
    for row in df.to_numpy():
        tmp = [r.strip() for r in row[:-1]]
        geometry = row[-1].wkt
        cent = row[-1].centroid.wkt

        row = tmp + [geometry, cent]

        value_format = "(" + ', '.join(['%s'] * len(row)) + ")"
        all_rows.append(cur.mogrify(value_format, row).decode('utf-8'))
    print("Insert Data ...")
    cur.execute(base_insert_sql.format(table_name, ','.join(all_rows)))


def insert_datas(cur, home):

    # 샘플링된 geometry가 삭제되는 경우가 있어, 삭제된 경우에는 원본 geometry를 사용
    si_file_original = os.path.join(home, 'data/shape/sigudong/CTPRVN.shp')
    gu_file_original = os.path.join(home, 'data/shape/sigudong/SIG.shp')
    dong_file_original = os.path.join(home, 'data/shape/sigudong/EMD.shp')
    zipcode_file_original = os.path.join(home, 'data/shape/base/KOREA_BASE.shp')

    si_file = os.path.join(home, 'data/shape/sigudong/CTPRVN_SIMPLIFY.shp')
    gu_file = os.path.join(home, 'data/shape/sigudong/SIG_SIMPLIFY.shp')
    dong_file = os.path.join(home, 'data/shape/sigudong/EMD_SIMPLIFY.shp')
    zipcode_file = os.path.join(home, 'data/shape/base/KOREA_BASE_SIMPLIFY.shp')

    category_columns = {
        'CTP': ['CTPRVN_CD', 'CTP_ENG_NM', 'geometry'],
        'SIG': ['SIG_CD', 'SIG_ENG_NM', 'geometry'],
        'EMD': ['EMD_CD', 'EMD_ENG_NM', 'geometry'],
        'ZIPCODE': ['CTP_KOR_NM', 'SIG_KOR_NM', 'BAS_ID', 'geometry']
    }

    table_name_keys = {
        'CTP': '지리_시도_SIMPLIFY',
        'SIG': '지리_시군구_SIMPLIFY',
        'EMD': '지리_읍면동_SIMPLIFY',
        'ZIPCODE': '지리_우편번호_SIMPLIFY'
    }

    si_df_original = gpd.read_file(si_file_original, sep='|', encoding='cp949')[category_columns['CTP']]
    # 데이터에 전라남도 영문이 잘 못 표기되어 임의로 변경
    si_df_original.loc[si_df_original['CTP_ENG_NM'] == 'Jellanam-do', 'CTP_ENG_NM'] = 'Jeollanam-do'
    gu_df_original = gpd.read_file(gu_file_original, sep='|', encoding='cp949')[category_columns['SIG']]
    dong_df_original = gpd.read_file(dong_file_original, sep='|', encoding='cp949')[category_columns['EMD']]
    zipcode_df_original = gpd.read_file(zipcode_file_original, sep='|', encoding='utf-8')[category_columns['ZIPCODE']]

    base_insert_sql = "INSERT INTO {} VALUES {}"

    # 시도 데이터 입력
    print("Start insert 지리_시도 data.")

    si_df = gpd.read_file(si_file, sep='|', encoding='cp949')[category_columns['CTP']]
    # 데이터에 전라남도 영문이 잘 못 표기되어 임의로 변경
    si_df.loc[si_df['CTP_ENG_NM'] == 'Jellanam-do', 'CTP_ENG_NM'] = 'Jeollanam-do'

    insert_table(cur, si_df[['CTP_ENG_NM', 'geometry']], base_insert_sql, table_name_keys['CTP'])

    # 시군구 데이터 입력
    print("Start insert 지리_시군구 data.")

    gu_df = gpd.read_file(gu_file, sep='|', encoding='cp949')[category_columns['SIG']]
    non_geometry_df = gu_df[gu_df['geometry'] == None]
    if len(non_geometry_df) > 0:
        geometry_df = gu_df[gu_df['geometry'] != None]
        non_geometry_df['geometry'] = gu_df_original[gu_df['geometry'] == None]['geometry'].values
        gu_df = pd.concat([geometry_df, non_geometry_df]).sort_index()
    result_gu_df = None
    for row in si_df[['CTPRVN_CD', 'CTP_ENG_NM']].to_numpy():
        tmp = gu_df[gu_df['SIG_CD'].str.startswith(row[0])]
        tmp['CTP_ENG_NM'] = row[1]
        if result_gu_df is None:
            result_gu_df = tmp
        else:
            result_gu_df = pd.concat([result_gu_df,tmp], ignore_index=True)
    insert_table(cur, result_gu_df[['CTP_ENG_NM', 'SIG_ENG_NM', 'geometry']], base_insert_sql, table_name_keys['SIG'])

    # 읍면동 데이터 입력
    print("Start insert 지리_읍면동 data.")

    dong_df = gpd.read_file(dong_file, sep='|', encoding='cp949')[category_columns['EMD']]
    non_geometry_df = dong_df[dong_df['geometry'] == None]
    if len(non_geometry_df) > 0:
        geometry_df = dong_df[dong_df['geometry'] != None]
        non_geometry_df['geometry'] = dong_df_original[dong_df['geometry'] == None]['geometry'].values
        dong_df = pd.concat([geometry_df, non_geometry_df]).sort_index()
    result_dong_df = None
    for row in result_gu_df[['SIG_CD', 'SIG_ENG_NM', 'CTP_ENG_NM']].to_numpy():
        tmp = dong_df[dong_df['EMD_CD'].str.startswith(row[0])]
        tmp['SIG_ENG_NM'] = row[1]
        tmp['CTP_ENG_NM'] = row[2]
        if result_dong_df is None:
            result_dong_df = tmp
        else:
            result_dong_df = pd.concat([result_dong_df,tmp], ignore_index=True)
    insert_table(cur, result_dong_df[['CTP_ENG_NM', 'SIG_ENG_NM', 'EMD_ENG_NM', 'geometry']], base_insert_sql, table_name_keys['EMD'])

    # 우편번호 데이터 입력
    print("Start insert 지리_우편번호 data.")
    zipcode_df = gpd.read_file(zipcode_file, sep='|', encoding='utf-8')[category_columns['ZIPCODE']]
    non_geometry_df = zipcode_df[zipcode_df['geometry'] == None]
    if len(non_geometry_df) > 0:
        geometry_df = zipcode_df[zipcode_df['geometry'] != None]
        non_geometry_df['geometry'] = zipcode_df_original[zipcode_df['geometry'] == None]['geometry'].values
        zipcode_df = pd.concat([geometry_df, non_geometry_df]).sort_index()
    insert_table(cur, zipcode_df, base_insert_sql, table_name_keys['ZIPCODE'])


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
