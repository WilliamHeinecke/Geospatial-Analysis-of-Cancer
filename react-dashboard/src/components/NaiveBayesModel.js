import React, { useState } from "react";
import axios from "axios";

const NaiveBayesModel = ({ selectedTab }) => {
  const [inputs, setInputs] = useState({
    Factor1: "1",
    Factor2: "1",
    Factor3: "1",
  });
  const [prediction, setPrediction] = useState(null);
  const [probability, setProbability] = useState(null);
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs({ ...inputs, [name]: value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validate input values
    if (
      isNaN(parseFloat(inputs.Factor1)) ||
      isNaN(parseFloat(inputs.Factor2)) ||
      isNaN(parseFloat(inputs.Factor3))
    ) {
      console.error("Invalid input: Please enter valid numeric values");
      return;
    }
    try {
      let response = null;
      if (selectedTab === "liver") {
        response = await axios.post("http://127.0.0.1:8000/predict", {
          //AirQuality: parseFloat(inputs.Factor1),
          BelowPoverty: parseFloat(inputs.Factor2),
          Diabetes: parseFloat(inputs.Factor3),
        });
      } else if (selectedTab === "lung") {
        response = await axios.post("http://127.0.0.1:8000/lung/predict", {
          Smoking: parseFloat(inputs.Factor1),
          Asthma: parseFloat(inputs.Factor2),
          Obesity: parseFloat(inputs.Factor3),
        });
      }
      console.log("Prediction Response:", response.data);
      setPrediction(response.data.prediction || "N/A");
      setProbability(response.data.probability || 0);
    } catch (error) {
      console.error("Error predicting:", error);
    }
  };
  return (
    <div>
      <h2>Linear Regression Cancer Prediction</h2>
      <form onSubmit={handleSubmit}>
        {selectedTab === "lung" ? (
          <div>
            <label>
              {selectedTab === "liver"
                ? "Air Quality (pm 2.5 average):"
                : "Smoking:"}
            </label>
            <input
              type="number"
              name="Factor1"
              //value={inputs.Factor1}
              onChange={handleInputChange}
            />
          </div>
        ) : (
          <></>
        )}
        <div>
          <label>
            {selectedTab === "liver" ? "Below Poverty Percentage:" : "Asthma"}
          </label>
          <input
            type="number"
            name="Factor2"
            //value={inputs.Factor2}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>{selectedTab === "liver" ? "Diabetes:" : "Obesity"}</label>
          <input
            type="number"
            name="Factor3"
            //value={inputs.Factor3}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit">Predict</button>
      </form>
      {prediction !== null && !isNaN(probability) && (
        <div>
          <h3>Prediction: {prediction}</h3>
        </div>
      )}
    </div>
  );
};
export default NaiveBayesModel;
