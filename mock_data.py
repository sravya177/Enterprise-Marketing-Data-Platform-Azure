import pandas as pd
import json
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize the Faker toolbox to generate realistic mock text
fake = Faker()
Faker.seed(42) # This ensures the fake data generated is consistent every time we run it

NUM_CUSTOMERS = 500
NUM_WEB_EVENTS = 5000

OUTPUT_CRM = "crm_customer_profiles.csv"
OUTPUT_WEB = "web_clickstream_events.json"

print("Starting mock data synthesis...")

# --- 1. GENERATE CRM BASE DATA ---
customers = []
for _ in range(NUM_CUSTOMERS):
    customers.append({
        "customer_id": f"CUST-{fake.unique.random_int(min=10000, max=99999)}",
        "signup_date": fake.date_between(start_date='-3y', end_date='today'),
        "state": fake.state_abbr(),
        "postal_code": fake.zipcode(),
        "total_lifetime_orders": random.randint(1, 50),
        "total_historical_spend": round(random.uniform(20.0, 5000.0), 2)
    })

# Convert the list of customers into a clean rows-and-columns format (DataFrame)
crm_df = pd.DataFrame(customers)
# Save it as an Excel-readable CSV file
crm_df.to_csv(OUTPUT_CRM, index=False)

# --- 2. GENERATE DEPENDENT WEB EVENT LOGS ---
events = []
pages = ["Home", "Product_View", "Cart_Add", "Checkout"]
# These weights make sure that 40% of clicks hit Home, 40% hit View, 15% Add to Cart, and only 5% Checkout
weights = [0.4, 0.4, 0.15, 0.05]
customer_ids = crm_df["customer_id"].tolist()

for _ in range(NUM_WEB_EVENTS):
    events.append({
        "session_id": fake.uuid4(),
        "customer_id": random.choice(customer_ids), # Matches a random customer from the list above
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat(),
        "page_visited": random.choices(pages, weights=weights)[0],
        "device_type": random.choice(["Mobile", "Desktop", "Tablet"])
    })

# Save the web data as a newline-delimited JSON log file
with open(OUTPUT_WEB, "w") as f:
    for entry in events:
        f.write(json.dumps(entry) + "\n")

print("Mock data synthesis complete. Clean relational profiles created successfully!")