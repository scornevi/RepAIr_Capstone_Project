# %%
# Libraries
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import IFixitLoader
import requests
import pandas as pd
import json

# %%
# Loading dotenv and api key
load_dotenv()
groq_key = os.getenv('GROQ_KEY')
USER_AGENT = os.getenv("USER_AGENT")

# %%
url = "https://www.ifixit.com/api/2.0/categories"

headers = {"User-Agent": USER_AGENT}

# Sending API request
response = requests.get(url, headers=headers)

# Checking API response
if response.status_code == 200:
    categories_json = response.json()
    print(json.dumps(categories_json, indent=2))
else:
    print("Loading of categories failed:", response.status_code)
    exit()

# %%

categories_list = []
for category, subcategories in categories_json.items():
    for subcategory, devices in subcategories.items():
        if isinstance(devices, dict):
            for device in devices.keys():
                categories_list.append((category, subcategory, device))
        else: categories_list.append((category, subcategory, None))
    else:
        categories_list.append((category, None, None))  # Falls keine Subkategorien existieren

df = pd.DataFrame(categories_list, columns=["Category", "Subcategory", "Device"])

print(df.head()) 

# %%
phones_df = df[df["Category"] == "Phone"]
print(phones_df.head(50))
# %%
# Fetch all guides
response = requests.get("https://www.ifixit.com/api/2.0/guides")
data = response.json()
# Print the structure of the response to understand it
print(type(data))  # Check if it's a list or dictionary
print(data[:2])  # Print the first two elements to inspect the format
# Extract titles if it's a list
if isinstance(data, list):
    for guide in data[:200]:  # Get the first 10 guides
        print(guide.get("title", "No title found"))
else:
    print("Unexpected API response format.")