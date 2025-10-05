import logo from './logo.svg';
import builtLogo from './built-logo.png';
import './App.css';
import ChatRunner from "./components/components";

// added for dropdown menu
import React, { useEffect, useState } from "react";
import Papa from "papaparse";

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

      <div className="content-wrapper"> 
        <div id="box1">
          <p>
            This website is a tool for urban planners that leverages data to provide 
            appropriate initiatives in the city of Chicago. Our considerations include, 
            but are not limited to, population density, pollution, and available green spaces.
          </p>
        </div>

        <div id="map">
          <img src="chi-map.png" alt="Chicago Map" width="766" height="458" />
        </div>
      </div>

      <div className="greenytro">
        <div id="box2">
          <p>
            As you use our urban planning tool we also have our personal assitant Greeny at your disposal!
          </p>
          <ChatRunner />
        </div>
        <div className="greeny-logo-container"></div>
        <img src="rgreeny.png" alt="greeny" width="300" height="300" />
      </div>

      <div className="Gen_Dashboard">
        <div id="banner">
          <p>Chicago Dashboard</p>
        </div>
        <div id="mini banner">
          <p>
            The following dashboard provides visualizations based on data from the general Chicago Land area!
          </p>
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

      <div id="map">
        <img src="chi-map.png" alt="Chicago Map" width="766" height="458" />
      </div>

      <div id="greeny-bot">
        <img src="rgreeny.png" alt="greeny" width="150" height="150"/>
      </div>

    </div>
  );
}

export default App;