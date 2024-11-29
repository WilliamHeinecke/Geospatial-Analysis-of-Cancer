import "./App.css";
import MapComponent from "./components/MapComponent";
import Grid from "@mui/material/Grid2";
import NaiveBayesModel from "./components/NaiveBayesModel.js";
function App() {
  return (
    <Grid
      container
      className="App"
      sx={{ height: "100vh", width: "100vw", justifyContent: "center" }}
    >
      <Grid
        item
        sx={{ backgroundColor: "#282c34", width: "auto", height: "auto" }}
      >
        <MapComponent />
      </Grid>
      <Grid>
        <NaiveBayesModel />
      </Grid>
    </Grid>
  );
}

export default App;
