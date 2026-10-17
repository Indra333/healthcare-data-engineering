
WITH source_data AS (

    SELECT *
    FROM {{ source('healthcare_raw', 'MEDICAL_CLAIMS') }}

),

cleaned AS (

    SELECT
        NULLIF(TRIM(CLAIM_ID), 'NULL') AS claim_id,

        COALESCE(
    		NULLIF(TRIM(LINE_NUMBER:"string"::VARCHAR), ''),
    		NULLIF(TRIM(LINE_NUMBER:"double"::VARCHAR), '')
	) AS line_number,

        NULLIF(TRIM(MEMBER_ID), 'NULL') AS member_id,

        NULLIF(TRIM(PROVIDER_ID), 'NULL') AS provider_id,

        NULLIF(TRIM(CLAIM_TYPE_CODE), 'NULL') AS claim_type_code,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_OF_FIRST_SERVICE), 'NULL'),
            'YYYY/MM/DD'
        ) AS date_of_first_service,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_OF_LAST_SERVICE), 'NULL'),
            'YYYY/MM/DD'
        ) AS date_of_last_service,

        NULLIF(TRIM(PROCEDURE_CODE), 'NULL') AS procedure_code,

        NULLIF(TRIM(PROCEDURE_MODIFIER_CODE_1), 'NULL')
            AS procedure_modifier_code_1,

        NULLIF(TRIM(PLACE_OF_SERVICE_CODE), 'NULL')
            AS place_of_service_code,

        CHARGE_SUBMITTED AS charge_submitted,
        ALLOWED_AMOUNT AS allowed_amount,
        COPAYMENT AS copayment,
        CO_INSURANCE AS co_insurance,
        DEDUCTIBLE AS deductible

    FROM source_data

)

SELECT *
FROM cleaned
