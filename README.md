# Geo-Korea-Database

한국 지도 데이터를 Postgresql DB 에 입력

1. 실행되고 있는 PostgreSQL 데이터베이스에 아래 데이터를 생성하는 작업

## 1. 데이터 마이그레이션

### 한국 지도 데이터 출처

- 도로명주소 건물 데이터
  - [Juso.co.kr/건물DB](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=rdnm)

- 기초구역도(우편번호) 지도 데이터
  - [Juso.co.kr/기초구역도](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=bsin)

- 행정구역(시도, 시군구, 읍면동, 리) 지도 데이터
  - [대한민국 최신 행정구역(SHP) 다운로드](http://www.gisdeveloper.co.kr/?p=2332)

### 환경 설정
- npm & mapshaper 설치
```bash
apt install npm
npm install -g mapshaper
```
- python 3.x 설치

```bash
virtualenv --no-site-packages --distribute --python=python3.6 venv
source venv/bin/activate
```

- pip 모듈 설치

```bash
pip install -r requirements.txt
```

### 데이터 생성

0. 데이터 다운로드
- 위 [한국 지도 데이터 출처](#-한국-지도-데이터-출처) 의 3가지 링크에서 데이터 다운로드

1. 건물 데이터 압축파일 해제

```bash
source env.sh

unzip -O cp949 <건물DB.zip 파일 경로> -d $GEO_KR_DATABASE/data/building/
# 예제)
# unzip -O cp949 202007_건물DB_전체분.zip -d $GEO_KR_DATABASE/data/building/
```

2. 지도 데이터 파일 해제
- 기초구역도

```bash
source env.sh

# 압축해제
unzip -O cp949 <기초구역도.zip 파일 경로> -d $GEO_KR_DATABASE/data/shape/base/
mv $GEO_KR_DATABASE/data/shape/base/<기초구역도 폴더>/* $GEO_KR_DATABASE/data/shape/base/
rmdir $GEO_KR_DATABASE/data/shape/base/<기초구역도 폴더>
# 예제)
# unzip -O cp949 201912기초구역DB_전체분.zip -d $GEO_KR_DATABASE/data/shape/base/
# mv $GEO_KR_DATABASE/data/shape/base/201912기초구역DB_전체분/* $GEO_KR_DATABASE/data/shape/base/
# rmdir $GEO_KR_DATABASE/data/shape/base/201912기초구역DB_전체분

# 시도별 기초구역도 데이터 병합
mapshaper -i $GEO_KR_DATABASE/data/shape/base/*/*.shp snap combine-files encoding=cp949  \
          -merge-layers name=merged-layers \
          -simplify weighted 0.5% \
          -o $GEO_KR_DATABASE/data/shape/base/KOREA_BASE.shp format=shapefile target=merged-layers

# 한국 기초구역도 데이터 샘플링
mapshaper -i $GEO_KR_DATABASE/data/shape/base/KOREA_BASE.shp encoding=cp949 \
          -simplify weighted 0.5% \
          -o $GEO_KR_DATABASE/data/shape/base/KOREA_BASE_SIMPLIFY.shp format=shapefile
```

- 행정구역

```bash
source env.sh
mkdir -p $GEO_KR_DATABASE/data/shape/sigudong/

unzip -O cp949 <시,구,동 별.zip 파일 경로> -d $GEO_KR_DATABASE/data/shape/sigudong/
# 예제)
# unzip -O cp949 CTPRVN_202005.zip -d $GEO_KR_DATABASE/data/shape/sigudong/

# 행정구역 지도 데이터 샘플링
mapshaper -i $GEO_KR_DATABASE/data/shape/sigudong/<CTPRVN|SIG|EMD|LI>.shp encoding=cp949 \
          -simplify weighted 0.5% \
          -o $GEO_KR_DATABASE/data/shape/sigudong/<CTPRVN|SIG|EMD|LI>_SIMPLIFY.shp format=shapefile

# 예제)
# mapshaper -i $GEO_KR_DATABASE/data/shape/sigudong/CTPRVN.shp encoding=cp949 \
#           -simplify weighted 0.5% \
#           -o $GEO_KR_DATABASE/data/shape/sigudong/CTPRVN_SIMPLIFY.shp format=shapefile
```

### DB 로 데이터 입력

```bash
# 건물 데이터 입력
python src/building_tables.py --op <operation> --host <host> --port <port> --user <db user> --password <db user passwd> --database <database name>

# 지리 데이터 입력
python src/jiri_tables_simplify.py --op <operation> --host <host> --port <port> --user <db user> --password <db user passwd> --database <database name>

# 행정구역 별 지리 매핑 데이터 입력
python src/dministractive_district_tables_simplify.py --op <operation> --host <host> --port <port> --user <db user> --password <db user passwd> --database <database name>
```
