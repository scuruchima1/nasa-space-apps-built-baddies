import logo from './logo.svg';
import builtLogo from './built-logo.png';
import './App.css';
import ChatRunner from "./components/components";

// added for dropdown menu
import React, { useEffect, useState, useRef} from "react";
import Papa from "papaparse";


// this detects the clicks on the circle or not
function GreenyCircle() {
  const [showBox, setShowBox] = useState(false);
  const popupRef = useRef(null);
  const circleRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target) &&
        circleRef.current &&
        !circleRef.current.contains(event.target)
      ) {
        setShowBox(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div>
      <div
        id="greeny-bot"
        className="circle"
        ref={circleRef}
        onClick={() => setShowBox(!showBox)}
      >
        <img src="rgreeny.png" alt="greeny" width="150" height="150" />
      </div>

      {showBox && (
        <div
          ref={popupRef}
          id="popup-box"
          style={{
            position: "fixed",
            bottom: "20px",
            right: "190px",
            width: "300px",
            padding: "20px",
            backgroundColor: "rgb(223,243,152)",
            border: "3px solid black",
            borderRadius: "10px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.2)",
          }}
        >
          <p>Hello! I’m Greeny. How can I help you today?</p>
          <label for="name"></label>
        <input type="text" id="name" name="name" placeholder="Enter text here!" size="45"></input>
        </div>
      )}
    </div>
  );
}



function App() {
  const [dropdownOptions, setDropdownOptions] = useState([]);

  useEffect(() => {
    // Load and parse CSV
    Papa.parse("Boundaries_-_Community_Areas_20251005.csv", {
      download: true,
      header: true,
      complete: function(results) {
        // Assuming column name is "GEOG"
        const neighborhoods = results.data
          .map(row => row.COMMUNITY)
          .filter(Boolean);
        const uniqueNeighborhoods = [...new Set(neighborhoods)];
        setDropdownOptions(uniqueNeighborhoods);
      }
    });
  }, []);  

  return (
    <div className="App" backgroundColor="rgb(0,91,77)">

      <div id="head">
        <p id="head-text">B[U]ILT X Urban Planning Initiative</p>
        <a href="https://built-illinois.org/#/Home">
          <img id="built" src={builtLogo} alt="Built Logo" />
        </a>
      </div>

      <section className="content-wrapper">
        <div className="stacked-text-container">

          <div className="intro-textbox box-one">
            <p>
              This website is a tool for urban planners that leverages data to provide appropriate initiatives in the city of Chicago.
            </p>
          </div>

          {/* Text Box 2: (Bottom Box) */}
          <div className="intro-textbox box-two">
            <p>
            Our analysis focuses on key factors including population density, pollution levels, and income. While we encorage furthur research with our tool,  it is critical that researchers acknowledge that  association does not imply causation, all data should be approached with necessary historical and social considerations to ensure responsible and actionable insights.
            </p>
          </div>

        </div>

        <div className="map">
          <img src="chi-map.png" alt="Chicago Map" width="766" height="458" />
        </div>

      </section>

      <div className="greenytro">
        <img src="animated_city.png" width="500" height="500" />
        <div id="box2">
          <p>
            As you use our urban planning tool we also have our personal assitant Greeny at your disposal!
          </p>
          <ChatRunner />
        </div>
        <div className="greeny-logo-container"></div>
        <img src="rgreeny.png" alt="greeny" width="300" height="300" />
      </div>

      <div id="Dashboard_header">
        <p>Data Dashboards</p>
      </div>

      <div className="Gen_Dashboard">
        <div id="mini_banner">
          <p>
            The following dashboard provides visualizations based on data from the general Chicago Land area and your neighborhood of choice!
          </p>
        </div>
        <div id="banner">
          <p>Chicago Dashboard</p>
        </div>
      </div>

      <div id="dropdown-container">
        <label htmlFor="neighborhood-select" style={{ color: "white" }}>
          Select a Neighborhood:
        </label>
        <select id="neighborhood-select">
          <option value="">--Choose an option--</option>
          {dropdownOptions.map((option, index) => (
            <option key={index} value={option}>{option}</option>
          ))}
        </select>
      </div>

      <GreenyCircle />
    </div>
  );
}

export default App;