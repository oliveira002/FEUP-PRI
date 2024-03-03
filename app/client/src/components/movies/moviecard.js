import React, {useEffect, useState} from 'react';
import './movies.css'
import {faSearch, faStar, faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { useNavigate } from 'react-router-dom';

export const MovieCard = ({id,name,desc,img_url,all_reviews,categories,date,price, price____l_ns}) => {
    const originalDate = new Date(date);
    const year = originalDate.getFullYear();
    const month = String(originalDate.getMonth() + 1).padStart(2, '0');
    const day = String(originalDate.getDate()).padStart(2, '0');
    const c_date = `${year}-${month}-${day}`;
    const rating = !all_reviews ? "No Rating" : all_reviews/10
    const new_price = (!price || price === '0.0,USD') ? "Free" :(price____l_ns/100 + "$")
    const words = desc.split(' ');
    const truncatedWords = words.slice(0, 17);
    const ab_desc = truncatedWords.join(' ') + '...';

    const navigate = useNavigate()

    const navigatePage = (id) => {
        navigate(`/game/${id}`);
    };

    return(
        <li className="movieCard" >
            <img src={img_url}/>
            <div className="space mt-2">
                <a href={`/game/${id}`} className="fw-bold h5 ms-2">{name}</a>
                <span href="#" className="h6 ms-2 description">{ab_desc}</span>
                <div className="d-flex tudo">
                    <span className="subra fw-bold ms-2">Rating:</span>
                    <div className="d-flex rat ms-2">
                        <span className="sub fw-bold">{rating}</span>
                        <FontAwesomeIcon icon={faStar}/>
                    </div>
                    <span className="subra fw-bold ms-2">Price:</span>
                    <span className="sub fw-bold ms-2">{new_price}</span>
                    <span className="subra fw-bold ms-2">Release:</span>
                    <span className="sub fw-bold ms-2 danger">{c_date}</span>
                    </div>
                    <button className="follow fw-bold" onClick={() => navigatePage(id)}>More Details</button>
                
            </div>
        </li>
    )
}