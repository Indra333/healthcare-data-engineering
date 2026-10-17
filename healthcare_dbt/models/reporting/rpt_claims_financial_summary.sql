
{{ config(materialized='table') }}

WITH medical_summary AS (

    SELECT
        'MEDICAL' AS claim_category,
        COUNT(*) AS total_records,
        SUM(allowed_amount) AS total_allowed_amount,
        SUM(copayment) AS total_copayment,
        SUM(co_insurance) AS total_coinsurance,
        SUM(deductible) AS total_deductible
    FROM {{ ref('fct_medical_claims') }}

),

pharmacy_summary AS (

    SELECT
        'PHARMACY' AS claim_category,
        COUNT(*) AS total_records,
        SUM(allowed_amount) AS total_allowed_amount,
        SUM(copayment) AS total_copayment,
        SUM(co_insurance) AS total_coinsurance,
        SUM(deductible) AS total_deductible
    FROM {{ ref('fct_pharmacy_claims') }}

)

SELECT * FROM medical_summary

UNION ALL

SELECT * FROM pharmacy_summary
