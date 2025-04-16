#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create the data
data = {
    'year': [2021, 2021],
    'status': ['collected', 'not collected'],
    'value': [0.3, 0.7]
}

# Create the DataFrame
df = pd.DataFrame(data)

#%%
# pie chart

# Set font size for all plot elements
font_size = 20
plt.rcParams.update({'font.size': font_size})

# Create the figure
fig, ax = plt.subplots(figsize=(6, 5))

# Create pie chart
ax.pie(
    df['value'],
    labels=df['status'],
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.viridis(range(len(df)))  # Using the 'viridis' colormap
)

# Equal aspect ratio ensures pie is drawn as a circle
ax.axis('equal')

# Set title
plt.title('E-waste in Germany')

# Show the plot
plt.show()

# %%
import pandas as pd

# Known collected value (30% of total waste)
collected = 160063700  # tons

# Calculate total waste (100%)
total = collected / 0.30  # tons

# Calculate uncollected waste (70%)
not_collected = total * 0.70  # tons

# 50% of uncollected waste is wrongly disposed
wrong_disposal = not_collected * 0.50  # tons

# Illegal exports (part of wrongly disposed waste)
illegal_exports = 155000  # tons

# Remaining wrongly disposed waste (other, e.g., landfill)
other_wrong_disposal = wrong_disposal - illegal_exports  # tons

# "?" inside Not Collected (value left after wrong disposal)
not_collected_questionable = not_collected - wrong_disposal  # tons

# Subcategories for Collected
household = collected * 0.92  # tons
industry = collected * 0.08  # tons

# Convert everything to kilotons (kt) by dividing by 1,000 and round to integer
collected_kt = round(collected / 1000)  # kilotons
total_kt = round(total / 1000)  # kilotons
not_collected_kt = round(not_collected / 1000)  # kilotons
wrong_disposal_kt = round(wrong_disposal / 1000)  # kilotons
illegal_exports_kt = round(illegal_exports / 1000)  # kilotons
other_wrong_disposal_kt = round(other_wrong_disposal / 1000)  # kilotons
not_collected_questionable_kt = round(not_collected_questionable / 1000)  # kilotons
household_kt = round(household / 1000)  # kilotons
industry_kt = round(industry / 1000)  # kilotons

# Prepare data for DataFrame in kilotons (kt)
data = [
    {"category": "Collected", "subcategory": "Household", "sub_subcategory": "", "value_kt": household_kt},
    {"category": "Collected", "subcategory": "Industry", "sub_subcategory": "", "value_kt": industry_kt},
    {"category": "Not Collected", "subcategory": "?", "sub_subcategory": "", "value_kt": not_collected_questionable_kt},
    {"category": "Not Collected", "subcategory": "Wrong Disposal", "sub_subcategory": "Illegal Export", "value_kt": illegal_exports_kt},
    {"category": "Not Collected", "subcategory": "Wrong Disposal", "sub_subcategory": "Other (e.g., Landfill)", "value_kt": other_wrong_disposal_kt}
]

# Create DataFrame
df_kt = pd.DataFrame(data)

# Display the DataFrame with rounded kilotons values
print(df_kt)


# %%
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
import math
import pandas as pd

# Sample DataFrame similar to your df_kt
data = {
    'category': ['Collected', 'Collected', 'Not Collected', 'Not Collected', 'Not Collected'],
    'subcategory': ['Household', 'Industry', '?', 'Wrong Disposal', 'Wrong Disposal'],
    'sub_subcategory': [None, None, None, 'Illegal Export', 'Other (e.g., Landfill)'],
    'value_kt': [147259, 12805, 186741, 155, 186586]
}

# Create the DataFrame
df_kt = pd.DataFrame(data)

#%%

# Style choice
plt.style.use('fivethirtyeight')

