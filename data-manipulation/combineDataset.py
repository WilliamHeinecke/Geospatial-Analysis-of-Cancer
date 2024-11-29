import pandas as pd

# Load the cancer incidence dataset
cancer_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/cancer_incidence/liver cancer/livercancer_inc_per100k_pop_2015_2019.csv")
print(cancer_data.head())
# Load the factor dataset
binge_drinking_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/binge_drinking_alcohol_adults_per100k_pop_2018_2019.csv")
print(binge_drinking_data.head())

coronary_disease_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/coronary_heart_disease_per100k_pop_2018_2019.csv")
print(coronary_disease_data.head())

diabetes_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/diabetes_adults_per100k_pop_2018_2019.csv")
print(diabetes_data.head())

# Preprocess the cancer incidence dataset
# Ensure CountyFIPS is a 5-digit string
cancer_data["CountyFIPS"] = cancer_data["CountyFIPS"].astype(str).str.zfill(5)

# Preprocess the factor dataset
# Ensure CountyFIPS is a 5-digit string
binge_drinking_data["CountyFIPS"] = binge_drinking_data["CountyFIPS"].astype(str).str.zfill(5)
coronary_disease_data["CountyFIPS"] = coronary_disease_data["CountyFIPS"].astype(str).str.zfill(5)
diabetes_data["CountyFIPS"] = diabetes_data["CountyFIPS"].astype(str).str.zfill(5)
# Aggregate the factor dataset by CountyFIPS (if multiple years are present)
# Example: Average the "Value" column across years


binge_drinking_data_agg = binge_drinking_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
coronary_disease_data_agg = coronary_disease_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
diabetes_data_agg = diabetes_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()


binge_drinking_data_agg.rename(columns={"Value": "BingeDrinking"}, inplace=True)
print(coronary_disease_data.head())
coronary_disease_data_agg.rename(columns={"Value": "CoronaryHeartDisease"}, inplace=True)
print(coronary_disease_data_agg.head())
diabetes_data_agg.rename(columns={"Value": "Diabetes"}, inplace=True)
print(diabetes_data_agg.head())

cancer_data.rename(columns={"Value": "CancerIncidence"}, inplace=True)
# Merge the datasets on StateFIPS and CountyFIPS
combined_data = pd.merge(
    cancer_data,
    binge_drinking_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    coronary_disease_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    diabetes_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
# Rename columns for clarity
#combined_data.rename(columns={"Value": "Factor Value"}, inplace=True)

# Save the combined dataset
combined_data.to_csv("combined_dataset.csv", index=False)

# Preview the combined dataset
print(combined_data.head())
