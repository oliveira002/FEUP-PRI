import React from "react";
import {useContext, useEffect, useState} from "react";
import './cast.css'
import {faSearch, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';
import Axios from "axios";


export const Cast = (props) => {
    const profileUrl = `https://image.tmdb.org/t/p/w300_and_h450_bestv2/${props.actor.profile_path}`
    return(
        <div className="d-flex flex-column cast me-2 align-items-center">
            <img src = {profileUrl} width="202" height="304"/>
            <p className="fw-bold mt-2">{props.actor.original_name}</p>
            <p className="">{props.actor.character}</p>
        </div>
    )
}