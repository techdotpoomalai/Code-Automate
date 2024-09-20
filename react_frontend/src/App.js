import './App.css';

import {BrowserRouter, Routes, Route } from "react-router-dom";


import Navbar from './Component/Navbar.js';
import Menu from './Component/Menu.js';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar/>
        <Routes>
          <Route path="/menu" element={ <Menu/> } />
        </Routes>
      </BrowserRouter>
      
    </div>
  );
}

export default App;
