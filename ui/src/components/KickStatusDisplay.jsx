import React from "react";

function KickStatusDisplay({ result }) {
  if (!result) return null;

  const { frame, speed_mph, result: resultType } = result;

  return (
    <div className="p-4 bg-black text-white rounded-2xl shadow-xl mt-4">
      <h2 className="text-xl font-bold mb-2">Kick Result</h2>
      <p>Frame: {frame}</p>
      <p>Speed: {speed_mph.toFixed(1)} MPH</p>
      <p>Result: {resultType}</p>
    </div>
  );
}

export default KickStatusDisplay;