# Create figure and assign axis objects
fig = plt.figure(figsize=(15,7.5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Pie chart data (Collected vs Not Collected)
collected = df_kt[df_kt['category'] == 'Collected']['value_kt'].sum()
not_collected = df_kt[df_kt['category'] == 'Not Collected']['value_kt'].sum()
pie_ratios = [collected, not_collected]
pie_labels = ['Collected', 'Not Collected']
pie_explode = [0.1, 0]  # Highlight the 'Collected' slice

# Pie chart parameters (rotate to position the first wedge)
angle = -180 * (pie_ratios[0] / sum(pie_ratios))
ax1.pie(pie_ratios, autopct='%1.1f%%', startangle=angle,
        labels=pie_labels, explode=pie_explode)

# Bar chart parameters (subcategories for Collected and Not Collected)
bar_ratios = []
bar_labels = []
bar_colors = ['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']

# Collect data for bar chart
for _, row in df_kt.iterrows():
    bar_ratios.append(row['value_kt'])
    if row['sub_subcategory'] is None:
        bar_labels.append(row['subcategory'])
    else:
        bar_labels.append(f"{row['subcategory']} -> {row['sub_subcategory']}")

# Bar chart settings
xpos = 0
bottom = 0
width = 0.2

# Create the stacked bar chart
for j in range(len(bar_ratios)):
    height = bar_ratios[j]
    ax2.bar(xpos, height, width, bottom=bottom, color=bar_colors[j % len(bar_colors)])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, f"{height/1000:.0f}k", ha='center')  # Add value labels in kilotons

# Labels and titles
ax2.set_title('Waste Breakdown by Subcategory')
ax2.set_xticks([xpos])
ax2.set_xticklabels(['Waste Subcategories'])
ax2.legend(bar_labels, loc='upper left', fontsize=10)

# Add a line connecting the pie chart to the bar chart using ConnectionPatch
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r

# Connect 'Collected' pie slice to bar chart
x = r * np.cos(math.pi / 180 * theta2) + center[0]
y = np.sin(math.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, sum(bar_ratios[:2])), xyB=(x, y),
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(2)
ax2.add_artist(con)

# Connect 'Not Collected' pie slice to bar chart
x = r * np.cos(math.pi / 180 * theta1) + center[0]
y = np.sin(math.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, sum(bar_ratios[:3])), xyB=(x, y),
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(2)

# Add title to the figure
plt.suptitle('Waste Distribution Breakdown', fontsize=16)

# Hide axis and display the chart
ax2.axis('off')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.tight_layout()
plt.show()



# %%


# Style choice
plt.style.use('fivethirtyeight')

# Create figure and assign axis objects
fig = plt.figure(figsize=(15,7.5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Pie chart data (Collected vs Not Collected)
collected = df_kt[df_kt['category'] == 'Collected']['value_kt'].sum()
not_collected = df_kt[df_kt['category'] == 'Not Collected']['value_kt'].sum()
pie_ratios = [collected, not_collected]
pie_labels = ['Collected', 'Not Collected']
pie_explode = [0.1, 0]  # Highlight the 'Collected' slice

# Pie chart parameters (rotate to position the first wedge)
angle = -180 * (pie_ratios[0] / sum(pie_ratios))
ax1.pie(pie_ratios, autopct='%1.1f%%', startangle=angle,
        labels=pie_labels, explode=pie_explode)

# Bar chart parameters (subcategories for Collected and Not Collected)
collected_ratios = df_kt[df_kt['category'] == 'Collected']['value_kt'].tolist()
not_collected_ratios = df_kt[df_kt['category'] == 'Not Collected']['value_kt'].tolist()

# Color choices for subcategories
collected_colors = ['#4CAF50', '#FF9800']  # Household, Industry
not_collected_colors = ['#2196F3', '#F44336', '#9C27B0']  # ?, Wrong Disposal

# Bar chart settings
width = 0.2
xpos_collected = 0  # X position for collected categories bar
xpos_not_collected = 1  # X position for not collected categories bar

# Left bar (Collected)
bottom = 0
for j in range(len(collected_ratios)):
    height = collected_ratios[j]
    ax2.bar(xpos_collected, height, width, bottom=bottom, color=collected_colors[j])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos_collected, ypos, f"{height/1000:.0f}k", ha='center')  # Add value labels in kilotons

# Right bar (Not Collected)
bottom = 0
for j in range(len(not_collected_ratios)):
    height = not_collected_ratios[j]
    ax2.bar(xpos_not_collected, height, width, bottom=bottom, color=not_collected_colors[j])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos_not_collected, ypos, f"{height/1000:.0f}k", ha='center')  # Add value labels in kilotons

# Labels and titles
ax2.set_title('Waste Breakdown by Subcategory')
ax2.set_xticks([xpos_collected, xpos_not_collected])
ax2.set_xticklabels(['Collected', 'Not Collected'])
ax2.legend(['Household', 'Industry', '?', 'Wrong Disposal', 'Illegal Export', 'Other'], loc='upper left', fontsize=10)

# Add a line connecting the pie chart to the bar chart using ConnectionPatch
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r

# Connect 'Collected' pie slice to bar chart (left side)
x = r * np.cos(math.pi / 180 * theta2) + center[0]
y = np.sin(math.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, sum(collected_ratios)), xyB=(x, y),
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(2)
ax2.add_artist(con)

# Connect 'Not Collected' pie slice to bar chart (right side)
x = r * np.cos(math.pi / 180 * theta1) + center[0]
y = np.sin(math.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, sum(not_collected_ratios)), xyB=(x, y),
                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(2)

# Add title to the figure
plt.suptitle('Waste Distribution Breakdown', fontsize=16)

# Hide axis and display the chart
ax2.axis('off')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.tight_layout()
plt.show()

# %%
import plotly.graph_objects as go

# Define the labels (categories, subcategories)
# Define the labels (categories, subcategories)
labels = [
    'Total', 'Collected', 'Not Collected', 'Household', 'Industry', 
    '?', 'Wrong Disposal', 'Illegal Export', 'Other (e.g., Landfill)'
]

# Define the parents (who belongs to whom)
parents = [
    '', 'Total', 'Total', 'Collected', 'Collected', 
    'Not Collected', 'Not Collected', 'Wrong Disposal', 'Wrong Disposal'
]

# Define the values (amounts per category/subcategory)
values = [
    533546, 160064, 373482, 147259, 12805, 
    186741, 186741, 155, 186586
]

# Create the Sunburst chart
trace = go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",  # Use total to make parent values sum correctly
    outsidetextfont={"size": 20, "color": "#377eb8"},
    marker={"line": {"width": 2}},
)

