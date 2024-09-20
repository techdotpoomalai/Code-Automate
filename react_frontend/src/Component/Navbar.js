import React, { useState } from 'react';
import './css/NavbarStyle.css';  // We'll define styles in this file
import { Link } from "react-router-dom";

function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    const toggleNavbar = () => {
        setIsOpen(!isOpen);
    };

    return (
        <nav className="navbar">
            <div className={`navbar-links ${isOpen ? 'open' : ''}`}>
                <Link to="/menu">Home</Link>
            </div>

            <div className="navbar-logo">
                <h2>SPT</h2>
            </div>
        </nav>
    );
}

export default Navbar;
