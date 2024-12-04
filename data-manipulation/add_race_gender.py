import pandas as pd
import numpy as np

# format pandas dataframes
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 240)

# adds the per capita gender and race values to the cancer files
# this is done after adding the factors to these files with the code in the combineDataset python file
# creating an instance of this class should make the files
# by setting include_race to false the race columns will not be added
# by setting include_gender to False the gender columns will not be added
class add_race_gender:
    def __init__(self, include_race, include_gender):
        self.include_race = include_race
        self.include_gender = include_gender

        # load needed files for liver cancer
        self.liver_cancer_data = pd.read_csv("Liver_dataset.csv")
        self.liver_cancer_gender = pd.read_csv("geospatial_cancer_data/geospatial_cancer_data/cancer_incidence/liver cancer/livercancer_inc_per100k_pop_2015_2019_gender.csv")
        self.liver_cancer_race = pd.read_csv("geospatial_cancer_data/geospatial_cancer_data/cancer_incidence/liver cancer/livercancer_inc_per100k_pop_2015_2019_race.csv")
        print(self.liver_cancer_data.head())
        print(self.liver_cancer_gender.head())
        print(self.liver_cancer_race.head())

        # load needed files for lung cancer
        self.lung_cancer_data = pd.read_csv("Lung_dataset.csv")
        self.lung_cancer_gender = pd.read_csv("geospatial_cancer_data/geospatial_cancer_data/cancer_incidence/lung cancer/lungcancer_inc_per100k_pop_2015_2019_gender.csv")
        self.lung_cancer_race = pd.read_csv("geospatial_cancer_data/geospatial_cancer_data/cancer_incidence/lung cancer/lungcancer_inc_per100k_pop_2015_2019_race.csv")
        print(self.lung_cancer_data.head())
        print(self.lung_cancer_gender.head())
        print(self.lung_cancer_race.head())

        self.pivot_gender_race()
        self.change_types()
        self.combine_data()
        self.create_files()

        print(self.liver_cancer_data.dtypes)
        print(self.lung_cancer_data.dtypes)

    # pivots lung and liver cancer race and gender data
    def pivot_gender_race(self):
        # pivot gender to columns instead of separate records for liver cancer
        self.liver_cancer_gender = self.liver_cancer_gender.pivot(index=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                                  columns="Gender",
                                  values="Value").reset_index()
        print(self.liver_cancer_gender.head())

        # pivot race to separate columns instead of separate records for liver cancer
        self.liver_cancer_race = self.liver_cancer_race.pivot(index=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                                  columns="Race Ethnicity",
                                  values="Value").reset_index()
        print(self.liver_cancer_race.head())

        # pivot gender to columns instead of separate records for lung cancer
        self.lung_cancer_gender = self.lung_cancer_gender.pivot(index=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                                  columns="Gender",
                                  values="Value").reset_index()
        print(self.lung_cancer_gender.head())

        # pivot race to separate columns instead of separate records for lung cancer
        self.lung_cancer_race = self.lung_cancer_race.pivot(index=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                                  columns="Race Ethnicity",
                                  values="Value").reset_index()
        print(self.lung_cancer_race.head())

    # combine the lung and liver cancer data with their corresponding race and gender data
    def combine_data(self):
        # add gender data to liver cancer data
        if self.include_gender:
            self.liver_cancer_data = pd.merge(
                self.liver_cancer_data,
                self.liver_cancer_gender,
                on=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                how="inner"
            )
        # add race data to liver cancer data
        if self.include_race:
            self.liver_cancer_data = pd.merge(
                self.liver_cancer_data,
                self.liver_cancer_race,
                on=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                how="inner"
            )
        print(self.liver_cancer_data.head())

        if self.include_gender:
            # add gender data to lung cancer data
            self.lung_cancer_data = pd.merge(
                self.lung_cancer_data,
                self.lung_cancer_gender,
                on=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                how="inner"
            )
        # add race data to liver cancer data
        if self.include_race:
            self.lung_cancer_data = pd.merge(
                self.lung_cancer_data,
                self.lung_cancer_race,
                on=["StateFIPS", "State", "CountyFIPS", "County", "Start Year", "End Year"],
                how="inner"
            )
        print(self.lung_cancer_data.head())

    # changes the types in the dataframes to floats
    def change_types(self):
        # replace suppressed with NaN before converting data
        self.liver_cancer_gender.replace("Suppressed", np.nan, inplace=True)
        self.liver_cancer_race.replace("Suppressed", np.nan, inplace=True)
        self.lung_cancer_gender.replace("Suppressed", np.nan, inplace=True)
        self.lung_cancer_race.replace("Suppressed", np.nan, inplace=True)

        # change values to float in liver cancer gender
        self.liver_cancer_gender = self.liver_cancer_gender.astype({"Female": "float64", "Male": "float64"})

        # change values to float in liver cancer race
        self.liver_cancer_race = self.liver_cancer_race.astype({
            "American Indian/Alaskan Native (includes Hispanic)": "float64",
            "Asian/Pacific Islander (includes Hispanic)": "float64",
            "Black (includes Hispanic)": "float64",
            "White (includes Hispanic)": "float64"})

        # change values to float in lung cancer gender
        self.lung_cancer_gender = self.lung_cancer_gender.astype({"Female": "float64", "Male": "float64"})

        # change values to float in lung cancer race
        self.lung_cancer_race = self.lung_cancer_race.astype({
            "American Indian/Alaskan Native (includes Hispanic)": "float64",
            "Asian/Pacific Islander (includes Hispanic)": "float64",
            "Black (includes Hispanic)": "float64",
            "White (includes Hispanic)": "float64"})

    # saves the dataframes to .csv files
    def create_files(self):
        file_name = "dataset.csv"

        if self.include_gender:
            file_name = "gender_" + file_name
        if self.include_race:
            file_name = "race_" + file_name

        self.liver_cancer_data.to_csv("Liver_" + file_name, index=False)
        self.lung_cancer_data.to_csv("Lung_" + file_name, index=False)


add_race_gender(True, True)
