-- Combine validated risk signals (account age, overnight hours) into a single score
CREATE VIEW transaction_risk_score AS
SELECT "Transaction ID", "Customer ID", "Transaction Amount", "Is Fraudulent",
  (CASE WHEN "Account Age Days" < 30 THEN 2 ELSE 0 END) +
  (CASE WHEN "Transaction Hour" BETWEEN 0 AND 5 THEN 1 ELSE 0 END) AS risk_score
FROM transactions;

-- Does the combined score separate fraud from legitimate transactions?
SELECT risk_score,
       COUNT(*) AS txns,
       ROUND(100.0 * SUM("Is Fraudulent") / COUNT(*), 2) AS fraud_rate_pct
FROM transaction_risk_score
GROUP BY risk_score
ORDER BY risk_score DESC;