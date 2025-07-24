import pandas as pd
import numpy as np

## Sales data
np.random.seed(42)

sales_people_ids = [
        1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009
        ]

def generate_sales_people(filename="../data/sales_team.csv"):
    sales_team_data = [
        {"id": 1001, "name": "Alice Johnson", "email": "alice@example.com", "phone": "555-123-1002"},
        {"id": 1002, "name": "Jared Smith", "email": "jared@example.com", "phone": "555-123-1003"},
        {"id": 1003, "name": "Heather Lee", "email": "heatherl@example.com", "phone": "555-123-1004"},
        {"id": 1004, "name": "Shaun Carter", "email": "shaun@example.com", "phone": "555-123-1005"},
        {"id": 1005, "name": "Marsha Brown", "email": "marsha@example.com", "phone": "555-123-1006"},
        {"id": 1006, "name": "Jared Miller", "email": "jaredm@example.com", "phone": "555-123-1007"},
        {"id": 1007, "name": "Heather Kim", "email": "heatherk@example.com", "phone": "555-123-1008"},
        {"id": 1008, "name": "Polly Adams", "email": "polly@example.com", "phone": "555-123-1009"},
        {"id": 1009, "name": "Dalisu Kim", "email": "dalisu@example.com", "phone": "555-123-1010"}
    ]
    df = pd.DataFrame(sales_team_data)
    df.to_csv(filename, index=False)
    print(f"{filename} generated")

## Sales data
def generate_sales_metrics(filename="../data/sales_data.csv"):
    sales_data = [{
        "mtd": 297000,
        "today": 9600,
        "yesterday": 20600,
        "nps": 61,
    }]
    df = pd.DataFrame(sales_data)
    df.to_csv(filename, index=False)
    print(f"{filename} generated")

## Feedback
def generate_feedback_data(filename="../data/feedback_data.csv"):
    feedback_data = [
        {"date": "2025-07-09", "sentiment": "neutral", "comment": "ok"},  # 14 days ago
        {"date": "2025-05-24", "sentiment": "positive", "comment": "Very helpful!!!"},  # 60 days ago  
        {"date": "2025-05-24", "sentiment": "positive", "comment": 'very good "thumbs up"'},  # Same timeframe
        # {"date": 14, "sentiment": "positive", "comment": "ok"}, 
        # {"date": 60, "sentiment": "positive", "comment": "Very helpful!!!"},
        # {"date": None, "sentiment": "positive", "comment": 'very good "thumbs up"'},       
        # {"date": 60, "sentiment": "positive", "comment": "Very helpful!!!"},
        # {"date": None, "sentiment": "positive", "comment": 'very good "thumbs up"'},
        # {"date": None, "sentiment": "negative", "comment": "Not satisfied with the service."},
        # {"date": None, "sentiment": "positive", "comment": "Quick response, thank you!"},
        # {"date": None, "sentiment": "negative", "comment": "Could be better."},
        # {"date": None, "sentiment": "positive", "comment": "Excellent support!"},
        # {"date": None, "sentiment": "positive", "comment": "Issue was resolved."},
        # {"date": None, "sentiment": "negative", "comment": "Still waiting for a reply."},
        # {"date": None, "sentiment": "positive", "comment": "Great experience!"},
        # {"date": None, "sentiment": "negative", "comment": "Not what I expected."},
        # {"date": None, "sentiment": "positive", "comment": "Will recommend to others."},
    ]
    df = pd.DataFrame(feedback_data)
    df.to_csv("../data/feedback_data.csv", index=False)
    print(f"{filename} generated")

## Social Media and engagement stats
    
## NPS
## Website stats"
def main():
    generate_sales_people()
    generate_sales_metrics()
    generate_feedback_data()


if __name__ == "__main__":
    main()
