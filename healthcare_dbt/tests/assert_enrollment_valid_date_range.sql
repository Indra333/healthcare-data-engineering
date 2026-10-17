
SELECT
    member_id,
    effective_date,
    end_date
FROM {{ ref('stg_enrollment') }}
WHERE end_date < effective_date
