import { useState, useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";

export default function TestKickUploader() {
  const { token } = useContext(AuthContext);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  if (!token) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setStatus("Uploading...");

    try {
      const formData = new FormData();
      formData.append("video", file);

      const res = await fetch(`${import.meta.env.VITE_API_URL}/simulate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setResult(data);
      setStatus("Simulation successful!");
    } catch (err) {
      console.error(err);
      setStatus("Failed to process video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-6 p-4 bg-gray-800 rounded shadow">
      <h2 className="text-xl font-semibold mb-3 text-white">Upload a Test Kick Video</h2>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="block mb-3 text-white"
      />

      <button
        type="submit"
        disabled={loading || !file}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Processing..." : "Upload & Simulate"}
      </button>

      {status && <p className="mt-2 text-white">{status}</p>}

      {result && (
        <div className="mt-4 p-3 bg-black text-white rounded">
          <p><strong>Speed:</strong> {result.speed_mph} mph</p>
          <p><strong>Result:</strong> {result.result_text}</p>
        </div>
      )}
    </form>
  );
}