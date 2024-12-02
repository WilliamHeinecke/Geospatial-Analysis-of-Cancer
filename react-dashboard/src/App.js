import "./App.css";
import MapComponent from "./components/MapComponent";
import Grid from "@mui/material/Grid2";
import NaiveBayesModel from "./components/NaiveBayesModel.js";
import LiverCorrelationDisplay from "./components/LiverCorrolationDisplay.js";
import StateMapHighestLiverCancer from "./components/StateMapHighestLiverCancer.js";
import { Typography, Box } from "@mui/material";
import InteractiveFactorsMap from "./components/InteractiveFactorsMap.js";

function App() {
  return (
    <Grid
      container
      className="App"
      sx={{ justifyContent: "center", width: "100%", height: "100%" }}
    >
      <Grid
        container
        className="App"
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
            Geospatial Analysis Dashboard: Cancer Incidence
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
              <MapComponent />
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
              <StateMapHighestLiverCancer />
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
              <InteractiveFactorsMap />
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
              <LiverCorrelationDisplay />
            </Box>
          </Grid>
          {/* Naive Bayes Model */}
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
              <NaiveBayesModel />
            </Box>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}

export default App;
