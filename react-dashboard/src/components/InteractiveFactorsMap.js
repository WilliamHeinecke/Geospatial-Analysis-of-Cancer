import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import { FormControl, MenuItem, Select, Box, Typography } from "@mui/material";

const InteractiveCountyMap = () => {
  const [geoJsonData, setGeoJsonData] = useState(null); // GeoJSON of counties
  const [overlayData, setOverlayData] = useState([]); // Data for overlay
  const [selectedFactor, setSelectedFactor] = useState("Smoking"); // Default factor
  const [availableFactors] = useState([
    "Smoking",
    "Obesity",
    "AirQuality",
    "BingeDrinking",
  ]);

  // Fetch GeoJSON data for counties
  useEffect(() => {
    const fetchGeoJson = async () => {
      const response = await axios.get(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
      );
      setGeoJsonData(response.data);
    };

    fetchGeoJson();
  }, []);

  // Fetch overlay data for the selected factor
  useEffect(() => {
    const fetchOverlayData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/overlay-data", {
          params: { factor: selectedFactor },
        });
        setOverlayData(response.data.data);
      } catch (error) {
        console.error("Error fetching overlay data:", error);
      }
    };

    fetchOverlayData();
  }, [selectedFactor]);

  const handleFactorChange = (event) => {
    setSelectedFactor(event.target.value);
  };

  // Match overlay data to GeoJSON by countyFIPS
  const onEachFeature = (feature, layer) => {
    const countyFIPS = feature.id; // FIPS code from GeoJSON
    const countyData = overlayData.find(
      (item) => item.countyFIPS === countyFIPS
    );

    // Add tooltip with factor value
    layer.bindTooltip(
      countyData
        ? `${countyData.County}, ${countyData.State}: ${countyData[selectedFactor]}`
        : "No data available",
      { sticky: true }
    );

    // Style counties dynamically
    layer.setStyle({
      fillColor: countyData ? getColor(countyData[selectedFactor]) : "#ccc",
      fillOpacity: 0.7,
      color: "#000",
      weight: 0.5,
    });
  };

  // Define color scale
  const getColor = (value) => {
    if (!value) return "#ccc";
    if (value > 30) return "#800026";
    if (value > 20) return "#BD0026";
    if (value > 10) return "#E31A1C";
    if (value > 5) return "#FD8D3C";
    return "#FFEDA0";
  };

  return (
    <div>
      <Box sx={{ marginBottom: "20px", textAlign: "center" }}>
        <Typography variant="h6">Select Factor to Overlay</Typography>
        <FormControl>
          <Select
            value={selectedFactor}
            onChange={handleFactorChange}
            sx={{ backgroundColor: "white", color: "black", minWidth: "150px" }}
          >
            {availableFactors.map((factor) => (
              <MenuItem key={factor} value={factor}>
                {factor}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <MapContainer
        style={{ height: "450px", width: "700px" }}
        center={[37.8, -96]} // Center of the US
        zoom={4}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {geoJsonData && (
          <GeoJSON data={geoJsonData} onEachFeature={onEachFeature} />
        )}
      </MapContainer>
    </div>
  );
};

export default InteractiveCountyMap;