# Set the layout
layout = go.Layout(
    margin=go.layout.Margin(t=0, l=0, r=0, b=0)
)

# Define the figure and display it
figure = {
    'data': [trace],
    'layout': layout
}

# Show the figure
import plotly.offline as pyo
pyo.iplot(figure)


# %%
import plotly.graph_objects as go

# Define the labels (categories, subcategories)
labels = [
    'Total', 'Collected', 'Not Collected', 'Household', 'Industry', 
    '?', 'Wrong Disposal', 'Illegal Export', 'Other (e.g., Landfill)'
]

# Define the parents (who belongs to whom)
parents = [
    '', 'Total', 'Total', 'Collected', 'Collected', 
    'Not Collected', 'Not Collected', 'Wrong Disposal', 'Wrong Disposal'
]

# Define the values (amounts per category/subcategory)
values = [
    533546, 160064, 373482, 147259, 12805, 
    186741, 186741, 155, 186586  # 155 for Illegal Export, 186586 for Other (e.g., Landfill)
]

# Create the Sunburst chart
trace = go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",  # Use total to make parent values sum correctly
    outsidetextfont={"size": 20, "color": "#377eb8"},
    marker={"line": {"width": 2}},
)

# Set the layout
layout = go.Layout(
    margin=go.layout.Margin(t=0, l=0, r=0, b=0)
)

# Define the figure and display it
figure = {
    'data': [trace],
    'layout': layout
}

# Show the figure
import plotly.offline as pyo
pyo.iplot(figure)

# %%
import pandas as pd

