import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("data.csv")

# Delete rows where prev_input is null
df = df[df.input.notnull()]

# Save the modified DataFrame to a new CSV file
df.to_csv("data_cleaned.csv", index=False)













