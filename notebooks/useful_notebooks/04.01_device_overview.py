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


df[df["Subcategory"=="Phone"]]

#%%
import subprocess

# Get the root directory of the git repository
root_dir = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).strip().decode("utf-8")
save_to = root_dir +"/data/ifixit_device_categories/devices.csv"
# save data frame df as.csv
df.to_csv(save_to, index=False)

# save also json categories_json
with open(root_dir + "/data/ifixit_device_categories/devices.json", "w") as f:
    json.dump(categories_json, f)

# %%
phones_df = df[df["Category"] == "Phone"]
print(phones_df.head(50))


# list all categories
print(df.Category.unique())
# list all subcategories

# make a function that gives all unique devices for category and subcategory each device on new line


def get_devices(category, subcategory):
    filtered_df = df[(df["Category"] == category) & (df["Subcategory"] == subcategory)]
    
    # Extract the values from the 'Device' column
    device_names = filtered_df['Device'].tolist()
    
    # Return devices with each on a new line
    return "\n".join(device_names)

df.Subcategory.unique()
# deploy function in example
print(get_devices("Phone", "Android Phone"))

# %%
# plot devices per subcategory phone
import matplotlib.pyplot as plt
import seaborn as sns

# set parameter for fontzise
size=18

# Set the figure size
plt.figure(figsize=(8, 5))

# Create a countplot
sns.countplot(data=phones_df, x='Subcategory', palette='viridis')
# Rotate x-axis labels
plt.xticks(rotation=90,fontsize=size)
# Add labels
plt.xlabel('Subcategory',fontsize=size)
plt.ylabel('# "Phone" devices on IFixit (total = 210)',fontsize=size)
plt.title('7 sub-categories inside category "Phone" ',fontsize=size)

# Show the plot
plt.show()

len(phones_df)

# %%
# plot devices per category

# Set the figure size
plt.figure(figsize=(8, 5))

# Create a countplot
sns.countplot(data=df, x='Category', palette='viridis')
# Rotate x-axis labels
plt.xticks(rotation=90,fontsize=size)
# Add labels
plt.xlabel('Category',fontsize=size)
plt.ylabel('# devices on IFixit (3623 total)',fontsize=size)
plt.title('16 device categories in IFixit ',fontsize=size)

# Show the plot
plt.show()

len(df.Device.unique())

#%%
# Function to plot pie chart for each category
def plot_pie_charts(df):
    # Group by Category and Subcategory, and count the occurrences
    category_counts = df.groupby(['Category', 'Subcategory']).size().unstack(fill_value=0)
    
    # Loop through each category and create a pie chart for the subcategories
    for category, subcategory_counts in category_counts.iterrows():
        # Plot the pie chart
        plt.figure(figsize=(6, 6))
        subcategory_counts.plot(kind='pie',
                                #autopct='%1.1f%%',
                                startangle=90,
                                labels=subcategory_counts.index,
                                legend=False)
        plt.title(f"Subcategory Distribution for {category}")
        plt.ylabel('')  # Hide the y-axis label
        plt.show()

# Call the function to plot pie charts
plot_pie_charts(df)
# %%

# Function to plot pie charts for each category in a 4x4 grid layout
def plot_pie_charts(df):
    # Group by Category and Subcategory, and count the occurrences
    category_counts = df.groupby(['Category', 'Subcategory']).size().unstack(fill_value=0)
    
    # Create a 4x4 grid for plotting
    fig, axes = plt.subplots(4, 4, figsize=(16, 16))
    axes = axes.flatten()  # Flatten the 2D array of axes to easily iterate over
    
    # Loop through each category and create a pie chart for the subcategories
    for idx, (category, subcategory_counts) in enumerate(category_counts.iterrows()):
        # Plot the pie chart on the corresponding subplot
        ax = axes[idx]
        subcategory_counts.plot(kind='pie', 
                                ax=ax,
                                labels=subcategory_counts.index,
                                legend=False, 
                                startangle=90,
                                autopct=None)  # Remove percentages
        ax.set_title(f"Subcategory Distribution for {category}")
        ax.set_ylabel('')  # Hide the y-axis label
        
    # Adjust the layout to make sure there's no overlap
    plt.tight_layout()
    plt.show()

# Call the function to plot pie charts
plot_pie_charts(df)
# %%
