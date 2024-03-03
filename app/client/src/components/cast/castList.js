import React from "react";
import {useContext, useEffect, useState} from "react";
import './cast.css'
import {faSearch, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';
import Axios from "axios";
import { Cast } from "./cast";


export const CastList = (props) => {
    return(
        <div className="content mt-4">
            <span className="h4 fw-bold uptitle">Cast</span>
            <div className="d-flex mt-2 castList">
                {props.cast.map((actor,index) => {
                    return <Cast key = {index} actor = {actor}/>
                })}
            </div>
        </div>
    )
}