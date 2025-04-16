#import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%%
# data
# Known collected value (30% of total waste)
collected = 160063700  # tons

# Calculate total waste (100%)
total = collected / 0.38  # tons

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

# Data
# === Real-World E-Waste Flow Calculation ===
# Based on German 2021 data and assumptions

# Official reported collected e-waste (from authorities, in tons)
collected = 1_006_370  # tons (actual, 2021)

# Sammelquote reported by BMUV
sammelquote = 0.386  # 38.6%

# Calculate total "old devices" generated in 2021 (physical waste flow)
total_old_devices = collected / sammelquote  # This assumes 38.6% was collected

# Fact: 50% of all old devices are wrongly disposed
wrongly_disposed = total_old_devices * 0.50  # tons

# Remaining part of old devices that were NOT wrongly disposed = still in circulation or reused
# Logic: Total devices - collected - wrongly disposed
in_circulation = total_old_devices - collected - wrongly_disposed  # tons

# Subcategories within 'collected'
household = 926_719  # tons (from text)
industry = 79_651  # tons (from text)

# Subcategories within 'wrongly disposed'
# Known illegal export figure
illegal_export = 155_000  # tons
landfill_other = wrongly_disposed - illegal_export  # tons

# === Output ===
print("💡 E-Waste Flow Summary (Germany, 2021) 💡")
print(f"Total old devices generated: {total_old_devices:,.0f} tons")
print(f"Collected: {collected:,.0f} tons")
print(f"  - Households: {waste_households:,.0f} tons")
print(f"  - Industry/Public: {waste_industry_public:,.0f} tons")
print(f"Wrongly Disposed: {wrongly_disposed:,.0f} tons")
print(f"  - Illegal Export: {illegal_export:,.0f} tons")
print(f"  - Landfill & Other: {landfill_other:,.0f} tons")
print(f"Still in Circulation / Stored / Reused: {still_in_circulation:,.0f} tons")

#%%
# data frame
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


#%%
# plot
total = df[df['Category'] == " Collected"]

# Sunburst plot data
labels = ['Devices sold/ year']  # Title as the root node
parents = ['']  # Root node has no parent
values = [df['Value (kt)'].sum()]  # Total sum as the root value

# Category (outer layer)
for cat in df['Category'].unique():
    labels.append(cat)
    parents.append('Devices sold/ year')  # Parent is the root node (title)
    values.append(df[df['Category'] == cat]['Value (kt)'].sum())

# Subcategory (inner layer)
for idx, row in df.iterrows():
    subcat = row['Subcategory']
    cat = row['Category']
    if subcat not in labels:
        labels.append(subcat)
        parents.append(cat)  # Parent is the category
        values.append(df[(df['Category'] == cat) & (df['Subcategory'] == subcat)]['Value (kt)'].sum())

# Build the Sunburst chart
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(line=dict(width=2)),
    textinfo="label",  # Only show labels (no values)
    textfont=dict(size=20),  # Set larger font size for all text
))

# Adjust the layout for better positioning of the title and ensure it's centered
fig.update_layout(
    title={
        'text': '> 500 megatons of Devices sold/ year',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'y': 0.95
    },
    margin=dict(t=50, l=0, r=0, b=0)
)

fig.show()
# %%
import plotly.graph_objects as go

# Pie chart data (donut)
labels = ['Devices sold/ year', 'Category A', 'Category B', 'Subcategory A1', 'Subcategory B1']
values = [60, 20, 15, 10, 5]  # Values corresponding to each label

fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Adjust this to control the size of the inner radius
    textinfo="label",  # Only display labels, no numeric values
    textfont=dict(size=18),  # Increase text font size
    pull=[0.1, 0.2, 0.3, 0.4, 0.5],  # Pull slices outward (optional)
))

fig.show()
# %%
df = df.iloc[:-2]
# Remove the 'Sub-Subcategory' column
df = df.drop(columns=['Sub-Subcategory'])

print(df)

#%%

# Sum the 'Value (kt)' by 'Category' for the outer layer
outer_values = df.groupby('Category')['Value (kt)'].sum()

# Prepare the outer labels and their respective colors
outer_labels = outer_values.index
outer_sizes = outer_values.values

# Define the colors for 'Collected' and 'Not Collected' (and shades for their subcategories)
outer_colors = {
    'Collected': '#1f77b4',  # Blue
    'Not Collected': '#ff7f0e'  # Orange
}

# Prepare the inner labels and their respective colors (group by both 'Category' and 'Subcategory')
inner_labels = df['Subcategory'].unique()
inner_sizes = [df[df['Subcategory'] == label]['Value (kt)'].sum() for label in inner_labels]

