DROP TABLE IF EXISTS 지리_우편번호;
DROP TABLE IF EXISTS 지리_읍면동;
DROP TABLE IF EXISTS 지리_시군구;
DROP TABLE IF EXISTS 지리_시도;

CREATE TABLE IF NOT EXISTS 지리_시도 (
    영문시도명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명)
);

CREATE TABLE IF NOT EXISTS 지리_시군구 (
    영문시도명 text,
    영문시군구명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명, 영문시군구명),
    FOREIGN KEY (영문시도명) REFERENCES 지리_시도 (영문시도명)
);

CREATE TABLE IF NOT EXISTS 지리_읍면동 (
    영문시도명 text,
    영문시군구명 text,
    영문읍면동명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명, 영문시군구명, 영문읍면동명),
    FOREIGN KEY (영문시도명, 영문시군구명) REFERENCES 지리_시군구 (영문시도명, 영문시군구명)
);

CREATE TABLE IF NOT EXISTS 지리_우편번호 (
    시도명 text,
    시군구명 text,
    기초구역번호 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (기초구역번호)
);
