
WITH source_data AS (

    SELECT *
    FROM {{ source('healthcare_raw', 'ENROLLMENT') }}

),

cleaned AS (

    SELECT
        NULLIF(TRIM(MEMBER_ID), 'NULL') AS member_id,

        NULLIF(TRIM(MEMBER_FIRST_NAME), 'NULL')
            AS member_first_name,

        NULLIF(TRIM(MEMBER_LAST_NAME), 'NULL')
            AS member_last_name,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_OF_BIRTH), 'NULL'),
            'YYYY-MM-DD'
        ) AS date_of_birth,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_OF_DEATH), 'NULL'),
            'YYYY/MM/DD'
        ) AS date_of_death,

        NULLIF(TRIM(GENDER), 'NULL') AS gender,

        TRY_TO_DATE(
            NULLIF(TRIM(EFFDATE), 'NULL'),
            'YYYY/MM/DD'
        ) AS effective_date,

        TRY_TO_DATE(
            NULLIF(TRIM(ENDDATE), 'NULL'),
            'YYYY/MM/DD'
        ) AS end_date,

        NULLIF(TRIM(ELIGIBILITY_SNAPSHOT_MONTH), 'NULL')
            AS eligibility_snapshot_month,

        NULLIF(TRIM(PCP_ID), 'NULL') AS pcp_id,

        NULLIF(TRIM(PLAN_CODE), 'NULL') AS plan_code

    FROM source_data

)

SELECT *
FROM cleaned
