
SELECT
    claim_id,
    line_number,
    date_of_first_service,
    date_of_last_service
FROM {{ ref('stg_medical_claims') }}
WHERE date_of_last_service < date_of_first_service
