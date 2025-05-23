import React, { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import TestKickUploader from "./TestKickUploader";

export default function Dashboard() {
  const { logout } = useContext(AuthContext);

  return (
    <div className="p-6 text-white">
      <TestKickUploader />
      <h1 className="text-3xl font-bold mb-4">You're logged in!</h1>
      <button
        onClick={logout}
        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 mb-6"
      >
        Logout
      </button>

      
    </div>
    
  );
}