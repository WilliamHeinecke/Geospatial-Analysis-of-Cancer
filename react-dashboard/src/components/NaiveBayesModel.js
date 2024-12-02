import React, { useState } from "react";
import axios from "axios";

const NaiveBayesModel = () => {
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
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        AirQuality: parseFloat(inputs.Factor1),
        BelowPoverty: parseFloat(inputs.Factor2),
        Diabetes: parseFloat(inputs.Factor3),
      });
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
        <div>
          <label>Air Quality (pm 2.5 average):</label>
          <input
            type="number"
            name="Factor1"
            //value={inputs.Factor1}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Below Poverty Percentage:</label>
          <input
            type="number"
            name="Factor2"
            //value={inputs.Factor2}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Diabetes:</label>
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
