
WITH source_data AS (

    SELECT *
    FROM {{ source('healthcare_raw', 'PHARMACY_CLAIMS') }}

),

cleaned AS (

    SELECT
        NULLIF(TRIM(CLAIM_ID), 'NULL') AS claim_id,

        NULLIF(TRIM(MEMBER_ID), 'NULL') AS member_id,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_OF_SERVICE), 'NULL'),
            'YYYY/MM/DD'
        ) AS date_of_service,

        TRY_TO_DATE(
            NULLIF(TRIM(DATE_PAID), 'NULL'),
            'YYYY/MM/DD'
        ) AS date_paid,

        NULLIF(TRIM(DISPENSING_PROVIDER_ID), 'NULL')
            AS dispensing_provider_id,

        RX_REFILL_NUMBER AS rx_refill_number,

        ALLOWED_AMOUNT AS allowed_amount,

        COPAYMENT AS copayment,

        CO_INSURANCE AS co_insurance,

        DEDUCTIBLE AS deductible,
	
	CASE
            WHEN TRY_TO_DATE(DATE_PAID, 'YYYY/MM/DD')
               < TRY_TO_DATE(DATE_OF_SERVICE, 'YYYY/MM/DD')
            THEN TRUE
            ELSE FALSE
        END AS payment_before_service_flag

    FROM source_data

)

SELECT *
FROM cleaned