# Define subcategory colors based on their category
inner_colors = []
for label in inner_labels:
    category = df[df['Subcategory'] == label]['Category'].iloc[0]
    if category == 'Collected':
        inner_colors.append(to_rgba(outer_colors['Collected'], alpha=0.5))  # Lighter shade for subcategories
    else:
        inner_colors.append(to_rgba(outer_colors['Not Collected'], alpha=0.5))  # Lighter shade for subcategories

# Create the plot
fig, ax = plt.subplots()

# First (inner) pie chart layer (Category)
ax.pie(outer_sizes, labels=outer_labels, radius=1, colors=[outer_colors['Collected'], outer_colors['Not Collected']],
       wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance=0.7)

# Second (outer) pie chart layer (Subcategory)
ax.pie(inner_sizes, labels=inner_labels, radius=1-0.3, colors=inner_colors,
       wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance=0.55)

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.set(aspect="equal", title="Pie Chart with Two Layers")

plt.show()
# %%
# INNER layer -> Category
inner_values = df.groupby('Category')['Value (kt)'].sum()
inner_labels = inner_values.index.tolist()
inner_sizes = inner_values.values.tolist()

# Simple color mapping for categories
inner_colors_dict = {
    'Collected': '#74BA9C',        # blue
    'Not Collected': '#E69A8D'     # orange
}
inner_colors = [inner_colors_dict[label] for label in inner_labels]

# OUTER layer -> Subcategory
outer_values = df['Value (kt)'].tolist()
outer_labels = df['Subcategory'].tolist()

# Subcategory inherits parent category color (lighter shade)
outer_colors = []
for i, label in enumerate(outer_labels):
    parent_category = df.loc[df['Subcategory'] == label, 'Category'].values[0]
    base_color = inner_colors_dict[parent_category]
    outer_colors.append(to_rgba(base_color, alpha=0.5))

# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))

# Plot INNER ring first (Category)
ax.pie(inner_sizes, labels=inner_labels, radius=0.7,
       colors=inner_colors,
       wedgeprops=dict(width=0.7, edgecolor='w'),
       labeldistance=0.5)

# Plot OUTER ring second (Subcategory)
ax.pie(outer_values, labels=outer_labels, radius=1,
       colors=outer_colors,
       wedgeprops=dict(width=0.3, edgecolor='w'),
       labeldistance=0.7)

# Final setup
ax.set(aspect="equal", title="Pie Chart: Category Inner, Subcategory Outer")
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Data
sizes = [927, 80, 134790, 1304]

# Simplified subcategory labels
sub_labels = [
    "Correctly\nDisposed\nHousehold", 
    "Industry", 
    "In Circulation", 
    "Wrongly \nDisposed"
]

# Colors for slices (shades based on category)
colors = [
    "#74BA9C",  # Collected - Household
    "#A3CBB3",  # Collected - Industry (less saturated)
    "#F2C0B1",  # Not Collected - In Circulation
    "#E69A8D"   # Not Collected - Wrongly Disposed
]

# Explode Household and Wrongly Disposed as one group
explode = [0.1, 0, 0, 0.1]

# Create pie chart
fig, ax = plt.subplots(figsize=(8, 8))

# Function to replace percentages with your labels
def label_format(pct, allvals):
    index = label_format.counter
    label = sub_labels[index]
    label_format.counter += 1
    return label

label_format.counter = 0

# Create pie with labels inside the slices
wedges, texts, autotexts = ax.pie(
    sizes,
    explode=explode,
    colors=colors,
    startangle=0,
    autopct=lambda pct: label_format(pct, sizes),
    textprops={'color': "black", 'fontsize': 18},
    pctdistance=0.65  # Distance from center
)

# Adjust exploded wedges to move as one group (Household and Wrongly Disposed)
angle_shift = np.deg2rad((wedges[3].theta2 + wedges[0].theta1) / 2)

for i in [0, 3]:
    center = -0 * (wedges[i].r - 0) * np.array([np.cos(angle_shift), np.sin(angle_shift)])
    wedges[i].set_center(center)
    autotexts[i].set_position(np.array(autotexts[i].get_position()) + center)

# Custom legend for main categories
legend_labels = ['Collected', 'Not Collected']
legend_colors = ['#74BA9C', '#E69A8D']

handles = [
    Patch(facecolor=legend_colors[0], label=legend_labels[0]),
    Patch(facecolor=legend_colors[1], label=legend_labels[1])
]

legend = ax.legend(
    handles=handles,
    title="",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=18,
    title_fontsize=18
)

legend.get_frame().set_linewidth(0)   # <--- removes the border
legend.get_frame().set_facecolor('none')  # <--- ensures background is transparent

ax.axis('equal')
plt.title('Electronics in Germany: \nTurnover 2021', fontsize=24)
plt.show()




# %%