# Known collected value (30% of total waste)
collected = 160064000  # tons

# Calculate total waste (100%)
total = collected / 0.30  # tons

# Calculate uncollected waste (70%)
not_collected = total * 0.70  # tons

# Now 71% of Not Collected is wrongly disposed
wrong_disposal_percentage = 0.71  # 71% of Not Collected waste is wrongly disposed
wrong_disposal = not_collected * wrong_disposal_percentage  # tons

# Illegal exports (part of wrongly disposed waste)
illegal_exports = 155000  # tons

# Remaining wrongly disposed waste (other, e.g., landfill)
other_wrong_disposal = wrong_disposal - illegal_exports  # tons

# "?" inside Not Collected (value left after wrong disposal)
not_collected_questionable = not_collected - wrong_disposal  # tons

# Subcategories for Collected
household = collected * 0.92  # tons
industry = collected * 0.08  # tons

# Convert from tons to kilotons for all calculations
collected_kt = collected / 1000
total_kt = total / 1000
not_collected_kt = not_collected / 1000
wrong_disposal_kt = wrong_disposal / 1000
illegal_exports_kt = illegal_exports / 1000
other_wrong_disposal_kt = other_wrong_disposal / 1000
not_collected_questionable_kt = not_collected_questionable / 1000
household_kt = household / 1000
industry_kt = industry / 1000

# Creating the DataFrame with 3 levels of categories (Category, Subcategory, Sub-Subcategory)
data = {
    'Category': [
        'Collected', 'Collected', 'Collected',  # Collected and its subcategories
        'Not Collected', 'Not Collected', 'Not Collected', 'Not Collected', 'Not Collected',  # Not Collected and its subcategories
    ],
    'Subcategory': [
        'Household', 'Industry', 'Unknown',  # Collected subcategories
        'Unknown', 'Wrong Disposal', 'Illegal Export', 'Other (e.g., Landfill)', 'Unknown',  # Not Collected subcategories
    ],
    'Sub-Subcategory': [
        'Unknown', 'Unknown', 'Unknown',  # Collected sub-subcategories
        'Unknown', 'Illegal Export', 'Illegal Export', 'Other (Landfill)', 'Unknown',  # Not Collected sub-subcategories
    ],
    'Value (kt)': [
        round(household_kt), round(industry_kt), round(0),  # Collected values
        round(not_collected_questionable_kt), round(wrong_disposal_kt), round(illegal_exports_kt), round(other_wrong_disposal_kt), round(0),  # Not Collected values
    ],
    'Parent': [
        'Collected', 'Collected', 'Collected',  # Parents for Collected subcategories
        'Not Collected', 'Not Collected', 'Not Collected', 'Wrong Disposal', 'Not Collected',  # Parents for Not Collected subcategories
    ]
}

df_3levels = pd.DataFrame(data)

# Display the DataFrame
print(df_3levels)
df = df_3levels

# %%
# Prepare the Sunburst Data
import pandas as pd
import plotly.graph_objects as go

# Input DataFrame (with your provided data)
data = {
    "Category": ['Collected', 'Collected', 'Collected', 'Not Collected', 'Not Collected', 'Not Collected', 'Not Collected', 'Not Collected'],
    "Subcategory": ['Household', 'Industry', 'Unknown', 'Unknown', 'Wrong Disposal', 'Illegal Export', 'Other (e.g., Landfill)', 'Unknown'],
    "Sub-Subcategory": ['Unknown', 'Unknown', 'Unknown', 'Unknown', 'Illegal Export', 'Illegal Export', 'Other (Landfill)', 'Unknown'],
    "Value (kt)": [147259, 12805, 0, 108310, 265173, 155, 265018, 0],
    "Parent": ['Collected', 'Collected', 'Collected', 'Not Collected', 'Not Collected', 'Not Collected', 'Wrong Disposal', 'Not Collected']
}

df = pd.DataFrame(data)

