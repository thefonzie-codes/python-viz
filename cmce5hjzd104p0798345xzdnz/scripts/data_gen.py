import pandas as pd
import numpy as np

def generate_regions(filename="../data/regions.csv"):
    regions = [
        ("North America", "USA", "NA"),
        ("Europe", "UK", "EU"),
        ("Europe", "Germany", "EU"),
        ("Asia", "India", "APAC"),
    ]
    df = pd.DataFrame(regions, columns = ["region", "country", "region_code"])
    df.to_csv(filename, index=False)
    print("regions.csv successfuly generated")

def generate_employees(region, filename="../data/employees.csv"):
    first_names = ['John', 'Jane', 'Alex', 'Sarah', 'Mike', 'Emma', 'David', 'Lisa', 'Chris', 'Anna', 'Mark', 'Sofia', 'Ryan', 'Maya', 'Tom', 'Zoe', 'Ben', 'Aria', 'Sam', 'Nora']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Garcia']
    countries = ["USA", "UK", "Germany", "India"]

    employees = []
    for employee in employees:
       pass 

def main():
    generate_regions()

if __name__ == "__main__":
    main()
