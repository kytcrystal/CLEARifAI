import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import {
  Container,
} from "@mui/material";

import Home from "./pages/home/Home";
import Survey from "./pages/Survey";
import MVP from "./pages/mvp/MVP";
import Header from "./components/Header";
import Footer from "./components/Footer";

export default function App() {
  return (
    <Router>
      <Header />
      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/survey" element={<Survey />} />
          <Route path="/mvp" element={<MVP />} />
        </Routes>
      </Container>
      <Footer />
    </Router>
  );
}