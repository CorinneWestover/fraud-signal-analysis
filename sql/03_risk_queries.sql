-- Are transactions sharing an IP address with another transaction more likely to be fraudulent?
WITH ip_activity AS (
  SELECT *,
         COUNT(*) OVER (PARTITION BY "IP Address") AS ip_txn_count
  FROM transactions
)
SELECT
  CASE WHEN ip_txn_count > 1 THEN 'Shared IP (2 txns)' ELSE 'Unique IP (1 txn)' END AS ip_group,
  COUNT(*) AS txns,
  ROUND(100.0 * SUM("Is Fraudulent") / COUNT(*), 2) AS fraud_rate_pct
FROM ip_activity
GROUP BY ip_group
ORDER BY fraud_rate_pct DESC;