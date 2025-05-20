// ui/src/pages/LoggedInPage.jsx
import { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";

function LoggedInPage() {
  const { user } = useContext(AuthContext);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h2 className="text-2xl font-bold mb-4">Welcome!</h2>
      <p className="text-lg">You are logged in as <strong>{user?.email}</strong>.</p>
    </div>
  );
}

export default LoggedInPage;
