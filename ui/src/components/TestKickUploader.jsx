import { useState, useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";

export default function TestKickUploader() {
  const { token } = useContext(AuthContext);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !token) return;

    setStatus("Uploading...");
    const formData = new FormData();
    formData.append("video", file);

    const res = await fetch(`${import.meta.env.VITE_API_URL}/simulate`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!res.ok) {
      setStatus("Failed to process video.");
      return;
    }

    const data = await res.json();
    setResult(data);
    setStatus("Success!");
  };

  if (!token) return null;

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit">Upload & Simulate</button>
      <p>{status}</p>
      {result && (
        <div>
          <p><strong>Speed:</strong> {result.speed_mph} mph</p>
          <p><strong>Result:</strong> {result.result_text}</p>
        </div>
      )}
    </form>
  );
}