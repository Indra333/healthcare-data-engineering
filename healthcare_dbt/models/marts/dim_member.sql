
{{ config(materialized='table') }}

WITH member_data AS (

    SELECT DISTINCT
        member_id,
        member_first_name,
        member_last_name,
        date_of_birth,
        gender
    FROM {{ ref('stg_enrollment') }}

),

unknown_member AS (

    SELECT
        'UNKNOWN' AS member_id,
        'Unknown' AS member_first_name,
        'Member' AS member_last_name,
        CAST(NULL AS DATE) AS date_of_birth,
        'Unknown' AS gender

)

SELECT * FROM member_data

UNION ALL

SELECT * FROM unknown_member
