import React from "react";
import {useContext, useEffect, useState} from "react";
import './review.css';
import {faSearch, faUser, faStar, faArrowUp} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';

export const ReviewCard = (props) => {

    function convertTimestampToDateString(timestamp) {
        const date = new Date(timestamp * 1000); // Convert to milliseconds
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
    }

    const formattedDate = convertTimestampToDateString(props.review.timestamp_created);

    return(
        <div className="box mb-4">
            <div className="d-flex">
                <div className="ms-3 mt-3">
                    <div className="d-flex">
                        <FontAwesomeIcon className="h5 me-2" icon={faUser}/>
                        <span className="fw-bold h5">{props.review.author.steamid}</span>
                        <div className="d-flex align-items-center authorRate ">
                            <span className="fw-bold ms-2 h6"> {props.review.votes_up}</span>
                            <FontAwesomeIcon className="ms-1 mb-2" icon={faArrowUp}/>
                        </div>
                    </div>
                    <p className="fw-light"> Written on {formattedDate} </p>
                    <span className="max-lines mt-1">{props.review.review}</span>
                </div>
            </div>
        </div>
    )
}