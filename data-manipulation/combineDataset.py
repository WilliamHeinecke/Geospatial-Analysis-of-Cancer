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

asthma_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/county_asthma_per100k_pop_2018_2019.csv")
print(asthma_data.head())

obesity_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/obesity_adults_per100k_pop_2018_2019.csv")
print(obesity_data.head())

below_poverty_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/pop_perc_below_poverty_2018_2019.csv")
print(below_poverty_data.head())
smoking_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/smoking_adults_per100k_pop_2018_2019.csv")
print(below_poverty_data.head())
air_quality_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/air_quality_pm2.5annualavg_bycounty_2018_2019.csv")
print(air_quality_data.head())

arsenic_data = pd.read_csv("../geospatial_cancer_data/geospatial_cancer_data/Factors_2018-2019/arsenic_annual_mean_conc_2018_2019.csv")
print(arsenic_data.head())
# Preprocess the cancer incidence dataset
# Ensure CountyFIPS is a 5-digit string
cancer_data["CountyFIPS"] = cancer_data["CountyFIPS"].astype(str).str.zfill(5)

# Preprocess the factor dataset
# Ensure CountyFIPS is a 5-digit string
binge_drinking_data["CountyFIPS"] = binge_drinking_data["CountyFIPS"].astype(str).str.zfill(5)
coronary_disease_data["CountyFIPS"] = coronary_disease_data["CountyFIPS"].astype(str).str.zfill(5)
diabetes_data["CountyFIPS"] = diabetes_data["CountyFIPS"].astype(str).str.zfill(5)
asthma_data["CountyFIPS"] = asthma_data["CountyFIPS"].astype(str).str.zfill(5)
obesity_data["CountyFIPS"] = obesity_data["CountyFIPS"].astype(str).str.zfill(5)
below_poverty_data["CountyFIPS"] = below_poverty_data["CountyFIPS"].astype(str).str.zfill(5)
below_poverty_data["Value"] = pd.to_numeric(below_poverty_data["Value"], errors="coerce")
smoking_data["CountyFIPS"] = smoking_data["CountyFIPS"].astype(str).str.zfill(5)
air_quality_data["CountyFIPS"] = air_quality_data["CountyFIPS"].astype(str).str.zfill(5)
arsenic_data["CountyFIPS"] = arsenic_data["CountyFIPS"].astype(str).str.zfill(5)
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
asthma_data_agg = asthma_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
obesity_data_agg = obesity_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
below_poverty_data_agg = below_poverty_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
smoking_data_agg = smoking_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
air_quality_data_agg = air_quality_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()
arsenic_data_agg = arsenic_data.groupby(["StateFIPS", "CountyFIPS"]).agg(
    {"Value": "mean"}
).reset_index()

binge_drinking_data_agg.rename(columns={"Value": "BingeDrinking"}, inplace=True)
print(coronary_disease_data.head())
coronary_disease_data_agg.rename(columns={"Value": "CoronaryHeartDisease"}, inplace=True)
print(coronary_disease_data_agg.head())
diabetes_data_agg.rename(columns={"Value": "Diabetes"}, inplace=True)
print(diabetes_data_agg.head())
asthma_data_agg.rename(columns={"Value": "Asthma"}, inplace=True)
print(asthma_data_agg.head())
obesity_data_agg.rename(columns={"Value": "Obesity"}, inplace=True)
print(obesity_data_agg.head())
below_poverty_data_agg.rename(columns={"Value": "BelowPoverty"}, inplace=True)
print(below_poverty_data_agg.head())
smoking_data_agg.rename(columns={"Value": "Smoking"}, inplace=True)
print(smoking_data_agg.head())
air_quality_data_agg.rename(columns={"Value": "AirQuality"}, inplace=True)
print(air_quality_data_agg.head())
arsenic_data_agg.rename(columns={"Value": "ArsenicConc"}, inplace=True)
print(arsenic_data_agg.head())

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
combined_data = pd.merge(
    combined_data,
    asthma_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    obesity_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    below_poverty_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    smoking_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
combined_data = pd.merge(
    combined_data,
    air_quality_data_agg,
    on=["StateFIPS", "CountyFIPS"],
    how="inner"
)
# combined_data = pd.merge(
#     combined_data,
#     arsenic_data_agg,
#     on=["StateFIPS", "CountyFIPS"],
#     how="inner"
# )
# Rename columns for clarity
#combined_data.rename(columns={"Value": "Factor Value"}, inplace=True)
combined_data["CancerIncidence"] = pd.to_numeric(combined_data["CancerIncidence"], errors="coerce")
combined_data.dropna(subset=["CancerIncidence"], inplace=True)
# Save the combined dataset
combined_data.to_csv("combined_dataset.csv", index=False)

# Preview the combined dataset
print(combined_data.head())