# Step 1: Prepare the Labels, Parents, and Values
# Labels: Unique values from Category, Subcategory, and Sub-Subcategory
labels = pd.concat([df['Category'], df['Subcategory'], df['Sub-Subcategory']]).unique().tolist()

# Step 2: Define Parents
parents = []

# Define parents based on categories, subcategories, and sub-subcategories
for _, row in df.iterrows():
    if row['Sub-Subcategory'] != 'Unknown':  # if there's a subsubcategory
        parents.append(row['Subcategory'])  # the subsubcategory's parent is the subcategory
    elif row['Subcategory'] != 'Unknown':  # if there's only a subcategory
        parents.append(row['Category'])  # the subcategory's parent is the category
    else:
        parents.append('')  # if no subcategory or subsubcategory, no parent

# Step 3: Define Values
values = df['Value (kt)'].tolist()

# Step 4: Create the Sunburst Chart
trace = go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",  # Use total to ensure the sum is correct
    outsidetextfont={"size": 20, "color": "#377eb8"},  # Customize the font
    marker={"line": {"width": 2}},  # Customize borders
)

# Step 5: Layout Settings
layout = go.Layout(
    margin=go.layout.Margin(t=0, l=0, r=0, b=0)
)

# Step 6: Define the figure and display it
figure = {
    'data': [trace],
    'layout': layout
}

# Show the figure
import plotly.offline as pyo
pyo.iplot(figure)

# %%
#######################################
# Known collected value (30% of total waste)
# Known collected value (30% of total waste)
# Known collected value (30% of total waste)
collected = 160064000  # tons

# Calculate total waste (100%)
total_waste = collected / 0.30  # tons
# sammelquote: anteil der inverkehr gebrachten geräte.

# Calculate uncollected waste (70%)
not_collected = total_waste * 0.70  # tons

# Known: 50% of total waste is wrongly disposed (this is 50% of the total waste, not just not_collected)
wrongly_disposed_of_total = total_waste * 0.50  # tons

# Calculate the fraction of wrongly disposed waste out of "not_collected"
wrongly_disposed_fraction = wrongly_disposed_of_total / not_collected

# Calculate wrongly disposed waste (portion of "not_collected")
wrongly_disposed = not_collected * wrongly_disposed_fraction  # tons

# Calculate the "unknown" waste that remains in the "not collected" category
unknown = not_collected - wrongly_disposed  # tons

# Household and Industry Subcategories under Collected
household = collected * 0.30  # 30% of collected goes to Household
industry = collected * 0.70  # 70% of collected goes to Industry

# Known: Illegal Export waste (subcategory of wrongly disposed)
illegal_exports = 155000  # tons

# Calculate Landfill & Other waste (the remainder of wrongly disposed waste)
landfill_other = wrongly_disposed - illegal_exports  # tons

# Create the structured data
data = {
    'Category': [
        'Collected', 'Collected',
        'Not Collected', 'Not Collected', 'Not Collected'
    ],
    'Subcategory': [
        'Household', 'Industry',
        'Unknown', 'Wrongly Disposed', 'Wrongly Disposed'
    ],
    'Sub-Subcategory': [
        np.nan, np.nan,
        np.nan, 'Illegal Export', 'Hausmüll/Landfill'
    ],
    'Value (kt)': [
        48019.2,   # Collected - Household
        112044.8,  # Collected - Industry
        106709.3,  # Not Collected - Unknown
        155,       # Not Collected - Wrongly Disposed - Illegal Export
        266618.3   # Not Collected - Wrongly Disposed - Hausmüll/Landfill
    ]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Value (kt)'] = df['Value (kt)'].round(1)  # one digit after comma

# Show the result
print(df)

#%%
# Debug output - Raw data check
print("Raw Data:\n", df)

# Prepare the data for the sunburst chart
labels = ['Total']  # Start with the root node 'Total'
parents = ['']      # Root node has no parent
values = [df['Value (kt)'].sum()]  # The total value is the sum of all values

# Debug output - Sum of total values
print("\nTotal Value (sum of all categories):", values[0])

# Add the Category level (Collected and Not Collected)
for cat in df['Category'].unique():
    cat_value = df[df['Category'] == cat]['Value (kt)'].sum()
    print(f"Category: {cat}, Total Value: {cat_value}")
    
    labels.append(cat)
    parents.append('Total')
    values.append(cat_value)

# Add the Subcategory level (Household, Industry, Unknown, Wrongly Disposed)
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']
    
    subcat_value = df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum()
    print(f"Subcategory: {subcat}, Parent Category: {cat}, Subcategory Value: {subcat_value}")
    
    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)
        values.append(subcat_value)

