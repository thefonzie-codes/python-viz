import numpy as np
import pandas as pd

def generate_metrics(filename="../data/metrics.csv"):
    metrics = [
        ("Monthly Recurring Revenue", 3.2, 4.0, "$", "M"),
        ("CAC Payback Period",       14.2, -0.9, "",  "mo"),
        ("Net Revenue Retention",    112, 4, "",  "%"),
        ("Monthly Churn Rate",       4.2, -0.6,"",  "%"),
        ("LTV:CAC Ratio",            4.8, 0.5, "",  "x"),
    ]
    df = pd.DataFrame(metrics, columns=["metric","value","delta","prefix","suffix"])
    df.to_csv(filename, index=False)

def generate_channel_acquisition(filename="../data/channel_acquisition.csv"):
    dates = pd.date_range("2022-03-01","2023-11-01", freq="MS")
    channels = [
        "Direct","Referrals","Email Marketing",
        "Content Marketing","Social Media",
        "Paid Search","Organic Search"
    ]
    np.random.seed(0)
    base = np.linspace(200, 800, len(dates))
    data = {"date": dates}
    for i, ch in enumerate(channels):
        noise = np.random.normal(scale=50, size=len(dates))
        trend = base * (1 + 0.1*np.sin(np.linspace(0,3*np.pi,len(dates)) + i))
        data[ch] = np.clip(trend + noise, 0, None).astype(int)
    pd.DataFrame(data).to_csv(filename, index=False)

def generate_arr_movement(filename="../data/arr_movement.csv"):
    np.random.seed(1)
    starting   = 28_000_000
    new_bus    = np.random.uniform(1_500_000,2_500_000)
    expansion  = np.random.uniform(800_000,1_500_000)
    contraction= -np.random.uniform(200_000,600_000)
    churn      = -np.random.uniform(100_000,500_000)
    ending     = starting + new_bus + expansion + contraction + churn
    rows = [
        ("Starting ARR", "absolute", starting),
        ("New Business", "relative", new_bus),
        ("Expansion",    "relative", expansion),
        ("Contraction",  "relative", contraction),
        ("Churn",        "relative", churn),
        ("Ending ARR",   "total",    ending),
    ]
    pd.DataFrame(rows, columns=["category","measure","value"]).to_csv(filename, index=False)

def generate_funnel_data(filename="../data/funnel_data.csv"):
    flows = [
        ("Organic Search","MQL",         5000),
        ("Paid Search",   "MQL",         4000),
        ("Content Marketing","MQL",      3000),
        ("Social Media",  "MQL",         3500),
        ("Direct",        "MQL",         4500),
        ("Email Marketing","MQL",        3200),
        ("Referrals",     "MQL",         2800),
        ("MQL",           "SQL",         6000),
        ("MQL",           "Unqualified", 2500),
        ("SQL",           "Opportunity", 1800),
        ("SQL",           "No Opportunity",2000),
        ("SQL",           "Lost",        1500),
        ("SQL",           "Won",          800),
    ]
    pd.DataFrame(flows, columns=["source","target","value"]).to_csv(filename, index=False)

def generate_cohort_data(filename="../data/cohort_data.csv", num_cohorts=8, months=12):
    np.random.seed(2)
    cohorts = [f"2022-{m:02d}" for m in range(4, 4+num_cohorts)]
    data = []
    for _ in cohorts:
        # Use smaller declines for first 8 months, larger for last 4 months
        declines = np.concatenate([
            np.random.uniform(3, 5, 8),
            np.random.uniform(5, 10, months - 8)
        ])
        retention = 100 - np.cumsum(declines)
        retention = np.clip(retention, 40, 100)
        data.append(retention)
    df = pd.DataFrame(data, columns=[f"M{i}" for i in range(months)])
    df.insert(0, "cohort", cohorts)
    df.to_csv(filename, index=False)

def main():
    generate_metrics()
    generate_channel_acquisition()
    generate_arr_movement()
    generate_funnel_data()
    generate_cohort_data()

if __name__ == "__main__":
    main()