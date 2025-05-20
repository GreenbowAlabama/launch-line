// ui/src/components/GoalDistanceSelector.jsx

import React from "react";

const GoalDistanceSelector = ({ distance, setDistance }) => {
  const handleChange = (e) => {
    setDistance(parseInt(e.target.value));
  };

  return (
    <div className="flex flex-col p-4 gap-2">
      <label htmlFor="goal-distance" className="text-lg font-medium">
        Goal Distance (yards):
      </label>
      <select
        id="goal-distance"
        value={distance}
        onChange={handleChange}
        className="p-2 border rounded-xl text-base"
      >
        {[5, 10, 15, 20, 25, 30].map((d) => (
          <option key={d} value={d}>
            {d} yards
          </option>
        ))}
      </select>
    </div>
  );
};

export default GoalDistanceSelector;
