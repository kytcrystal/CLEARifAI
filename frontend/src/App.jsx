import { useState } from "react";
import Box from "@mui/material/Box";
import UploadForm from "./UploadForm";
import ClearModel from "./ClearModel";
import RadarChart from "./RadarChart";
import "./App.css";

function App() {
  const [jobId, setJobId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [clearValues, setClearValues] = useState(null);

  return (
    <>
      <h1 style={{ marginBottom: "0.25rem" }}>CLEARifAI</h1>
      <p className="sub-text">
        Effective Team Communication in Agile Team Meetings through AI
        Evaluation
      </p>
      <ClearModel />

      <UploadForm
        setUploading={setUploading}
        onUploadComplete={(id) => setJobId(id)}
        onClearValuesReady={(values) => setClearValues(values)}
      />
      {uploading && <p>Uploading video... please wait ⏳</p>}

      {clearValues && <RadarChart values={clearValues} />}
    </>
  );
}

export default App;
