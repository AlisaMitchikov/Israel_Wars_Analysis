import pandas as pd
from matplotlib import pyplot as plt
from fpdf import FPDF

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

# Create a plot and save it to a file
plt.figure(figsize=(8, 6))  # Increase figure size for a larger graph
my_df_agg.plot(kind='bar')
plt.title('War Results')
plt.xlabel('Result')
plt.ylabel('Count')

# Save the plot as an image
plot_image_path = 'plot_image.png'
plt.savefig(plot_image_path, format='png')
plt.close()

# Prepare textual data for the PDF
textual_data = my_df_agg.to_string()

# Create a PDF document
pdf = FPDF()
pdf.add_page()

# Add title to the PDF
pdf.set_font("Arial", size=16)
pdf.set_xy(10, 10)
pdf.cell(0, 10, 'Analysis of Israel Wars', ln=True, align='C')

# Define dimensions and positions for side-by-side layout
text_x = 20
text_y = 30  # Start position after title
text_w = 60  # Width of the text block
text_h = 60  # Height of the text block
image_x = 90  # Position the image to the right of the text
image_y = 30
image_w = 100 # Width of the image

# Draw a black frame around the text
pdf.set_draw_color(0, 0, 0)  # Set color to black for the border
pdf.set_fill_color(255, 255, 255)  # Set fill color to white for the text background
pdf.rect(text_x - 1, text_y - 1, text_w + 2, text_h + 2, style='D')  # Draw rectangle with border

# Add textual data to the PDF
pdf.set_xy(text_x, text_y)
pdf.set_font("Arial", size=10)
pdf.multi_cell(text_w, 10, textual_data)

# Add plot image to the PDF
pdf.image(plot_image_path, x=image_x, y=image_y, w=image_w)

# Save the PDF to a file
pdf_output_path = 'output.pdf'
pdf.output(pdf_output_path)

print(f"PDF saved as {pdf_output_path}")