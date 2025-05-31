import React, { useState } from "react";
import { Container, Typography, Link } from "@mui/material";

function Mockup() {
  return (
    <>
      <Container
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
        <h2>Team Communication Evaluation</h2>
        <Container sx={{ mt: 4, mb: 4 }}>
          <Typography variant="body1" gutterBottom>
            This is a mockup. To try out the actual evaluation, you can:
          </Typography>
          <ul>
            <li>
              <Typography variant="body2">
                Look for me at XP 2025 Conference
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                <Link href="mailto:mailto:yatingcrystal.kwok@student.unibz.it">
                  Email me
                </Link>
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                Set it up based on{" "}
                <Link
                  href="https://github.com/kytcrystal/CLEARifAI"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  this repository
                </Link>
              </Typography>
            </li>
          </ul>
        </Container>
      </Container>
    </>
  );
}
export default Mockup;
