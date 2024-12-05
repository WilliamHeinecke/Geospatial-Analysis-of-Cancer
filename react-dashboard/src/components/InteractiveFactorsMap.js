import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import axios from "axios";

const InteractiveFactorsMap = () => {
  const [overlayData, setOverlayData] = useState([]);
  const [geoJson, setGeoJson] = useState(null);
  const [selectedFactor, setSelectedFactor] = useState("Diabetes"); // Default factor
  const [availableFactors] = useState([
    "Smoking",
    "Obesity",
    "BingeDrinking",
    "Diabetes",
  ]);

  // Fetch GeoJSON and overlay data
  useEffect(() => {
    // Fetch GeoJSON
    axios
      .get(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
      )
      .then((response) => setGeoJson(response.data))
      .catch((error) => console.error("Error loading GeoJSON:", error));

    // Fetch overlay data
    axios
      .get("http://127.0.0.1:8000/overlay-data", {
        params: { factor: selectedFactor },
      })
      .then((response) => {
        const processedData = response.data.data.map((item) => ({
          ...item,
          CountyFIPS: item.CountyFIPS.toString().padStart(5, "0"), // Convert FIPS to 5-digit string
          Value: parseFloat(item[selectedFactor]), // Ensure Value is a number
        }));
        setOverlayData(processedData);
      })
      .catch((error) => console.error("Error loading overlay data:", error));
  }, [selectedFactor]);

  if (!overlayData.length || !geoJson) {
    return <div>Loading...</div>;
  }

  const fipsCodes = overlayData.map((item) => item.CountyFIPS);
  const values = overlayData.map((item) => item.Value);

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <h1 style={{ margin: "10px 0", color: "white" }}>
        Geospatial Analysis Dashboard: {selectedFactor}
      </h1>
      <div style={{ marginBottom: "10px", textAlign: "center" }}>
        <label
          style={{ color: "white", fontWeight: "bold", marginRight: "10px" }}
        >
          Select Factor:
        </label>
        <select
          value={selectedFactor}
          onChange={(e) => setSelectedFactor(e.target.value)}
          style={{ padding: "5px", fontSize: "16px" }}
        >
          {availableFactors.map((factor) => (
            <option key={factor} value={factor}>
              {factor}
            </option>
          ))}
        </select>
      </div>
      <Plot
        data={[
          {
            type: "choroplethmapbox",
            geojson: geoJson,
            locations: fipsCodes,
            z: values,
            colorscale: "Viridis",
            colorbar: {
              title: selectedFactor,
              thickness: 20,
            },
          },
        ]}
        layout={{
          mapbox: {
            style: "carto-positron",
            center: { lon: -95.7129, lat: 37.0902 },
            zoom: 3,
          },
          title: `${selectedFactor} by County`,
          autosize: true,
          margin: { l: 0, r: 0, t: 30, b: 0 }, // Reduced margins
        }}
        useResizeHandler={true}
        style={{ width: "700px", height: "450px" }} // Adjust map to take up most of the available space
        config={{
          mapboxAccessToken: "your-mapbox-access-token", // Replace with your Mapbox token
        }}
      />
    </div>
  );
};

export default InteractiveFactorsMap;
