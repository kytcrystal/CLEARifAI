import { Link } from "@mui/material";
export default function Survey() {
  const formPath = "https://docs.google.com/forms/d/e/1FAIpQLSdIFD-AdqR6ms3px0VbieMSRdLPcGVFueydwnOLXRs24scDzQ/viewform?usp=header"
  return (
    <>
      <p>
        Respond from{" "}
        <Link
          href={formPath}
          target="_blank"
          rel="noopener noreferrer"
        >
        Google Form
        </Link>{" "}
        instead
      </p>
      <div style={{ height: "100vh", width: "100%" }}>
        <iframe
          src={formPath}
          width="100%"
          height="100%"
          title="Survey"
        >
          Loading…
        </iframe>
      </div>
    </>
  );
}
