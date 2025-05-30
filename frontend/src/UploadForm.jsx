import React, { useState } from "react";

function UploadForm({ onUploadComplete, setUploading, onClearValuesReady }) {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      const jobId = data.job_id;
      console.log(jobId)

      onUploadComplete(jobId);

      const clearRes = await fetch(`/evaluate_communication/${jobId}?min_speakers=0&max_speakers=0`, {
        method: "POST",
      });
      const results = await clearRes.json();
      const text = results.evaluate_communication;
      const clearScores = retrieveScores(text)

      onClearValuesReady(clearScores);
    } catch (err) {
      console.error("Upload or CLEAR fetch error:", err);
      alert("Something went wrong. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        border: "2px solid #000",
        borderRadius: "10px",
        padding: "1.5rem",
        marginTop: "2rem",
        backgroundColor: "#f9f9f9",
        maxWidth: "900px",
        margin: "2rem auto",
        boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
      }}
    >
      <h2>Evaluate Your Team Meeting</h2>
      <p>
        Upload your team's meeting video to receive an evaluation based on the CLEAR model
      </p>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit" disabled={!file}>
        Upload Video
      </button>
    </form>
  );
}

function retrieveScores(text){
  const match = text.match(/```json\s*([\s\S]*?)\s*```/);

  let clearScores = null;

  if (match) {
    try {
      clearScores = JSON.parse(match[1]);
      console.log("Parsed CLEAR values:", clearScores);
      return clearScores
    } catch (err) {
      console.error("Failed to parse CLEAR JSON:", err);
    }
  } else {
    console.warn("No JSON block found in response");
  }
}

export default UploadForm;
