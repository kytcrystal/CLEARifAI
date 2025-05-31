import { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import RadarChart from "./RadarChart";
import "../../App.css";
import Mockup from "./MockUp";

function MVP() {
  const [jobId, setJobId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [clearValues, setClearValues] = useState(null);
  const [isMock, setIsMock] = useState(false);

  useEffect(() => {
    const forceMock = false; // <-- toggle this flag for testing
    const isGitHubPages =
      window.location.hostname.includes("github.io") || forceMock;
    setIsMock(isGitHubPages);

    if (isGitHubPages) {
      setClearValues({
        C: 0.2,
        L: 0.1,
        E: 0.0,
        A: 0.3,
        R: 0.0,
      });
    }
  }, []);

  return (
    <>
      {isMock ? (
        <>
          <Mockup />
          <RadarChart
            values={{
              C: 0.8,
              L: 0.7,
              E: 0.75,
              A: 0.6,
              R: 0.9,
            }}
          />
        </>
      ) : (
        <>
          <UploadForm
            setUploading={setUploading}
            onUploadComplete={(id) => setJobId(id)}
            onClearValuesReady={(values) => setClearValues(values)}
          />
          {uploading && <p>Uploading video... please wait ⏳</p>}
          {clearValues && <RadarChart values={clearValues} />}
        </>
      )}
    </>
  );
}

export default MVP;
