import logo from './logo.svg';
import builtLogo from './built-logo.png';
import './App.css';
import ChatRunner from "./components/components";
function App() {
  return (
    <div className="App" backgroundColor="rgb(0,91,77)">
      <div id="head"> <p id="head-text">B[U]ILT X Urban Planning Initiative</p>
      <a href="https://built-illinois.org/#/Home">
        <img id="built" src={builtLogo} alt="Built Logo" />
      </a>
      </div>
    

    <div className="content-wrapper"> 
    
   
        <div id="box1">
         <p>This website is a tool for urban planners that leverages data to provide appropriate initiatives in the city of Chicago. Our considerations include, but are not limited to, population density, pollution, and available green spaces.</p>
        </div>
 
        <div id="map">
         <img src="chi-map.png" alt="Chicago Map" width="766" height="458" />
        </div>

    </div>

  

      <div className= "greenytro">
        <div id="box2">
          <p> As you use our urban planning tool we also have our personal assitant Greeny at your disposal!  </p>
           <ChatRunner />
        </div>
        <div className="greeny-logo-container"></div>
         <img src="rgreeny.png" alt="greeny" width="300" height="300"></img>
        </div>
     

     <div className= "Gen_Dashboard">
      <div id= "banner">
        <p> Chicago Dashboard</p>
      </div>
      <div id = "mini banner">
        <p> The following dashboard provides visualizations based on data from the general Chicago Land area!</p>
      </div>
     </div>

    </div>

    
  );
}

export default App;
