import logo from './logo.svg';
import builtLogo from './built-logo.png';
import './App.css';
import ChatRunner from "./components/components";
function App() {
  return (
    <div className="App" backgroundColor="rgb(102,152,101)">
      <div id="head"> <p id="head-text">B[U]ILT X Urban Planning Initiative</p></div>

      <div id="box">
        <p>This website is a tool for urban planners that leverages data to provide appropriatte initiatives in the city of Chicago</p>
        
        <ChatRunner />
      </div>

      <a href="https://built-illinois.org/#/Home">
        <img id="built" src={builtLogo} alt="Built Logo" />
      </a>
      
    </div>

 
    
  );
}

export default App;
