INSERT INTO 행정구역_시도
SELECT 시도명, A.영문시도명, GEOMETRY, CENTER_COORDINATES
FROM (
    SELECT DISTINCT 시도명, 영문시도명
    FROM 도로명코드
) as A, 지리_시도 as B
WHERE A.영문시도명 = B.영문시도명
;

INSERT INTO 행정구역_시군구
SELECT 시도명, A.영문시도명, 시군구명, A.영문시군구명, GEOMETRY, CENTER_COORDINATES
FROM (
    SELECT DISTINCT 시도명, 영문시도명, 시군구명, 영문시군구명
    FROM 도로명코드
    WHERE 시군구명 IS NOT NULL
) as A, 지리_시군구 as B
WHERE A.영문시도명 = B.영문시도명
    and A.영문시군구명 = B.영문시군구명
;

INSERT INTO 행정구역_읍면동
SELECT 시도명, A.영문시도명, 시군구명, A.영문시군구명, 읍면동명, A.영문읍면동명, GEOMETRY, CENTER_COORDINATES
FROM (
    SELECT DISTINCT 시도명, 영문시도명, 시군구명, 영문시군구명, 읍면동명, 영문읍면동명
    FROM 도로명코드
    WHERE 시군구명 IS NOT NULL
) as A, 지리_읍면동 as B
WHERE A.영문시도명 = B.영문시도명
    and A.영문시군구명 = B.영문시군구명
    and A.영문읍면동명 = B.영문읍면동명
;

INSERT INTO 행정구역_우편번호
SELECT A.시도명, A.시군구명, A.행정동명, A.우편번호, A.건축물대장_건물명, A.상세건물명, A.시군구용_건물명, GEOMETRY, CENTER_COORDINATES
FROM (
    SELECT DISTINCT 시도명, 시군구명, 행정동명, 우편번호, 건축물대장_건물명, 상세건물명, 시군구용_건물명
    FROM 건물정보
    WHERE 건축물대장_건물명 is not null
) as A, 지리_우편번호 as B
WHERE A.우편번호 = B.기초구역번호
;
