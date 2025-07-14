import pandas as pd
import json
import os

# --- Create Directory for Data ---
if not os.path.exists('data'):
    os.makedirs('data')

# --- Data for Plot 1: Student Retention KPI & Composition ---

# 1a. Main KPI
retention_kpi = {"retention_rate": 91}
with open('data/retention_kpi.json', 'w') as f:
    json.dump(retention_kpi, f)

# 1b. Student Composition Bar Chart
student_composition_data = {
    'Category': ['Returning', 'New'],
    'Count': [3600, 1600]
}
student_composition_df = pd.DataFrame(student_composition_data)
student_composition_df.to_csv('data/student_composition.csv', index=False)

# --- Data for Plot 2: Retention by School ---
retention_by_school_data = {
    'Campus': ['Campus 2', 'Campus 1', 'Campus 3', 'Campus 4', 'Campus 8', 'Campus 6', 'Campus 5', 'Campus 7'],
    'RetentionRate': [92, 91, 94, 84, 92, 92, 92, 85]
}
retention_by_school_df = pd.DataFrame(retention_by_school_data)
retention_by_school_df.to_csv('data/retention_by_school.csv', index=False)

# --- Data for Plot 4: District Withdrawals (and used for Plot 3) ---
# This detailed monthly data will be aggregated for the pie chart to ensure consistency.
district_withdrawals_data = [
    {'Month': 'August', 'Year': 2022, 'Reason': 'Elementary With', 'Count': 45},
    {'Month': 'August', 'Year': 2022, 'Reason': 'EXP CAN\'T RET', 'Count': 5},
    {'Month': 'August', 'Year': 2022, 'Reason': 'Transferred to', 'Count': 2},
    {'Month': 'August', 'Year': 2022, 'Reason': 'OTHER (UNKNOWN)', 'Count': 10},

    {'Month': 'September', 'Year': 2022, 'Reason': 'Elementary With', 'Count': 52},
    {'Month': 'September', 'Year': 2022, 'Reason': 'EXP CAN\'T RET', 'Count': 10},
    {'Month': 'September', 'Year': 2022, 'Reason': 'OTHER (UNKNOWN)', 'Count': 10},

    {'Month': 'October', 'Year': 2022, 'Reason': 'Elementary With', 'Count': 50},
    {'Month': 'October', 'Year': 2022, 'Reason': 'EXP CAN\'T RET', 'Count': 15},
    {'Month': 'October', 'Year': 2022, 'Reason': 'OTHER (UNKNOWN)', 'Count': 12},

    {'Month': 'November', 'Year': 2022, 'Reason': 'Elementary With', 'Count': 42},
    {'Month': 'November', 'Year': 2022, 'Reason': 'EXP CAN\'T RET', 'Count': 3},
    {'Month': 'November', 'Year': 2022, 'Reason': 'OTHER (UNKNOWN)', 'Count': 13},

    {'Month': 'December', 'Year': 2022, 'Reason': 'Elementary With', 'Count': 15},
    {'Month': 'December', 'Year': 2022, 'Reason': 'EXP CAN\'T RET', 'Count': 2},
    {'Month': 'December', 'Year': 2022, 'Reason': 'OTHER (UNKNOWN)', 'Count': 4},

    {'Month': 'January', 'Year': 2023, 'Reason': 'Elementary With', 'Count': 60},
    {'Month': 'January', 'Year': 2023, 'Reason': 'Enroll In Other', 'Count': 2},
    {'Month': 'January', 'Year': 2023, 'Reason': 'EXP CAN\'T RET', 'Count': 15},
    {'Month': 'January', 'Year': 2023, 'Reason': 'OTHER (UNKNOWN)', 'Count': 21},

    {'Month': 'February', 'Year': 2023, 'Reason': 'Elementary With', 'Count': 30},
    {'Month': 'February', 'Year': 2023, 'Reason': 'EXP CAN\'T RET', 'Count': 5},
    {'Month': 'February', 'Year': 2023, 'Reason': 'OTHER (UNKNOWN)', 'Count': 14},

    {'Month': 'March', 'Year': 2023, 'Reason': 'Elementary With', 'Count': 25},
    {'Month': 'March', 'Year': 2023, 'Reason': 'Enroll In Other', 'Count': 1},
    {'Month': 'March', 'Year': 2023, 'Reason': 'EXP CAN\'T RET', 'Count': 5},
    {'Month': 'March', 'Year': 2023, 'Reason': 'OTHER (UNKNOWN)', 'Count': 9},

    {'Month': 'April', 'Year': 2023, 'Reason': 'Elementary With', 'Count': 2},
    {'Month': 'April', 'Year': 2023, 'Reason': 'OTHER (UNKNOWN)', 'Count': 3},
]
district_withdrawals_df = pd.DataFrame(district_withdrawals_data)
district_withdrawals_df.to_csv('data/district_withdrawals.csv', index=False)


# --- Data for Plot 3: Top Withdrawal Reasons ---
# This data is derived from the monthly withdrawals to ensure consistency.
withdrawal_summary = district_withdrawals_df.groupby('Reason')['Count'].sum().reset_index()
total_withdrawals = withdrawal_summary['Count'].sum()
withdrawal_summary['Percentage'] = round((withdrawal_summary['Count'] / total_withdrawals) * 100, 1)

# The pie chart only shows reasons with non-negligible percentages.
# We will save the full summary, and the plotting script will handle filtering.
withdrawal_summary.to_csv('data/withdrawal_reasons.csv', index=False)


print("Data generation complete. Files saved in 'data/' directory:")
print("- retention_kpi.json")
print("- student_composition.csv")
print("- retention_by_school.csv")
print("- district_withdrawals.csv")
print("- withdrawal_reasons.csv")
