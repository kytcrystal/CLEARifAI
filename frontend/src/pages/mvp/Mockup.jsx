import React from "react";
import { Box, Typography, Link, Stack, Paper } from "@mui/material";

function Mockup() {
  return (
    <Box
      component={Paper}
      elevation={3}
      sx={{
        borderRadius: 2,
        p: { xs: 2, md: 4 },
        mt: 4,
        maxWidth: "900px",
        mx: "auto",
        backgroundColor: "#f9f9f9",
      }}
    >
      <Typography variant="h5" gutterBottom>
        Team Communication Evaluation
      </Typography>

      <Typography variant="body1" sx={{ mb: 2 }}>
        This is a mockup. To try out the actual evaluation, you can:
      </Typography>

      <Stack spacing={1} component="ul" sx={{ pl: 3 }}>
        <li>
          <Typography variant="body2">
            Look for me at XP 2025 Conference
          </Typography>
        </li>
        <li>
          <Typography variant="body2">
            <Link href="mailto:yatingcrystal.kwok@student.unibz.it">
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
      </Stack>
    </Box>
  );
}

export default Mockup;
