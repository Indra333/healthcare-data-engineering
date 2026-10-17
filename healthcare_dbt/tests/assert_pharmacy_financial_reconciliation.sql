
WITH ranked_source AS (

    SELECT
        claim_id,
        allowed_amount,

        ROW_NUMBER() OVER (
            PARTITION BY claim_id
            ORDER BY date_paid DESC NULLS LAST
        ) AS claim_version_rank

    FROM {{ ref('stg_pharmacy_claims') }}

),

expected AS (

    SELECT
        COUNT(*) AS expected_claims,
        SUM(allowed_amount) AS expected_allowed_amount

    FROM ranked_source
    WHERE claim_version_rank = 1

),

actual AS (

    SELECT
        COUNT(*) AS actual_claims,
        SUM(allowed_amount) AS actual_allowed_amount

    FROM {{ ref('fct_pharmacy_claims') }}

)

SELECT
    expected_claims,
    actual_claims,
    expected_allowed_amount,
    actual_allowed_amount

FROM expected
CROSS JOIN actual

WHERE
    expected_claims <> actual_claims
    OR expected_allowed_amount
        IS DISTINCT FROM actual_allowed_amount
