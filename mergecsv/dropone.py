import pandas as pd

subsets = ['vehicle_year',	'vehicle_make',	'vehicle_model', 'vehicle_style','total_tax_credit',	'total_insurance',	'total_maintenance',	'total_repairs',	'total_taxs_fees',	'total_financing',	'total_depreciation',	'total_fuel',	'total_total']
df1=pd.read_csv("80202_last_output.csv")


unique_df = df1.drop_duplicates(subset=subsets)

unique_df.to_csv("output_drop2.csv",index=False)