# Debug output - Values for 'Wrongly Disposed' category
wrongly_disposed_value = df[df['Subcategory'] == 'Wrongly Disposed']['Value (kt)'].sum()
print("\nTotal 'Wrongly Disposed' Value:", wrongly_disposed_value)

# Manually ensure correct split between Illegal Export and Hausmüll/Landfill
illegal_export_value = 155  # Value for Illegal Export
landfill_value = wrongly_disposed_value - illegal_export_value  # The rest goes to Hausmüll/Landfill

print("Illegal Export Value:", illegal_export_value)
print("Hausmüll/Landfill Value:", landfill_value)

# Add the sub-subcategories under "Wrongly Disposed"
labels.append('Illegal Export')
parents.append('Wrongly Disposed')
values.append(illegal_export_value)

labels.append('Hausmüll/Landfill')
parents.append('Wrongly Disposed')
values.append(landfill_value)

# Debug output - Final labels, parents, and values before building the plot
print("\nLabels:", labels)
print("Parents:", parents)
print("Values:", values)

# Build and display the Sunburst chart
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",  # Ensure correct child-to-parent relationship
    marker=dict(line=dict(width=2))
))

# Update layout and display the chart
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    title="Waste Disposal Categories"
)

fig.show()
# %%
total*10^-6

################################################################

#%%



# Known collected value (30% of total waste)
collected = 160063700  # tons

# Calculate total waste (100%)
total = collected / 0.30  # tons

# Household and Industry proportions
household = collected * 0.92  # 92% of collected goes to Household
industry = collected * 0.08  # 8% of collected goes to Industry

# Calculate uncollected waste (70%)
not_collected = total * 0.70  # tons

# Wrongly disposed waste (equal to the collected amount)
wrongly_disposed = collected  # tons

# In circulation (waste that is not wrongly disposed)
in_circulation = not_collected - wrongly_disposed  # tons

# Illegal export (known value)
illegal_export = 155000  # tons

# Landfill & other (waste that's wrongly disposed but not exported)
landfill_other = wrongly_disposed - illegal_export  # tons

