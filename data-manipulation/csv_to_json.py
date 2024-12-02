import pandas as pd
import json

# Function to convert CSV to JSON
def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a dictionary
    data = df.to_dict(orient="records")

    # Write the dictionary to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"CSV file successfully converted to JSON and saved at {json_file_path}")

# Example usage
csv_file_path = "combined_dataset.csv"  # Replace with your CSV file path
json_file_path = "combined_data.json"  # Replace with your desired JSON output file path
csv_to_json(csv_file_path, json_file_path)
