import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from fpdf import FPDF
from datetime import datetime


# --------------------------------------- Source #1 --------------------------------------- #

# Read from source - Israel wars 
df_html_wars_orig = pd.read_html('https://en.wikipedia.org/wiki/List_of_wars_involving_Israel')

# Extract relevant table from source
df_html_wars = df_html_wars_orig[1]

# Rename table columns
df_html_wars.columns = ['War Name','Combatant #1', 'Combatant #2', 'Results', 'Israeli Prime Minister',
                 'Defense Minister of Israel', 'Chief of Staff of the IDF', 'IDF Forces Losses', 'Civilians Losses']

# Get read of problematic characters in strings
df_html_wars = df_html_wars.replace(r'\[\d{1,3}\]', '', regex=True)
df_html_wars = df_html_wars.replace('–', '-', regex=True)
df_html_wars = df_html_wars.replace(r'[\u05B2\u00A0]', '', regex=True)

# Replace text in 'Results' column for specific result - Victory, Defeat, Stalemate  
# # define peaces of text indicating victory
def is_victory(item):
    victory_lower = ['victory','both sides claimed victory','tactical victories','accord']
    for value in victory_lower:
        if value in item.lower():
            return True   
# # replace relevant values with 'Victory'
df_html_wars['Results'] = df_html_wars['Results'].apply(lambda item : 'Victory' if is_victory(item) else ('Defeat' if 'defeat' in item.lower() else 'Stalemate'))


# Convert string values in 'Combatant #1' and 'Combatant #2' columns to lists
def string_to_list(item):
    splited_item = item.split()
    return splited_item
df_html_wars['Combatant #1'] = df_html_wars['Combatant #1'].apply(lambda item : string_to_list(item))
df_html_wars['Combatant #2'] = df_html_wars['Combatant #2'].apply(lambda item : string_to_list(item))

# Replace empty or NULL values with 0 in 'Civilians Losses' column
df_html_wars['Civilians Losses'] = df_html_wars['Civilians Losses'].fillna('0').replace('None', '0') 

# Split war name from war years
df_html_wars[['War Name','War Years']] = df_html_wars['War Name'].str.split('(', expand=True)

# Remove bracket and spaces from 'War Years' column
df_html_wars[['War Name', 'War Years']] = df_html_wars[['War Name', 'War Years']].applymap(lambda item: item.replace(')', '').rstrip())


# Save to CSV
# df_html_wars.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\Israel_Wars.csv", encoding='utf-8', index=False)


# --------------------------------------- Source #2 --------------------------------------- #

# Read from csv - Wars duration
df_csv = pd.read_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\sources\csv\Israel_Wars_Duration.csv",encoding='cp1252')

# Get read of problematic characters in strings
df_csv = df_csv.replace(r'\[\d{1,3}\]', '', regex=True)
df_csv = df_csv.replace('–', '-', regex=True)
df_csv = df_csv.replace(r'[\u05B2\u00A0]', '', regex=True)


# --------------------------------------- Source #3 --------------------------------------- #


# Read from source - Israel Demographics
df_html_demographics_orig = pd.read_html('https://he.wikipedia.org/wiki/%D7%93%D7%9E%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%94_%D7%A9%D7%9C_%D7%99%D7%A9%D7%A8%D7%90%D7%9C')

# Extract relevant table from source
df_html_demographics = df_html_demographics_orig[4]

# Keep needed columns only : Year, Population
df_html_demographics = df_html_demographics[['שנה', 'אוכלוסייה (אלפים)']]

# Rename column names
df_html_demographics = df_html_demographics.rename(columns={'שנה':'Year', 'אוכלוסייה (אלפים)':'Population (K)'})

# Duplicate row 0 and modify the Year
row_to_insert = df_html_demographics.iloc[0].copy()
row_to_insert['Year'] = 1947

# Insert the modified row at the beginning of the DataFrame
df_html_demographics = pd.concat([pd.DataFrame([row_to_insert]), df_html_demographics], ignore_index=True)

# print(df_html_demographics)

