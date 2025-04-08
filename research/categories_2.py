from dotenv import load_dotenv
import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% Loading dotenv and API key
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")

# %% Fetch Categories from iFixit API
url = "https://www.ifixit.com/api/2.0/categories"
headers = {"User-Agent": USER_AGENT}

# Send the API request
response = requests.get(url, headers=headers)

# Check API response
if response.status_code == 200:
    categories_json = response.json()
    # Uncomment for debugging to see the structure of categories_json
    # print(json.dumps(categories_json, indent=2))  
else:
    print("Loading categories failed:", response.status_code)
    exit()

# %% Parse Categories and Models (Capture all levels)
categories_list = []

# Function to recursively extract categories, subcategories, intermediate levels, and models
def extract_all_levels(categories, hierarchy_levels):
    if isinstance(categories, dict):
        for key, value in categories.items():
            # Add the current key (category, subcategory, intermediate level) to the hierarchy
            new_hierarchy = hierarchy_levels + [key]
            if isinstance(value, dict):
                # If it's a subcategory or intermediate level, continue recursion
                extract_all_levels(value, new_hierarchy)
            elif value is None:
                # If value is None, this is the last level (model names)
                categories_list.append(tuple(new_hierarchy))

# Iterate through the top-level categories and start extracting all levels
for category_name, subcategories in categories_json.items():
    if isinstance(subcategories, dict):
        # For each category, iterate through the subcategories or intermediate levels
        extract_all_levels(subcategories, [category_name])

# %% 
# Create DataFrame from the extracted data (with all levels)
# Dynamically assign column names like level1, level2, etc.
num_levels = max(len(item) for item in categories_list)
columns = [f"level{i+1}" for i in range(num_levels)]

# Create the DataFrame with dynamic columns
df_all_levels = pd.DataFrame(categories_list, columns=columns)

# Drop columns where all values are NaN (missing)
df_all_levels_clean = df_all_levels.dropna(axis=1, how='all')

# total number of device models
print("Total device models:", len(df_all_levels_clean))


#%%
# plot level one barplot

# Set font size for all plot elements
font_size = 20
plt.rcParams.update({'font.size': font_size})

# Create a bar plot for level 1
plt.figure(figsize=(10, 6))

# Directly apply 'viridis' palette to the countplot
sns.countplot(x='level1', data=df_all_levels_clean, order=df_all_levels_clean['level1'].value_counts().index, palette='viridis')

# Remove the black box (axes spines) around the plot
sns.despine()

# Set plot titles and labels
plt.title('# Device categories on ifixit.com')
plt.xticks(rotation=90)
plt.xlabel('')
plt.ylabel('')

#%%
# Filter the DataFrame to include only rows where 'level1' is 'Phone'
df_phone = df_all_levels_clean[df_all_levels_clean['level1'] == 'Phone']

# total phones
print("Total phone models:", len(df_phone))

#%%
# create bar plot for level2 of level1=phone

# Set font size for all plot elements
font_size = 20
plt.rcParams.update({'font.size': font_size})

# Create the figure and axes
plt.figure(figsize=(6, 5))

# Directly apply 'viridis' palette to the countplot
sns.countplot(x='level2', data=df_phone, order=df_phone['level2'].value_counts().index, palette='viridis')

# Remove the black box (axes spines) around the plot
sns.despine()

# Set plot titles and labels
plt.title('# Phones on ifixit.com')
plt.xticks(rotation=90)
plt.xlabel('')
plt.ylabel('')

# %%
# Create a figure with two subplots: one for level 1 and one for level 2
# Set font size for all plot elements
font_size = 20
plt.rcParams.update({'font.size': font_size})

# Create the figure with specified layout
fig = plt.figure(figsize=(12, 6))

# Define the grid specifications: set relative the widths of plots
gridspec = fig.add_gridspec(1, 2, width_ratios=[0.7, 0.3])

# Create the first subplot (left one, 60% width)
ax1 = fig.add_subplot(gridspec[0])
sns.countplot(x='level1', data=df_all_levels_clean, order=df_all_levels_clean['level1'].value_counts().index, palette='viridis', ax=ax1)
sns.despine(ax=ax1)

# Set titles and labels for the first plot
ax1.set_title('# Device categories')
ax1.set_xlabel('')
ax1.set_ylabel('')
ax1.tick_params(axis='x', rotation=90)

# Create the second subplot (right one, 40% width)
ax2 = fig.add_subplot(gridspec[1])
df_phone = df_all_levels_clean[df_all_levels_clean['level1'] == 'Phone']
sns.countplot(x='level2', data=df_phone, order=df_phone['level2'].value_counts().index, palette='viridis', ax=ax2)
sns.despine(ax=ax2)

# Set titles and labels for the second plot
ax2.set_title('# Phones')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.tick_params(axis='x', rotation=90)

# Adjust layout to avoid overlap
plt.tight_layout()

