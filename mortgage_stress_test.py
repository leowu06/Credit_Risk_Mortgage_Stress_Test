import pandas as pd
import numpy as np

n = 10000
np.random.seed(42)

df = pd.DataFrame({
    "loan_id": np.arange(n),
    "current_balance": np.random.uniform(50000,500000, n),
    "original_property_value": np.random.uniform(100000, 700000, n),
    "days_past_due": np.random.choice([0,10,20,40,70,120], n,p=[0.75,0.1,0.05,0.05,0.03,0.02]),
    "baseline_pd_12m": np.random.uniform(0.0001, 0.05, n),
    "baseline_LGD": np.random.uniform(0.05,0.4,n)
})

df["current_property_value"] = df["original_property_value"] * np.random.uniform(0.95, 1.30, n)
df["baseline_LTV"] = df["current_balance"] / df["current_property_value"]

def determine_stage(row):
    dpd = row["days_past_due"]
    
    if dpd >= 90:
        return 3
    if dpd >= 30:
        return 2
    else:
        return 1

df["baseline_stage"] = df.apply(determine_stage, axis = 1)

stress_factor = 0.85
df["stress_property"] = df["current_property_value"]*stress_factor
df["stress_LTV"] = df["current_balance"]/df["stress_property"]

def LGD_from_LTV(row):
    ltv = row["stress_LTV"]

    conditions = [
        ltv < 0.6,
        (ltv >= 0.6) & (ltv < 0.8),
        (ltv >= 0.8) & (ltv < 1.0)
    ]

    choices = [0.05, 0.15, 0.30]

    return np.select(conditions, choices, default=0.50)

df["stress_LGD"] = df.apply(LGD_from_LTV, axis=1)

def stress_pd(row):
    pd = row["baseline_pd_12m"]
    ltv = row["stress_LTV"]
    if ltv > 1:
        return min(pd*3,1)
    if ltv > 0.9:
        return min(pd*2, 1)
    else:
        return pd
    
df["stress_pd"] = df.apply(stress_pd, axis = 1)

df["baseline_EL"] = df["baseline_pd_12m"] * df["baseline_LGD"] * df["current_balance"]
df["stress_EL"] = df["stress_pd"] * df["stress_LGD"] * df["current_balance"]

def migrate_stages(row):
    dpd = row["days_past_due"]
    pd = row["stress_pd"]
    if dpd>= 90:
        return 3
    if dpd >= 30 or pd > 2*row["baseline_pd_12m"]:
        return 2
    else:
        return 1
    
df["stress_stage"] = df.apply(migrate_stages, axis = 1)
df.to_csv("/Users/leowuqiu/Desktop/Python Course/mortgage_stress_output.csv", index=False)