df_html_demographics.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\df_html_demographics.csv", encoding='utf-8', index=False)


# --------------------------------------- Join Source #1 + Source #2 --------------------------------------- #

df_joined = pd.merge(df_html_wars,df_csv,left_on='War Name',right_on='War Name', how='outer')

# df_joined.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\df_joined.csv", encoding='utf-8', index=False)

# Define columns appearing twice - without 'War Name' , 'Duration Dates' which appear once
columns_to_combine = ['Combatant #1', 'Combatant #2', 'Results', 'Israeli Prime Minister',
                      'Defense Minister of Israel', 'Chief of Staff of the IDF', 'IDF Forces Losses', 'Civilians Losses','War Years']

# Make a copy of joined data frame
df_combined = df_joined.copy()

# Add new columns to the copy which are the combination of _x and -y
for col in columns_to_combine:
    df_combined[col] = df_joined[f"{col}_x"].combine_first(df_joined[f"{col}_y"])

# Drop the _x and _y columns
df_combined = df_combined.drop(columns=[f"{col}_x" for col in columns_to_combine] +[f"{col}_y" for col in columns_to_combine])

# Calc 'Duration time'
def calc_dur_time(duration_dates):
# Given string with start and end dates

    # Split the string into two parts: start date and end date
    start_date_str, end_date_str = duration_dates.split(" - ")

    # Convert the date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%B %d, %Y")

    if not "Ongoing" in duration_dates:
        end_date = datetime.strptime(end_date_str, "%B %d, %Y")

        # Calculate the duration in days
        duration_days = (end_date - start_date).days

        # Determine the appropriate format (days, months, years)
        if duration_days < 30:
            # Less than a month, display in days
            txt = f"Duration: {duration_days} days"
            return txt
        elif duration_days < 365:
            # Less than a year, display in months
            months = duration_days // 30  # Approximate month calculation
            days = duration_days % 30
            txt = f"Duration: {months} months"
            return txt
        else:
            # More than a year, display in years, months, and days
            years = duration_days // 365
            remaining_days = duration_days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            txt = f"Duration: {years} years"
            return txt     
    else: 
        end_date = datetime.now() # today

        # Calculate the duration in days
        duration_days = (end_date - start_date).days   

        # Determine the appropriate format (days, months, years)
        if duration_days < 30:
            # Less than a month, display in days
            txt = f"Duration: {duration_days}+ days"
            return txt
        elif duration_days < 365:
            # Less than a year, display in months
            months = duration_days // 30  # Approximate month calculation
            days = duration_days % 30
            txt = f"Duration: {months}+ months"
            return txt
        else:
            # More than a year, display in years, months, and days
            years = duration_days // 365
            remaining_days = duration_days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            txt = f"Duration: {years}+ years"
            return txt                  


df_combined['Duration time'] = df_combined['Duration Dates'].apply(lambda item : calc_dur_time(item))



df_combined.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\df_combined.csv", encoding='utf-8', index=False)



# # --------------------------------------- Analyze Sources --------------------------------------- #

# # 1) Count wars per results - bar chart + pie chart # #


# Group by 'Results' 
df_combined_agg = df_combined['Results'].value_counts()
print(df_combined_agg)

# Bar graph legend
ax = df_combined_agg.plot(kind='bar')

for i, count in enumerate(df_combined_agg):
    ax.text(i, count, str(count), ha='center', va='bottom')  # Annotate each bar with its count

# plt.show()

# Pie chart with legend showing percentages
plt.pie(df_combined_agg, labels=df_combined_agg.index, autopct='%1.1f%%') 
plt.legend(df_combined_agg.index, title="Results")

# plt.show()

# --------------------------------------

# # 5) Losses by wars # #

# IDF 
# Group by 'Results' 
# Get rid of problematic characters in strings
df_combined = df_combined.replace(r'[+,\u05B2\u00A0]', '', regex=True)
df_combined['IDF Forces Losses'] = df_combined['IDF Forces Losses'].apply(lambda item : int(item))

