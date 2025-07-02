import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from pymongo import MongoClient
from tabulate import tabulate

# Load .env variables
load_dotenv()
BEARER = os.getenv("BEARER")
MONGO_URI = os.getenv("MONGO_URI")

# Check required variables
if not BEARER:
    raise ValueError("BEARER token not found in .env file")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["dyno"]
collection = db["prices"]

# GraphQL endpoint and query
endpoint = "https://preview.craft-world.gg/graphql"
query = """
query {
  exchangePriceList {
    baseSymbol
    prices {
      referenceSymbol
      amount
      recommendation
    }
  }
}
"""

params = {"query": query}
headers = {
    "Authorization": f"Bearer {BEARER}",
    "Content-Type": "application/json"
}

# Send request
response = requests.get(endpoint, headers=headers, params=params)

if response.status_code == 200:
    raw_data = response.json()
    exchange = raw_data.get("data", {}).get("exchangePriceList", {})

    transformed_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": {}
    }

    base = exchange.get("baseSymbol")
    prices = exchange.get("prices", [])

    table_rows = []

    for price in prices:
        asset = price.get("referenceSymbol")
        value = price.get("amount")
        recommendation = price.get("recommendation")

        # Transform structure
        transformed_data["data"][asset] = {
            "base": base,
            "value": value,
            "recommendation": recommendation
        }

        # Prepare for table
        table_rows.append([asset, base, round(value, 5), recommendation])

    # Print fancy table
    print("\n📊 Tabela Formatada:\n")
    print(tabulate(table_rows, headers=["Asset", "Base", "Value", "Recommendation"], tablefmt="grid"))

    # Print raw table
    print("\n📋 Tabela RAW:\n")
    print("ASSET       PRICE       STATUS")
    for row in table_rows:
        asset = row[0].ljust(15)
        # Format number with comma as decimal separator
        price = f"{row[2]:,.5f}".replace(",", "X").replace(".", ",").replace("X", ".").ljust(15)
        status = row[3]
        print(f"{asset}{price}{status}")

else:
    print(f"❌ Request failed with status code {response.status_code}")
    print(response.text)
