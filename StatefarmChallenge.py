# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KT6x3aNsQS1TkAtSpnqv0n0ZS5cpA5zX
"""



import pandas as pd
from sodapy import Socrata
import tkinter as tk
from tkinter import ttk
import torch


client = Socrata("www.dallasopendata.com", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.dallasopendata.com,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("v3uv-ukdv", limit=4000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

results_df

filtered_df = results_df[results_df['victimtype'].str.contains('Business', case=False, na = False)]

unique_elements = filtered_df['zip_code'].value_counts()
type(unique_elements)
#zipcode_df = unique_elements.to_frame()

#zipcode_df = zipcode_df.rename(columns={'index': 'zipcode', 'zip_code': 'frequency'})
zipcode_df = unique_elements.reset_index()
zipcode_df.columns = ['zipcode', 'frequency']


def get_most_common_crime():
    zip_code = entry.get()
    most_common_crime = filtered_df[filtered_df['zip_code'] == zip_code]['offincident'].value_counts().idxmax()
    condition = (zipcode_df['zipcode'] == zip_code)
    result = zipcode_df.loc[condition, 'frequency'].values[0]
    if result/1019 > 0.1:
      result_label.configure(text=f"{zip_code} has been flagged as a high-risk area for theft. Following Statefarm's guidelines for business protection can reduce upto 15% on premium rates.")
    else:
      result_label.configure(text=f"Enjoy low premium rates with StateFarm's small business insurance. Like a good neighbour, StateFarm is there !")
    


# Create main application window
root = tk.Tk()
root.title("Crime Analysis Application")

# Create and place label and entry for zip code
label = ttk.Label(root, text="Enter Zip Code:")
label.pack(pady=10)
entry = ttk.Entry(root)
entry.pack(pady=10)


#most_common_crime = filtered_df[filtered_df['zip_code'] == x_value]['offincident'].value_counts().idxmax()


# Create button to trigger crime analysis
button = ttk.Button(root, text="Get Most Common Crime", command=get_most_common_crime)
button.pack(pady=10)

# Create label to display result
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

# Start the application event loop
root.mainloop()