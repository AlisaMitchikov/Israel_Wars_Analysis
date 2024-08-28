import pandas as pd
from matplotlib import pyplot as plt

# --------------------------------------- Source #1 --------------------------------------- #

# Read from source - Israel wars
df = pd.read_html('https://en.wikipedia.org/wiki/List_of_wars_involving_Israel')

# Extract relevant table from source
my_df = df[1]

# Rename table columns
my_df.columns = ['War Name','Combatant #1', 'Combatant #2', 'Results', 'Israeli Prime Minister',
                 'Defense Minister of Israel', 'Chief of Staff of the IDF', 'IDF Forces Losses', 'Civilians Losses']

# Get read of problematic characters in strings
my_df = my_df.replace(r'\[\d{1,3}\]', '', regex=True)
my_df = my_df.replace('–', '-', regex=True)
my_df = my_df.replace(r'[\u05B2\u00A0]', '', regex=True)

# Replace text in 'Results' column for specific result - Victory, Defeat, Stalemate  
# # define peaces of text indicating victory
def is_victory(item):
    victory_lower = ['victory','both sides claimed victory','tactical victories','accord']
    for value in victory_lower:
        if value in item.lower():
            return True   
# # replace relevant values with 'Victory'
my_df['Results'] = my_df['Results'].apply(lambda item : 'Victory' if is_victory(item) else ('Defeat' if 'defeat' in item.lower() else 'Stalemate'))


# Convert string values in 'Combatant #1' and 'Combatant #2' columns to lists
def string_to_list(item):
    splited_item = item.split()
    return splited_item
my_df['Combatant #1'] = my_df['Combatant #1'].apply(lambda item : string_to_list(item))
my_df['Combatant #2'] = my_df['Combatant #2'].apply(lambda item : string_to_list(item))

# Replace empty or NULL values with 0 in 'Civilians Losses' column
my_df['Civilians Losses'] = my_df['Civilians Losses'].fillna('0').replace('None', '0') 

# Save to CSV
# my_df.to_csv(r"E:\קריירה\הכנה 2024\פרוייקטים\analysis\app\Israel_Wars.csv", encoding='utf-8', index=False)

# Print data
# print(my_df)
# print(my_df['Combatant #1'] )


# --------------------------------------- Analyze Sources --------------------------------------- #

# Group by 'Results'
my_df_agg = my_df['Results'].value_counts()
print(my_df_agg)

my_df_agg.plot(kind='bar')
plt.show()
