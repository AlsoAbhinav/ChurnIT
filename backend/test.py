import pandas as pd

df = pd.read_csv("dataset.csv")
unique_contract_values = df["Contract"].unique().tolist()
print(f"Unique Contract values: {unique_contract_values}")
