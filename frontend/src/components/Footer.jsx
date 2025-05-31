import { Box, Typography, IconButton, Link } from '@mui/material';
import EmailIcon from "@mui/icons-material/Email";
import GitHubIcon from "@mui/icons-material/GitHub";

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        mt: 'auto',
        py: 10,
        px: 4,
        textAlign: 'center',
      }}
    >
      <Typography variant="body2" color="text.secondary">
        CLEARifAI {new Date().getFullYear()}
      </Typography>
      <Box sx={{ mt: 1 }}>
        <IconButton
          component="a"
          href="mailto:yatingcrystal.kwok@student.unibz.it"
          target="_blank"
          rel="noopener"
          color="inherit"
        >
          <EmailIcon />
        </IconButton>

        <IconButton
          component="a"
          href="https://github.com/kytcrystal/CLEARifAI"
          target="_blank"
          rel="noopener"
          color="inherit"
        >
          <GitHubIcon />
        </IconButton>
      </Box>
    </Box>
  );
}
