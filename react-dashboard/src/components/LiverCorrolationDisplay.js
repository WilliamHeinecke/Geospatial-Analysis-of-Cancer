import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import {
  TextField,
  Container,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from "@mui/material";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const LiverCorrolationDisplay = () => {
  const [threshold, setThreshold] = useState(0.1); // Default correlation threshold
  const [correlations, setCorrelations] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch correlations from the API
  useEffect(() => {
    const fetchCorrelations = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await axios.get("http://127.0.0.1:8000/correlations", {
          params: { threshold },
        });
        setCorrelations(response.data.highly_correlated_factors);
      } catch (err) {
        setError("Failed to fetch correlations");
      } finally {
        setLoading(false);
      }
    };

    fetchCorrelations();
  }, [threshold]); // Re-fetch when threshold changes

  // Handle text input change
  const handleInputChange = (event) => {
    const value = parseFloat(event.target.value);
    if (!isNaN(value) && value >= 0.1 && value <= 1.0) {
      setThreshold(value);
    }
  };

  // Prepare data for the bar chart
  const barChartData = {
    labels: Object.keys(correlations), // Factors
    datasets: [
      {
        label: "Correlation",
        data: Object.values(correlations), // Correlation values
        backgroundColor: "rgba(75, 192, 192, 0.6)", // Light teal color
        borderColor: "rgba(75, 192, 192, 1)", // Dark teal color
        borderWidth: 1,
      },
    ],
  };

  return (
    <Container maxWidth="md" sx={{ py: 4, color: "white" }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Correlation Viewer
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Typography variant="body1" sx={{ mb: 1 }}>
          Correlation Threshold (0.1 - 1.0):
        </Typography>
        <TextField
          type="number"
          inputProps={{ step: 0.01, min: 0.1, max: 1.0 }}
          value={threshold}
          onChange={handleInputChange}
          label="Threshold"
          variant="outlined"
          size="small"
          sx={{ width: "150px", color: "white" }}
        />
      </Box>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ my: 3 }}>
          {error}
        </Alert>
      )}

      {!loading && !error && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Bar Chart of Correlations
          </Typography>
          <Bar
            data={barChartData}
            options={{
              responsive: true,
              plugins: {
                legend: { display: false },
                tooltip: { enabled: true },
              },
              scales: {
                y: {
                  beginAtZero: true,
                  title: { display: true, text: "Correlation" },
                },
                x: { title: { display: true, text: "Factors" } },
              },
            }}
          />
        </Box>
      )}
    </Container>
  );
};

export default LiverCorrolationDisplay;
