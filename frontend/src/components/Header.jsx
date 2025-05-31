import { Link as RouterLink } from "react-router-dom";

import {
  AppBar,
  Toolbar,
  Button,
  Slide,
  Typography,
  useScrollTrigger,
} from "@mui/material";

function HideOnScroll({ children }) {
  const trigger = useScrollTrigger();
  return (
    <Slide appear={false} direction="down" in={!trigger}>
      {children}
    </Slide>
  );
}

export default function Header() {
  return (
    <>
      <HideOnScroll>
        <AppBar
          position="fixed"
          elevation={0}
          sx={{ backgroundColor: "transparent", color: "black" }}
        >
          <Toolbar>
            <Button color="inherit" component={RouterLink} to="/">
              Home
            </Button>
            <Button color="inherit" component={RouterLink} to="/survey">
              Survey
            </Button>
            <Button color="inherit" component={RouterLink} to="/mvp">
              MVP
            </Button>
          </Toolbar>
        </AppBar>
      </HideOnScroll>
      <h1 style={{ marginBottom: "0.25rem" }}>CLEARifAI</h1>
      <Typography sx={{ fontStyle: "italic", mt: 1 }}>
        <strong>/klɪəɹ.ɪ.fʌɪ/</strong>
      </Typography>
      <p className="sub-text">
        Effective Team Communication in Agile Team Meetings through AI
        Evaluation
      </p>
    </>
  );
}
