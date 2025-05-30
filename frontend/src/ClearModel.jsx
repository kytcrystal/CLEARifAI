import React from "react";
import "./ClearModel.css";

export default function ClearModel() {
  return (
    <div className="container">
      <div className="column left">
        <h2 className="heading">CLEAR Model<br /><span className="sub">From Modern Agile</span></h2>
        <ul className="clear-list">
          <li><span className="letter">C</span>urious, caring and open-minded</li>
          <li><span className="letter">L</span>isten to one another</li>
          <li><span className="letter">E</span>ncourage everyone to contribute</li>
          <li><span className="letter">A</span>void dominating or interrupting</li>
          <li><span className="letter">R</span>epeat and review people’s points</li>
        </ul>
      </div>

      <div className="column right">
        <h2 className="heading">AI Evaluation</h2>
        <p>Based on</p>
        <ul>
          <li>7 Psychological Safety Statements<br /><span className="note">(Developed by Amy Edmondson)</span></li>
          <li>12 Active Listening Skills<br /><span className="note">(Proposed by International Listening Association)</span></li>
        </ul>
      </div>
    </div>
  );
}
