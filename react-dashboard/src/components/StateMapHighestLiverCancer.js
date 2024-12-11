import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import { Modal, Box, Typography, Button } from "@mui/material";

const StateMapHighestLiverCancer = ({ selectedTab }) => {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [highestStateData, setHighestStateData] = useState(null);
  const [modalData, setModalData] = useState(null);
  const [mapCenter, setMapCenter] = useState([37.8, -96]); // Center of the US
  const [mapZoom, setMapZoom] = useState(4);
  const [mapKey, setMapKey] = useState("liver");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch the state with the highest average cancer rate
        const stateResponse = await axios.get(
          "http://127.0.0.1:8000/" + selectedTab + "/highest-cancer-rate"
        );
        setHighestStateData(stateResponse.data);

        // Fetch GeoJSON data for US states
        const geoJsonResponse = await axios.get(
          "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
        );
        const usGeoJson = geoJsonResponse.data;

        // Highlight the state in GeoJSON data
        const updatedGeoJson = {
          ...usGeoJson,
          features: usGeoJson.features.map((feature) => {
            const isHighlighted =
              feature.properties.name ===
              stateResponse.data.state_with_highest_rate;
            return {
              ...feature,
              properties: {
                ...feature.properties,
                isHighlighted,
              },
            };
          }),
        };

        setGeoJsonData(updatedGeoJson);
        setMapKey(selectedTab);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [selectedTab]);

  const onEachFeature = (feature, layer) => {
    const { name, isHighlighted } = feature.properties;
    console.log("in each feature");
    // Bind tooltip with state name and highlight info
    layer.bindTooltip(
      `${name}${isHighlighted ? " (Highest Cancer Rate)" : ""}`,
      { sticky: true }
    );

    // Style the state
    layer.setStyle({
      color: isHighlighted ? "red" : "blue",
      weight: isHighlighted ? 3 : 1,
      fillOpacity: isHighlighted ? 0.7 : 0.4,
    });

    // Add click event for showing modal
    layer.on("click", () => {
      setModalData({
        name,
        isHighlighted,
      });

      // Dynamic zoom: Adjust map center and zoom to the clicked state
      const coordinates = feature.geometry.coordinates[0][0];
      setMapCenter([coordinates[1], coordinates[0]]);
      setMapZoom(6);
    });
  };

  if (!geoJsonData || !highestStateData) {
    return <div>Loading map...</div>;
  }

  return (
    <div
      style={{
        height: "500px",
        width: "100%",
        color: "white",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h2>State With The Highest Average {selectedTab} Cancer Rate</h2>
      <p>
        <strong>{highestStateData.state_with_highest_rate}</strong> with an
        average rate of{" "}
        <strong>{highestStateData.highest_average_rate.toFixed(2)}</strong> per
        100k, compared to an overall average rate of{" "}
        <strong>{highestStateData.overall_average_rate.toFixed(2)}</strong>.
      </p>
      <MapContainer
        style={{
          height: "400px",
          width: "400px",
          borderRadius: "50%",
          overflow: "hidden",
          alignSelf: "center",
        }}
        center={mapCenter}
        zoom={mapZoom}
        key={JSON.stringify(mapCenter)} // Ensure map resets when center changes
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <GeoJSON
          key={mapKey + "key"}
          data={geoJsonData}
          onEachFeature={onEachFeature}
        />
      </MapContainer>

      {/* Modal for displaying state details */}
      {modalData && (
        <Modal
          open={!!modalData}
          onClose={() => setModalData(null)}
          aria-labelledby="state-modal-title"
          aria-describedby="state-modal-description"
        >
          <Box
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: 300,
              bgcolor: "background.paper",
              boxShadow: 24,
              p: 4,
              borderRadius: 2,
            }}
          >
            <Typography id="state-modal-title" variant="h6" component="h2">
              {modalData.name}
            </Typography>
            <Typography id="state-modal-description" sx={{ mt: 2 }}>
              {modalData.isHighlighted
                ? `This state has the highest average cancer rate: ${highestStateData.highest_average_rate.toFixed(
                    2
                  )} per 100k.`
                : `This state does not have the highest cancer rate. The overall average is ${highestStateData.overall_average_rate.toFixed(
                    2
                  )} per 100k.`}
            </Typography>
            <Button
              onClick={() => setModalData(null)}
              variant="contained"
              sx={{ mt: 2 }}
            >
              Close
            </Button>
          </Box>
        </Modal>
      )}
    </div>
  );
};

export default StateMapHighestLiverCancer;
