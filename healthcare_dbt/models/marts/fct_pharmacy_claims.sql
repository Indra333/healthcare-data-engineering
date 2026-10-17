
{{ config(materialized='table') }}

WITH pharmacy_claims AS (

    SELECT *
    FROM {{ ref('stg_pharmacy_claims') }}

),

ranked_claims AS (

    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY claim_id
            ORDER BY date_paid DESC NULLS LAST
        ) AS claim_version_rank
    FROM pharmacy_claims

),

latest_claims AS (

    SELECT *
    FROM ranked_claims
    WHERE claim_version_rank = 1

),

member_dimension AS (

    SELECT member_id
    FROM {{ ref('dim_member') }}
    WHERE member_id <> 'UNKNOWN'

)

SELECT
    c.claim_id,

    c.member_id AS source_member_id,
    COALESCE(m.member_id, 'UNKNOWN') AS member_key,

    c.date_of_service,
    c.date_paid,
    c.dispensing_provider_id,
    c.rx_refill_number,

    c.allowed_amount,
    c.copayment,
    c.co_insurance,
    c.deductible,

    c.payment_before_service_flag

FROM latest_claims c

LEFT JOIN member_dimension m
    ON c.member_id = m.member_id
