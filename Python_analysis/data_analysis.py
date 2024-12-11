import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error, mean_absolute_error

# format pandas dataframes
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 240)


class data_analysis:
    def __init__(self, file):
        self.data = pd.read_csv(file)

        self.data.rename(columns={
            "American Indian/Alaskan Native (includes Hispanic)": "American Indian/Alaskan Native",
            "Asian/Pacific Islander (includes Hispanic)": "Asian/Pacific Islander",
            "Black (includes Hispanic)": "Black",
            "White (includes Hispanic)": "White"
        }, inplace=True)

    # make a correlation matrix for the data file
    def correlation_matrix(self):
        relevant_cols = ["BingeDrinking", "CoronaryHeartDisease",
                     "Diabetes", "Asthma", "Obesity", "BelowPoverty", "Smoking",
                     "Female", "Male", "American Indian/Alaskan Native",
                     "Asian/Pacific Islander", "Black", "White"]

        if "LiverCancerIncidence" in self.data.columns:
            relevant_cols.append("LiverCancerIncidence")
            cancer_type = "Liver"
        else:
            relevant_cols.append("LungCancerIncidence")
            cancer_type = "Lung"

        correlation_matrix = self.data[relevant_cols].corr()
        print(correlation_matrix)
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title(f"Correlation Heatmap of Factors and {cancer_type} Cancer Rates")
        plt.tight_layout()
        plt.show()

    # determines which factors are most important for predicting male and female cancer with random forest
    def important_predictors(self):
        predictor_list = ["BingeDrinking", "CoronaryHeartDisease", "Diabetes", "Asthma", "Obesity", "BelowPoverty", "Smoking"]

        reduced_data = self.data[predictor_list + ["Male", "Female"]]
        reduced_data = reduced_data.dropna()

        self.important_preds_helper(reduced_data, predictor_list, "Male")
        self.important_preds_helper(reduced_data, predictor_list, "Female")
        plt.show()

    # called in important_predictors make separate random forest models for male and female cancer rates
    def important_preds_helper(self, reduced_data, predictor_list, gender):
        y = reduced_data[gender]
        x_train, x_test, y_train, y_test = train_test_split(reduced_data[predictor_list], y, test_size=0.2,
                                                                random_state=1)
        # make and fit models
        rf_model = RandomForestRegressor(n_estimators=100, random_state=1)
        rf_model.fit(x_train, y_train)

        # Predict on test data
        y_pred = rf_model.predict(x_test)

        # Evaluate performance
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"EVALUATION ON {gender} MODEL")
        print(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}")
        print(f"MAPE: {mape}%")
        print(f"RMSE: {rmse}")
        print(f"MAE {mae}")

        # get feature importance
        feature_importances = pd.DataFrame({
            "Feature": x_train.columns,
            "Importance": rf_model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        # plot the importance of features used to predict cancer rate
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importances["Feature"], feature_importances["Importance"])
        plt.gca().invert_yaxis()  # Highest importance at the top
        if "LiverCancerIncidence" in self.data.columns:
            plt.title(f"Feature Importances for {gender} Liver Cancer Rates")
        else:
            plt.title(f"Feature Importances for {gender} Lung Cancer Rates")
        plt.xlabel("Importance")
        plt.ylabel("Features")


Liver = data_analysis("Liver_race_gender_dataset.csv")
Lung = data_analysis("Lung_race_gender_dataset.csv")

Liver.correlation_matrix()
Lung.correlation_matrix()

Liver.important_predictors()
Lung.important_predictors()
