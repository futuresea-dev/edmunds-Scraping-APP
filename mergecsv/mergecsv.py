import pandas as pd

df1=pd.read_csv("output.csv")
df2=pd.read_csv("output2.csv")

full_df = pd.concat([df1,df2])
unique_df = full_df.drop_duplicates(subset=['vehicle_year',	'vehicle_make',	'vehicle_model', 'vehicle_style','total_tax_credit',	'total_insurance',	'total_maintenance',	'total_repairs',	'total_taxs_fees',	'total_financing',	'total_depreciation',	'total_fuel',	'total_total'])

unique_df.to_csv("final_drop.csv",index=False)