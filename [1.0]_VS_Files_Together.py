# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 23:26:54 2023

@author: lgsse
"""
import pandas as pd
import numpy as np
import re
import os
import io
import glob
import matplotlib.pyplot as plt
print("----------------------------------------------------------------------------")
print("")
print("Developed by: Luiz Gustavo Schultz Senko")
print('Email: lgssenko@gmail.com')
print('')
print("----------------------------------------------------------------------------")
print('')
print('')




# # Ask for user input
# user_filename = input("Please enter a filename (without extension), or press Enter to use the default filename: ")

# # If user provided a filename, use it. Otherwise, use the default filename
# output_filename = user_filename if user_filename else '0_0_VS_Files_Together'

# Specify the output filename without the extension
output_filename = '0_0_VS_Files_Together'

def process_csv_v4(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        table_lines = file.readlines()
    return process_table_v4(table_lines, file_path)

def process_table_v4(table_lines, file_path):
    # Skip processing if the file is the output file
    if os.path.basename(file_path) == output_filename:
        return None

    # Split the lines of the table into two strings, one for each table
    table_string_1 = ''.join(table_lines[:24])  # The first 24 lines form the first table
    table_string_2 = ''.join(table_lines[24:])  # The remaining lines form the second table

    # Convert the strings into StringIO objects so we can read them with pandas
    table_file_1 = io.StringIO(table_string_1)
    table_file_2 = io.StringIO(table_string_2)

    # Read the top table (with 'Hipocotilo' and 'Raiz' columns)
    top_table = pd.read_csv(table_file_1, sep=";", decimal=",", skiprows=2, nrows=24)  # Modify nrows to 24
    
    # Compute the averages of the 'Hipocotilo' and 'Raiz' columns
    if 'Hipocotilo' in top_table.columns and 'Raiz' in top_table.columns:
        hyp_average = top_table['Hipocotilo'].mean()
        root_average = top_table['Raiz'].mean()
    else:
        print(f"No 'Hipocotilo' or 'Raiz' column in file: {file_path}")
        return None

    # Read the bottom table (with all other columns)
    bottom_table = pd.read_csv(table_file_2, sep=";", decimal=",", nrows=1)

    # Extract Cultivar and Repetition from the filename
    #This pattern will match N3D_10ABEC as cultivar N3 and repetition D, ignoring the _10ABEC
    base_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove file extension
    match = re.match(r"([A-Za-z][0-9]+)([A-Za-z])", base_name)
    if match:
        cultivar, repetition = match.groups()
    else:
        print(f"Unexpected filename format: {file_path}")
        return None

    # Add the Cultivar and Repetition columns to the bottom table
    bottom_table.insert(0, "Cultivar", cultivar)
    bottom_table.insert(1, "Repetition", repetition)
    
    # Add the HypAverage and RootAverage columns to the bottom table
    bottom_table["HypAverage"] = hyp_average
    bottom_table["RootAverage"] = root_average

    # Convert 'Germinação' column to numeric format
    bottom_table["Germinação"] = bottom_table["Germinação"].str.replace('%', '').astype(float)
    
    return bottom_table

# Get a list of all .csv file paths
csv_file_paths = glob.glob('*.csv')

# Check if any .csv files were found
if not csv_file_paths:
    print("No .csv files found!")
    print('Place the script inside the folder with Vigor-S .csv files!')
    input("Press Enter to exit...")
    exit()

# Exclude the output file from the list of files to process
csv_file_paths = [path for path in csv_file_paths if os.path.basename(path) != output_filename + '.csv']

# Run the processing function and combine the results into a single DataFrame
combined_data_4 = pd.concat([process_csv_v4(file_path) for file_path in csv_file_paths if process_csv_v4(file_path) is not None])

# Remove leading spaces from column names
combined_data_4.columns = combined_data_4.columns.str.strip()

# Apply rounding to the specified columns
combined_data_4 = combined_data_4.round({'HypAverage': 2, 'RootAverage': 2, 'Vigor': 0, 'Crescimento': 0, 'Uniformidade': 0})

# Apply transformations to the specified columns to create new columns
combined_data_4["HypSTATS"] = (combined_data_4["HypAverage"] + 0.5) ** 0.5
combined_data_4["RootSTATS"] = (combined_data_4["RootAverage"] + 0.5) ** 0.5
combined_data_4["Aver_LenSTATS"] = (combined_data_4["Comprimento Medio"] + 0.5) ** 0.5
combined_data_4["GrowthSTATS"] = (combined_data_4["Crescimento"] + 0.5) ** 0.5
combined_data_4["UniformSTATS"] = (combined_data_4["Uniformidade"] + 0.5) ** 0.5
combined_data_4["VigorSTATS"] = (combined_data_4["Vigor"] + 0.5) ** 0.5
combined_data_4["GerminSTATS"] = np.arcsin(combined_data_4["Germinação"] / 100) ** 0.5

# Rearrange columns
combined_data_4 = combined_data_4[["Cultivar", "Repetition", "HypAverage", "RootAverage", "Comprimento Medio", 
                                   "Vigor", "Crescimento", "Uniformidade", "Germinação", "Desvio Padrao", 
                                   "Plantulas Normais", "Plantulas Anormais", "Sementes nao Germinadas", 
                                   "HypSTATS", "RootSTATS", "Aver_LenSTATS", "GrowthSTATS", "UniformSTATS", 
                                   "VigorSTATS", "GerminSTATS"]]

# Convert DataFrame to string with European number formatting
combined_data_4_str = combined_data_4.to_csv(sep=';', decimal=',', index=False)

# Save the result to a CSV file in the same directory
print("- Saving file...")
output_file_path = os.path.join('.', output_filename + '.csv')

# Write "SEP=;" line and DataFrame to the file
with open(output_file_path, 'w', newline='') as file:
    file.write('SEP=;\n')
    file.write(combined_data_4_str)
    print("- file saved as 0_0_VS_Files_Together.csv")
    print("----------------------------------------------------------------------------")
    print("HypSTATS, RootSTATS, Aver_LenSTATS, GrowthSTATS, UniformSTATS and VigorSTATS")
    print("- Values transformed using (X+0.5)^0.5")
    print('')
    print("----------------------------------------------------------------------------")
    print('GerminSTATS')
    print('- Valuestransformed using arcsin(X/100)^0.5')
    print('')

#__________ UNCOMMENT FOR PLOTS :) ________________________________________________________________________________

def Plot_STATS(df, columns_to_plot, output_filename):
    print("----------------------------------------------------------------------------")
    print('- Ploting simple graphs')
    # Group the data by Cultivar and compute means and standard deviations
    grouped_means = df.groupby('Cultivar')[columns_to_plot].mean()
    grouped_stds = df.groupby('Cultivar')[columns_to_plot].std()

    # Calculate the number of subplot rows and columns
    num_plots = len(columns_to_plot)
    num_cols = 2
    num_rows = num_plots // num_cols + (num_plots % num_cols > 0)
    
    # Define the size of the figure (in inches)
    fig_width = 10   # width of the figure in inches
    fig_height = 3 * num_rows   # height of the figure in inches
    
    # Create a new figure with the specified size
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height))

    # Flatten axs to make it a 1D array
    axs = axs.flatten()

    # Now, plot each column
    for i, column in enumerate(columns_to_plot):
        grouped_means[column].plot.bar(yerr=grouped_stds[column], capsize=4, ax=axs[i])  # Generate a bar plot with error bars
        axs[i].set_title(column)
        axs[i].set_ylabel('Average Value')
        axs[i].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

    # Remove unused subplots
    for j in range(i+1, num_rows*num_cols):
        fig.delaxes(axs[j])

    plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding

    # Save the figure to a PNG file with 300 DPI
    plt.savefig("VS_STATS.png", dpi=300)
    print('- VS_STATS.png saved with 300 DPI')


    # Set the DPI for saving via the GUI to 300
    plt.rcParams['savefig.dpi'] = 300
    print('- You can change the plot using the GUI and export it the way you want')
    print('OBS: Error bars represents the standard deviation')
    print('')
    print(' Be happy :) ')

    # Show the plot
    plt.show()

# Specify the columns to plot
columns_to_plot = ['HypAverage', 'RootAverage', 'Comprimento Medio', 'Vigor', 'Crescimento', 'Uniformidade']

# Call the Plot_STATS function
Plot_STATS(combined_data_4, columns_to_plot, output_filename)