import { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import RadarChart from "./RadarChart";
import "../../App.css";
import Evaluation from "./Evaluation";

function MVP() {
  const [jobId, setJobId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [clearValues, setClearValues] = useState(null);
  const [isMock, setIsMock] = useState(false);

  useEffect(() => {
    const forceMock = true; // <-- toggle this flag for testing
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
      {!isMock ? (
        <>
          {/* MOCK MODE */}
          <Evaluation />
          <p>
            This is a mockup. To try out the actual evaluation, you can look for
            me at XP 2025 Conference,{" "}
            <a href="mailto:mailto:yatingcrystal.kwok@student.unibz.it">
              email me
            </a>{" "}
            or set it up based on{" "}
            <a
              href="https://github.com/kytcrystal/CLEARifAI"
              target="_blank"
              rel="noopener noreferrer"
            >
              this repository
            </a>
          </p>
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
          {/* REAL MODE */}
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
