import "./App.css";
import MapComponent from "./components/MapComponent";
import Grid from "@mui/material/Grid2";
import NaiveBayesModel from "./components/NaiveBayesModel.js";
import LiverCorrelationDisplay from "./components/LiverCorrolationDisplay.js";
import StateMapHighestLiverCancer from "./components/StateMapHighestLiverCancer.js";
import { Typography, Box, Button } from "@mui/material";
import InteractiveFactorsMap from "./components/InteractiveFactorsMap.js";
import React, { useState } from "react";

function App() {
  const [selectedTab, setSelectedTab] = useState("liver"); // Default tab: Liver Cancer

  // Sidebar Tabs
  const cancerTabs = {
    liver: "Liver Cancer",
    lung: "Lung Cancer",
  };

  return (
    <Grid
      container
      className="App"
      sx={{ justifyContent: "space-between", width: "100%", height: "auto" }}
    >
      {/* Sidebar */}
      <Grid
        item
        xs={12}
        md={2}
        sx={{
          backgroundColor: "#333",
          color: "white",
          padding: "20px",
          minHeight: "100vh",
        }}
      >
        <Typography variant="h5" component="h2" gutterBottom>
          Cancer Dashboard
        </Typography>
        <Box sx={{ marginTop: "20px" }}>
          {Object.keys(cancerTabs).map((key) => (
            <Button
              key={key}
              variant={selectedTab === key ? "contained" : "outlined"}
              color="primary"
              onClick={() => setSelectedTab(key)}
              sx={{
                display: "block",
                width: "100%",
                textAlign: "left",
                marginBottom: "10px",
                color: "white",
                backgroundColor: selectedTab === key ? "#555" : "transparent",
                borderColor: "#777",
              }}
            >
              {cancerTabs[key]}
            </Button>
          ))}
        </Box>
      </Grid>

      {/* Main Content */}
      <Grid
        item
        xs={12}
        md={10}
        sx={{
          height: "100%",
          width: "auto",
          backgroundColor: "#282c34",
          color: "white",
          padding: "20px",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <Grid item xs={12} sx={{ textAlign: "center", marginBottom: "20px" }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Geospatial Analysis Dashboard: {cancerTabs[selectedTab]}
          </Typography>
        </Grid>

        {/* Main Section */}
        <Grid container spacing={2} sx={{ marginBottom: "20px" }}>
          {/* Left: Main Map */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                borderRadius: "8px",
                overflow: "hidden",
                height: "100%",
                backgroundColor: "#1c1e22",
                padding: "10px",
              }}
            >
              <MapComponent selectedTab={selectedTab} />
            </Box>
          </Grid>
          {/* Right: State with Highest Cancer Rate */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                borderRadius: "8px",
                overflow: "hidden",
                height: "100%",
                backgroundColor: "#1c1e22",
                padding: "10px",
              }}
            >
              <StateMapHighestLiverCancer selectedTab={selectedTab} />
            </Box>
          </Grid>
        </Grid>

        {/* Bottom Section */}
        <Grid container spacing={2} paddingTop={"10px"}>
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                borderRadius: "8px",
                overflow: "hidden",
                height: "100%",
                backgroundColor: "#1c1e22",
                padding: "10px",
              }}
            >
              <InteractiveFactorsMap selectedTab={selectedTab} />
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                borderRadius: "8px",
                overflow: "hidden",
                height: "100%",
                backgroundColor: "#1c1e22",
                padding: "10px",
              }}
            >
              <LiverCorrelationDisplay selectedTab={selectedTab} />
            </Box>
          </Grid>
          {/* Linear Regression */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                borderRadius: "8px",
                overflow: "hidden",
                height: "100%",
                backgroundColor: "#1c1e22",
                padding: "10px",
              }}
            >
              <NaiveBayesModel selectedTab={selectedTab} />
            </Box>
          </Grid>
        </Grid>
      </Grid>
      {/* other side bar */}
      <Grid
        item
        xs={12}
        md={2}
        sx={{
          backgroundColor: "inherit",
          color: "white",
          padding: "20px",
          minHeight: "100vh",
        }}
      ></Grid>
    </Grid>
  );
}

export default App;