# Update the DataFrame with the new values
# Update the DataFrame with the new values
data = {
    'Category': [
        'Collected', 'Collected', 'Not Collected', 'Not Collected', 'Not Collected', 'Not Collected'
    ],
    'Subcategory': [
        'Household', 'Industry', 'In Circulation', 'Wrongly disposed', 'Wrongly disposed', 'Wrongly disposed'
    ],
    'Sub-Subcategory': [
        None, None, None, None, 'Illegal Export', 'Landfill & other'
    ],
    'Value (kt)': [
        round(household / 1000),   # Collected - Household (in kilotons)
        round(industry / 1000),    # Collected - Industry (in kilotons)
        round(in_circulation / 1000),    # Not Collected - In Circulation (in kilotons)
        round(wrongly_disposed / 1000),   # Not Collected - Wrongly Disposed (in kilotons)
        round(illegal_export / 1000),    # Not Collected - Illegal Export (in kilotons)
        round(landfill_other / 1000)     # Not Collected - Landfill & Other (in kilotons)
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Show the DataFrame
print(df)

# %%
print("Raw Data:\n", df)

# Prepare the data for the sunburst chart
labels = ['Total']  # Start with the root node 'Total'
parents = ['']      # Root node has no parent
values = [df['Value (kt)'].sum()]  # The total value is the sum of all values

# Debug output - Sum of total values
print("\nTotal Value (sum of all categories):", values[0])

# Add the Category level (Collected and Not Collected)
for cat in df['Category'].unique():
    cat_value = df[df['Category'] == cat]['Value (kt)'].sum()
    print(f"Category: {cat}, Total Value: {cat_value}")
    
    labels.append(cat)
    parents.append('Total')
    values.append(cat_value)

# Add the Subcategory level (Household, Industry, Unknown, Wrongly Disposed)
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']
    
    subcat_value = df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum()
    print(f"Subcategory: {subcat}, Parent Category: {cat}, Subcategory Value: {subcat_value}")
    
    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)
        values.append(subcat_value)

# Debug output - Values for 'Wrongly Disposed' category
wrongly_disposed_value = df[df['Subcategory'] == 'Wrongly disposed']['Value (kt)'].sum()
print("\nTotal 'Wrongly disposed' Value:", wrongly_disposed_value)

# Manually ensure correct split between Illegal Export and Hausmüll/Landfill
illegal_export_value = 155  # Value for Illegal Export
#landfill_value = wrongly_disposed_value - illegal_export_value  # The rest goes to Hausmüll/Landfill

print("Illegal Export Value:", illegal_export_value)
print("Hausmüll/Landfill Value:", landfill_other)

# Add the sub-subcategories under "Wrongly Disposed"
labels.append('Illegal Export')
parents.append('Wrongly disposed')
values.append(illegal_export_value)

labels.append('Hausmüll/Landfill')
parents.append('Wrongly disposed')
values.append(landfill_value)

# Debug output - Final labels, parents, and values before building the plot
print("\nLabels:", labels)
print("Parents:", parents)
print("Values:", values)

# Build and display the Sunburst chart
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",  # Ensure correct child-to-parent relationship
    marker=dict(line=dict(width=2))
))

# Update layout and display the chart
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    title="Waste Disposal Categories"
)

fig.show()
# %%
print(df)

# Sunburst plot data
labels = ['Total']
parents = ['']
values = [df['Value (kt)'].sum()]

# Add Category level
for cat in df['Category'].unique():
    labels.append(cat)
    parents.append('Total')
    values.append(df[df['Category'] == cat]['Value (kt)'].sum())

# Add Subcategory level
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']

    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)
        values.append(df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum())

# Add Sub-Subcategory level (only if not NaN)
for idx, row in df.iterrows():
    subsub = row['Sub-Subcategory']
    subcat = row['Subcategory']

    if pd.notna(subsub) and subsub not in labels:
        labels.append(subsub)
        parents.append(subcat)
        values.append(
            df[(df['Subcategory'] == subcat) & (df['Sub-Subcategory'] == subsub)]['Value (kt)'].sum()
        )

# Build the Sunburst chart
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(line=dict(width=2))
))

# Update layout for better visualization
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# Show the plot
fig.show()
print(df)
# %%

# Sunburst plot data: only Category and Subcategory
labels = ['Devices sold / year']
parents = ['']
values = [df['Value (kt)'].sum()]

# Add Category level
for cat in df['Category'].unique():
    labels.append(cat)
    parents.append('Devices sold / year')
    values.append(df[df['Category'] == cat]['Value (kt)'].sum())

# Add Subcategory level (No Sub-Subcategory this time!)
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']

    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)
        values.append(
            df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum()
        )

# Build the simplified 2-ring Sunburst chart
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(line=dict(width=2))
))

fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# Show the plot
fig.show()
print(df)
# %%
# Sunburst setup
labels = ['> 500 megatons \n Devices sold/ year']
parents = ['']
values = [df['Value (kt)'].sum()]

# Category (outer layer)
for cat in df['Category'].unique():
    labels.append(cat)
    parents.append('> 500 megatons \n Devices sold/ year')
    values.append(df[df['Category'] == cat]['Value (kt)'].sum())

# Subcategory (inner layer)
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']
    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)
        values.append(df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum())

# Build the sunburst
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(line=dict(width=2))
))

fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

fig.show()
# %%

# %%
