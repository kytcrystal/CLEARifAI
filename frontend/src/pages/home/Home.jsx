import { useState } from "react";
import ClearModel from "./ClearModel";
import { Box, Button } from '@mui/material';
import "../../App.css";

function Home() {
  const [jobId, setJobId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [clearValues, setClearValues] = useState(null);
  const imagePath = `${import.meta.env.BASE_URL}CLEARifAI-Poster.png`;
  const posterPath = `${import.meta.env.BASE_URL}CLEARifAI-Poster.pdf`;


  return (
    <>
      <ClearModel />
      <Box my={4}>
        <img
          src={imagePath}
          alt="Poster preview"
          style={{ maxWidth: '100%', borderRadius: '8px' }}
        />
      </Box>

      <Button
        variant="contained"
        component="a"
        href={posterPath}
        download="CLEARifAI-Poster.pdf"
        sx={{ backgroundColor: "#2a2a5e", color: "white", '&:hover': { backgroundColor: "#000" } }}
      >
        Download PDF
      </Button>
    </>
  );
}

export default Home;
