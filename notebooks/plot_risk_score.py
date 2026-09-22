import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/fraud_signals.db")
query = """
SELECT risk_score,
       COUNT(*) AS txns,
       ROUND(100.0 * SUM("Is Fraudulent") / COUNT(*), 2) AS fraud_rate_pct
FROM transaction_risk_score
GROUP BY risk_score
ORDER BY risk_score;
"""
df = pd.read_sql(query, conn)
conn.close()

# Sequential blue ramp, light -> dark, matching increasing risk
colors = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(df["risk_score"].astype(str), df["fraud_rate_pct"], color=colors, width=0.6)

for bar, pct in zip(bars, df["fraud_rate_pct"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{pct}%", ha="center", va="bottom", fontsize=11, color="#0b0b0b")

ax.set_xlabel("Risk score")
ax.set_ylabel("Fraud rate (%)")
ax.set_title("Fraud rate climbs sharply with risk score", fontsize=13, pad=15)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#c3c2b7")
ax.spines["bottom"].set_color("#c3c2b7")
ax.tick_params(colors="#52514e")
ax.yaxis.grid(True, color="#e1e0d9", linewidth=0.8)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("screenshots/risk_score_chart.png", dpi=150)
print("Saved chart to screenshots/risk_score_chart.png")