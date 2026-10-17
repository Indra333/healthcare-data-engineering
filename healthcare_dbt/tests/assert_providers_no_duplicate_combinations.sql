
SELECT
    provider_id,
    provider_name,
    provider_npi_number,
    supplier_name,
    COUNT(*) AS duplicate_count
FROM {{ ref('stg_providers') }}
GROUP BY
    provider_id,
    provider_name,
    provider_npi_number,
    supplier_name
HAVING COUNT(*) > 1
