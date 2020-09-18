DROP INDEX IF EXISTS 행정구역_우편번호_SIMPLIFY_INDEX;
DROP INDEX IF EXISTS 행정구역_읍면동_SIMPLIFY_INDEX;
DROP INDEX IF EXISTS 행정구역_시군구_SIMPLIFY_INDEX;
DROP INDEX IF EXISTS 행정구역_시도_SIMPLIFY_INDEX;

DROP TABLE IF EXISTS 행정구역_우편번호_SIMPLIFY;
DROP TABLE IF EXISTS 행정구역_읍면동_SIMPLIFY;
DROP TABLE IF EXISTS 행정구역_시군구_SIMPLIFY;
DROP TABLE IF EXISTS 행정구역_시도_SIMPLIFY;

CREATE TABLE IF NOT EXISTS 행정구역_시도_SIMPLIFY (
    시도명 text,
    영문시도명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명)
);
CREATE INDEX IF NOT EXISTS 행정구역_시도_SIMPLIFY_INDEX ON 행정구역_시도_SIMPLIFY (시도명);

CREATE TABLE IF NOT EXISTS 행정구역_시군구_SIMPLIFY (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명, 시군구명),
    FOREIGN KEY (시도명) REFERENCES 행정구역_시도_SIMPLIFY (시도명)
);
CREATE INDEX IF NOT EXISTS 행정구역_시군구_SIMPLIFY_INDEX ON 행정구역_시군구_SIMPLIFY (시도명, 시군구명);

CREATE TABLE IF NOT EXISTS 행정구역_읍면동_SIMPLIFY (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    읍면동명 text,
    영문읍면동명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (시도명, 시군구명, 읍면동명),
    FOREIGN KEY (시도명, 시군구명) REFERENCES 행정구역_시군구_SIMPLIFY (시도명, 시군구명)
);
CREATE INDEX IF NOT EXISTS 행정구역_읍면동_SIMPLIFY_INDEX ON 행정구역_읍면동_SIMPLIFY (시도명, 시군구명, 읍면동명);

CREATE TABLE IF NOT EXISTS 행정구역_우편번호_SIMPLIFY (
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
CREATE INDEX IF NOT EXISTS 행정구역_우편번호_SIMPLIFY_INDEX ON 행정구역_우편번호_SIMPLIFY (우편번호);
