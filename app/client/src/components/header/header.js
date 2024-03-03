import React from "react";
import {useContext, useEffect, useState} from "react";
import './header.css'
import {faSearch, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';
import {BasicModal} from "./popup";
import Axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";


export const Header = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');	
    const navigate = useNavigate();
    const handleOpenModal = () => {
        setIsModalOpen(true);
      };
    
    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    
      const handleSearch = () => {
        if (searchQuery.trim() !== '') {
            navigate(`/search/?query=${searchQuery}`);
        }
    };
    return(
        <div className="fix2">
            <header>
                <a href="/" className="fw-bold h4 mb-0 ms-4 me-4 logo"> GamesBank </a>
                <nav className = "d-flex">
                </nav>
           
                <div className="searchbar">
                <input
                        type="text"
                        placeholder="Search"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                                handleSearch();
                            }
                        }}
                    />
      
                    <FontAwesomeIcon
                        className="me-2 lupa"
                        icon={faSearch}
                        onClick={handleSearch}
                    />

                </div>

            </header>
        </div>
    )
}