df_combined_agg = df_combined.groupby('War Name')['IDF Forces Losses'].sum().sort_values(ascending=False) 
print(df_combined_agg)
ax = df_combined_agg.plot(kind='bar')

# Add annotations to each bar
for i, (war_name, value) in enumerate(df_combined_agg.items()):
    ax.text(i, value + 10, str(value), ha='center', va='bottom')

# Set labels and title
ax.set_xlabel('War Name')
ax.set_ylabel('Sum of IDF Forces Losses')
ax.set_title('Sum of IDF Forces Losses by War')

# Add a dummy legend (if desired)
ax.legend(['Total Losses'], title='Legend')

# plt.show()

# Civilians
# Group by 'Results' 
# Get rid of problematic characters in strings
df_combined['Civilians Losses'] = df_combined['Civilians Losses'].replace(r'[+,\u05B2\u00A0~]', '', regex=True)
df_combined.loc[1,'Civilians Losses'] = df_combined.loc[1,'Civilians Losses'].replace('2-3','3')
df_combined['Civilians Losses'] = df_combined['Civilians Losses'].apply(lambda item : int(item))

df_combined_agg = df_combined.groupby('War Name')['Civilians Losses'].sum().sort_values(ascending=False) 
print(df_combined_agg)
ax = df_combined_agg.plot(kind='bar')

# Add annotations to each bar
for i, (war_name, value) in enumerate(df_combined_agg.items()):
    ax.text(i, value + 10, str(value), ha='center', va='bottom')

# Set labels and title
ax.set_xlabel('War Name')
ax.set_ylabel('Sum of Civilians Losses')
ax.set_title('Sum of Civilians Losses by War')

# Add a dummy legend (if desired)
ax.legend(['Total Losses'], title='Legend')

# plt.show()

# both
# Group by 'Results' 
# Get rid of problematic characters in strings
df_combined = df_combined.replace(r'[+,\u05B2\u00A0]', '', regex=True)
df_combined['Civilians Losses'] = df_combined['Civilians Losses'].replace(r'[+,\u05B2\u00A0~]', '', regex=True)
df_combined.loc[1,'Civilians Losses'] = df_combined.loc[1,'Civilians Losses'].replace('2-3','3')
df_combined['IDF Forces Losses'] = df_combined['IDF Forces Losses'].apply(lambda item : int(item))
df_combined['Civilians Losses'] = df_combined['Civilians Losses'].apply(lambda item : int(item))
df_combined['All Losses'] = df_combined['IDF Forces Losses'] + df_combined['Civilians Losses']
print(df_combined['All Losses'])

df_combined_agg = df_combined.groupby('War Name')['All Losses'].sum().sort_values(ascending=False) 
print(df_combined_agg)
ax = df_combined_agg.plot(kind='bar')

# Add annotations to each bar
for i, (war_name, value) in enumerate(df_combined_agg.items()):
    ax.text(i, value + 10, str(value), ha='center', va='bottom')

# Set labels and title
ax.set_xlabel('War Name')
ax.set_ylabel('Sum of All Losses')
ax.set_title('Sum of All Losses by War')

# Add a dummy legend (if desired)
ax.legend(['Total Losses'], title='Legend')

# plt.show()


# --------------------------------------

# # 4) Wars per duration # #
def dur_block(item):
    if '1 months' in item or 'days' in item:
        return 'less than a month'
    elif 'months' in item:
        return '1-11 months'
    else: return '1 year and above'
df_combined['Duartion blocks'] =  df_combined['Duration time'].apply(lambda item : dur_block(item))
print(df_combined['Duartion blocks'])


# Group by 'Results' 
# Get rid of problematic characters in strings
df_combined = df_combined.replace(r'[+,\u05B2\u00A0]', '', regex=True)

df_combined_agg = df_combined['Duartion blocks'].value_counts()
print(df_combined_agg)
ax = df_combined_agg.plot(kind='bar')

# Add annotations to each bar
for i, (war_name, value) in enumerate(df_combined_agg.items()):
    ax.text(i, value + 10, str(value), ha='center', va='bottom')

