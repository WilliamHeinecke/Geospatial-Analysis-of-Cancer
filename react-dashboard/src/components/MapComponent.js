import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import axios from "axios";

const ChoroplethMap = () => {
  const [data, setData] = useState([]);
  const [geoJson, setGeoJson] = useState(null);

  useEffect(() => {
    // Fetch cancer data JSON from the public/data folder
    axios
      .get("/data/livercancer_inc_per_100k_pop_2015_2019.json")
      .then((response) => {
        const processedData = response.data.map((item) => ({
          ...item,
          CountyFIPS: item.CountyFIPS.toString().padStart(5, "0"), // Convert FIPS to 5-digit string
          Value: parseFloat(item.Value), // Ensure Value is a number
        }));
        setData(processedData);
      })
      .catch((error) => console.error("Error loading cancer data:", error));

    // Fetch GeoJSON file (local or external)
    axios
      .get(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
      )
      .then((response) => setGeoJson(response.data))
      .catch((error) => console.error("Error loading GeoJSON:", error));
  }, []);

  if (!data.length || !geoJson) {
    return <div>Loading...</div>;
  }

  const fipsCodes = data.map((item) => item.CountyFIPS);
  const values = data.map((item) => item.Value);

  return (
    <div>
      <h1 style={{ margin: "0", color: "white" }}>
        Geospatial Analysis Dashboard: Cancer Incidence
      </h1>
      <Plot
        data={[
          {
            type: "choroplethmapbox",
            geojson: geoJson,
            locations: fipsCodes,
            z: values,
            colorscale: "Viridis",
            colorbar: {
              title: "Cancer Incidence",
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
          title: "Cancer Incidence by County",
        }}
      />
    </div>
  );
};

export default ChoroplethMap;
