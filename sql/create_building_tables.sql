DROP INDEX IF EXISTS 관련지번_INDEX;
DROP INDEX IF EXISTS 건물정보_INDEX;
DROP INDEX IF EXISTS 도로명코드_INDEX;

DROP TABLE IF EXISTS 관련지번;
DROP TABLE IF EXISTS 건물정보;
DROP TABLE IF EXISTS 도로명코드;

CREATE TABLE IF NOT EXISTS 도로명코드 (
    시군구코드 text,
    도로명번호 text,
    도로명 text,
    영문도로명 text,
    읍면동일련번호 text,
    시도명 text,
    시군구명 text,
    읍면동구분 text,	
    읍면동코드 text,	
    읍면동명 text,
    상위도로명번호 text,
    상위도로명 text,
    사용여부 text,
    변경이력사유 text,
    변경이력정보 text,
    영문시도명 text,
    영문시군구명 text,
    영문읍면동명 text,
    고시일자 text,
    말소일자 text,
    PRIMARY KEY (시군구코드, 도로명번호, 읍면동일련번호)
);
CREATE INDEX IF NOT EXISTS 도로명코드_INDEX ON 도로명코드 (시군구코드, 도로명번호, 읍면동일련번호);

CREATE TABLE IF NOT EXISTS 건물정보 (
    법정동코드 text,
    시도명 text,
    시군구명 text,
    법정읍면동명 text,
    법정리명 text,
    산여부 text,
    지번본번 integer,
    지번부번 integer,
    도로명코드 text,
    도로명 text,
    지하여부 text,
    건물본번 integer,
    건물부번 integer,
    건축물대장_건물명 text,
    상세건물명 text,
    건물관리번호 text PRIMARY KEY,
    읍면동일련번호 text,
    행정동코드 text,
    행정동명 text,
    우편번호 text,
    우편일련번호 text,
    다량배달처명 text,
    이동사유코드 text,
    고시일자 text,
    변동전도로명주소 text,
    시군구용_건물명 text,
    공동주택여부 text,
    기초구역번호 text,
    상세주소여부 text,
    비고1 text,
    비고2 text
);
CREATE INDEX IF NOT EXISTS 건물정보_INDEX ON 건물정보 (건물관리번호);

CREATE TABLE IF NOT EXISTS 관련지번 (
    법정동코드 text,
    시도명 text,
    시군구명 text,
    법정읍면동명 text,
    법정리명 text,
    산여부 text,
    지번본번 integer,
    지번부번 integer,
    도로명코드 text,
    지하여부 text,
    건물본번 integer,
    건물부번 integer,
    지번일련번호 integer,
    이동사유코드 text,
    PRIMARY KEY (도로명코드, 지하여부, 건물본번, 건물부번, 지번일련번호)
);
CREATE INDEX IF NOT EXISTS 관련지번_INDEX ON 관련지번 (도로명코드, 지하여부, 건물본번, 건물부번, 지번일련번호);
