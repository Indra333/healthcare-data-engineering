
{{ config(materialized='table') }}

WITH provider_data AS (

    SELECT DISTINCT
        provider_id,
        provider_name,
        provider_npi_number
    FROM {{ ref('stg_providers') }}

),

unknown_provider AS (

    SELECT
        'UNKNOWN' AS provider_id,
        'Unknown Provider' AS provider_name,
        'UNKNOWN' AS provider_npi_number

)

SELECT * FROM provider_data

UNION ALL

SELECT * FROM unknown_provider
