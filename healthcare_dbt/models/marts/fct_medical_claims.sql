
{{ config(materialized='table') }}

WITH medical_claims AS (

    SELECT *
    FROM {{ ref('stg_medical_claims') }}

),

member_dimension AS (

    SELECT member_id
    FROM {{ ref('dim_member') }}
    WHERE member_id <> 'UNKNOWN'

),

provider_dimension AS (

    SELECT provider_id
    FROM {{ ref('dim_provider') }}
    WHERE provider_id <> 'UNKNOWN'

)

SELECT
    c.claim_id,
    c.line_number,

    c.member_id AS source_member_id,
    COALESCE(m.member_id, 'UNKNOWN') AS member_key,

    c.provider_id AS source_provider_id,
    COALESCE(p.provider_id, 'UNKNOWN') AS provider_key,

    c.claim_type_code,
    c.date_of_first_service,
    c.date_of_last_service,
    c.procedure_code,
    c.procedure_modifier_code_1,
    c.place_of_service_code,

    c.charge_submitted,
    c.allowed_amount,
    c.copayment,
    c.co_insurance,
    c.deductible

FROM medical_claims c

LEFT JOIN member_dimension m
    ON c.member_id = m.member_id

LEFT JOIN provider_dimension p
    ON c.provider_id = p.provider_id
