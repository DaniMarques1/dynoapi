import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
BEARER = os.getenv("BEARER")

# Ensure token is present
if not BEARER:
    raise ValueError("BEARER token not found in .env file")

# Endpoint and query
endpoint = "https://preview.craft-world.gg/graphql"
query = (
    "query { account { tradeExecutions { id errorReason quote { type input { symbol amount } "
    "output { symbol amount } details { priceImpactPercentage } } trade { transaction { hash } "
    "input { symbol amount } output { symbol amount } } } } }"
)

# URL-encode the query for GET request
params = {"query": query}

# Headers with Authorization
headers = {
    "Authorization": f"Bearer {BEARER}",
    "Content-Type": "application/json"
}

# Send GET request
response = requests.get(endpoint, headers=headers, params=params)

# Handle response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