# Set labels and title
ax.set_xlabel('War Dyaration')
ax.set_ylabel('Sum of Wars')
ax.set_title('Sum of Wars by Duration')

# Add a dummy legend (if desired)
ax.legend(['count wars'], title='Legend')

# plt.show()

# --------------------------------------

# # # 6) Wars per Prime Minister # #
# Count the number of each result per Prime Minister
df_combined_agg = df_combined.groupby('Israeli Prime Minister')['Results'].value_counts().unstack().fillna(0)

# Aggregate number of wars and number of 'Victory'
df_combined_agg['Total Wars'] = df_combined_agg.sum(axis=1)
df_combined_agg['Victory'] = df_combined_agg.get('Victory', 0)

# Calculate percentage of Victory
df_combined_agg['Victory %'] = (df_combined_agg['Victory'] / df_combined_agg['Total Wars']) * 100

# Print the aggregated DataFrame
print(df_combined_agg[['Total Wars', 'Victory', 'Victory %']])

# Plotting
ax = df_combined_agg[['Total Wars', 'Victory']].plot(kind='bar')

# Add annotations to each bar
for i, (index, row) in enumerate(df_combined_agg.iterrows()):
    # ax.text(i - 0.2, row['Total Wars'] + 0.5, f"Total: {int(row['Total Wars'])}", ha='center', va='bottom')
    ax.text(i + 0.2, row['Victory'] + 0.5, f"Victory: ({row['Victory %']:.1f}%)", ha='center', va='bottom')

# # Set labels and title
# ax.set_xlabel('Israeli Prime Minister')
# ax.set_ylabel('Count')
# ax.set_title('Count of Wars and Victories by Prime Minister')

# # Show plot
# plt.show()


# --------------------------------------

# # # 2) Wars through the years # #

# add a column of start year
df_combined['War Years'] = df_combined['War Years'].astype(str)
df_combined['War Start Year'] = df_combined['War Years'].apply(lambda item : item.split("-")[0].replace(" ","")).astype(str).apply(lambda item : item.replace(".0","")).astype(int)

# create new df that hold necessary data only - War Name & War Start Year
wars  = df_combined[['War Name','War Start Year']]

# print(wars)

# Your data
war_names = df_combined['War Name']
start_years = df_combined['War Start Year']

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the data
ax.plot(start_years, [1] * len(start_years), 'ro')  # Red dots for each war


# Initialize a dictionary to keep track of label offsets for each year
label_offsets = {}

# Add vertical labels closer to the dots
for war_name, start_year in zip(war_names, start_years):
    # Combine war name and year for the label
    label = f"{war_name}"
    
    # Calculate an offset if there are multiple labels for the same year
    if start_year in label_offsets:
        label_offsets[start_year] += 0.023  # Smaller increase for closer labels
    else:
        label_offsets[start_year] = 1.01  # Initial closer offset for labels

    # Plot the war name label with the calculated offset and vertical rotation
    ax.text(start_year, label_offsets[start_year], label, ha='center', va='bottom', rotation=90)
    
    # Plot the year under the dot
    ax.text(start_year, 0.998, start_year, ha='center', va='top', fontsize=10, rotation=75)

# Customize the plot
ax.set_yticks([])  # Hide y-axis ticks
ax.set_xlabel('Year')
ax.set_title('Timeline of Wars')

# Show the plot
plt.tight_layout()
# plt.show()


# --------------------------------------

# # # 3) Wars through the years # 

# Create DataFrames for each dataset

population_data = df_html_demographics[['Year','Population (K)']]
losses_data = df_html_demographics[['Start Year','All Losses']]

df_population = pd.DataFrame(population_data)
df_losses = pd.DataFrame(losses_data)

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Population
ax1.plot(df_population['Year'], df_population['Population (K)'], color='blue', label='Population (K)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Population (K)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for losses
ax2 = ax1.twinx()
ax2.plot(df_losses['Start Year'], df_losses['All Losses'], color='red', label='All Losses', linestyle='--')
ax2.set_ylabel('All Losses', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add titles and legends
fig.suptitle('Population Growth and Losses Over the Years')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show plot
plt.show()