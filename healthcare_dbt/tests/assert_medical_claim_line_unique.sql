
-- Every claim_id + line_number combination
-- must appear exactly once in the fact table.

SELECT
    claim_id,
    line_number,
    COUNT(*) AS duplicate_count

FROM {{ ref('fct_medical_claims') }}

GROUP BY
    claim_id,
    line_number

HAVING COUNT(*) > 1
