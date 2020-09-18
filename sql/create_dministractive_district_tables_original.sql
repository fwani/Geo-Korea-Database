DROP INDEX IF EXISTS 행정구역_우편번호_INDEX;
DROP INDEX IF EXISTS 행정구역_읍면동_INDEX;
DROP INDEX IF EXISTS 행정구역_시군구_INDEX;
DROP INDEX IF EXISTS 행정구역_시도_INDEX;

DROP TABLE IF EXISTS 행정구역_우편번호;
DROP TABLE IF EXISTS 행정구역_읍면동;
DROP TABLE IF EXISTS 행정구역_시군구;
DROP TABLE IF EXISTS 행정구역_시도;

CREATE TABLE IF NOT EXISTS 행정구역_시도 (
    시도명 text,
    영문시도명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명)
);
CREATE INDEX IF NOT EXISTS 행정구역_시도_INDEX ON 행정구역_시도 (시도명);

CREATE TABLE IF NOT EXISTS 행정구역_시군구 (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명, 시군구명),
    FOREIGN KEY (시도명) REFERENCES 행정구역_시도 (시도명)
);
CREATE INDEX IF NOT EXISTS 행정구역_시군구_INDEX ON 행정구역_시군구 (시도명, 시군구명);

CREATE TABLE IF NOT EXISTS 행정구역_읍면동 (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    읍면동명 text,
    영문읍면동명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명, 시군구명, 읍면동명),
    FOREIGN KEY (시도명, 시군구명) REFERENCES 행정구역_시군구 (시도명, 시군구명)
);
CREATE INDEX IF NOT EXISTS 행정구역_읍면동_INDEX ON 행정구역_읍면동 (시도명, 시군구명, 읍면동명);

CREATE TABLE IF NOT EXISTS 행정구역_우편번호 (
    시도명 text,
    시군구명 text,
    읍면동명 text,
    우편번호 text,
    건축물대장_건물명 text,
    상세건물명 text,
    시군구용_건물명 text,
    GEOMETRY text,
    CENTER_COORDINATES text
);
CREATE INDEX IF NOT EXISTS 행정구역_우편번호_INDEX ON 행정구역_우편번호 (우편번호);
