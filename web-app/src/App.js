import logo from './logo.svg';
import builtLogo from './built-logo.png';
import './App.css';
import ChatRunner from "./components/components";
function App() {
  return (
    <div className="App" backgroundColor="rgb(102,152,101)">
      <div id="head"> <p id="head-text">B[U]ILT X Urban Planning Initiative</p>
      <a href="https://built-illinois.org/#/Home">
        <img id="built" src={builtLogo} alt="Built Logo" />
      </a>
      </div>

    <div className="content-wrapper"> 
    
   
        <div id="box">
         <p>This website is a tool for urban planners that leverages data to provide appropriate initiatives in the city of Chicago</p>
        </div>
 
        <div id="map">
         <img src="chi-map.png" alt="Chicago Map" width="250" height="319.5" />
        </div>

    </div>

  

      <div className= "greenytro">
        <div id="box">
          <p> As you use our urban planning tool we also have our personal assitant Greeny at your disposal!  </p>
           <ChatRunner />
        </div>
        
       

      </div>


     
      
    </div>

 
    
  );
}

export default App;
