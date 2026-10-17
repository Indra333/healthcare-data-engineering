
WITH source_data AS (

    SELECT *
    FROM {{ source('healthcare_raw', 'PROVIDERS') }}

),

cleaned AS (

    SELECT
        NULLIF(TRIM(PROVIDER_ID), 'NULL') AS provider_id,

        NULLIF(TRIM(PROVIDER_NAME), 'NULL') AS provider_name,

        NULLIF(TRIM(PROVIDER_NPI_NUMBER), 'NULL')
            AS provider_npi_number,

        NULLIF(TRIM(SUPPLIER_NAME), 'NULL') AS supplier_name

    FROM source_data

)

SELECT DISTINCT
    provider_id,
    provider_name,
    provider_npi_number,
    supplier_name
FROM cleaned
