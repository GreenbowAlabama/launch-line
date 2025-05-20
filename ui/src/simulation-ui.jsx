import React, { useEffect, useState } from "react";

const SimulationUI = () => {
  const [kickData, setKickData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const poll = () => {
      fetch("http://localhost:5050/kick")
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "waiting") {
            setTimeout(poll, 1000); // Keep polling
          } else {
            setKickData(data);
            setError(null);
          }
        })
        .catch((err) => {
          console.error("Failed to fetch kick data", err);
          setError("Error: Failed to fetch kick data");
          setTimeout(poll, 3000); // Retry after 3s
        });
    };

    poll(); // start polling
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", color: "#fff", background: "#111", minHeight: "100vh" }}>
      <h1>Soccer Launch Monitor</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!kickData && <p>Loading kick data...</p>}
      {kickData && (
        <>
          <p><strong>Speed:</strong> {kickData.speed_mph.toFixed(1)} MPH</p>
          <p><strong>Result:</strong> {kickData.result}</p>
          <p><strong>Frame:</strong> {kickData.frame}</p>
        </>
      )}
    </div>
  );
};

export default SimulationUI;