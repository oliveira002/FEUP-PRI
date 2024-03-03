import React from "react";
import {useContext, useEffect, useState} from "react";
import './review.css';
import {faSearch, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';
import { ReviewCard } from "./review";
import axios from "axios";

export const ReviewList = ({url, name,full_desc,desc,img_url,all_reviews,categories,date,price}) => {


    const [reviews, setReviews] = useState([])

    const match = url && url.match(/\/app\/(\d+)\//);
    const steamID = match && match[1]
    
    const getReviews = async () => {
        try {
            if(steamID) {
                const response = await axios.get(`http://localhost:4000/gameReviews/${steamID}?json=1`);
                setReviews(response.data.reviews.slice(0,4))
            }
        } catch (error) {
            console.error("Error fetching most popular:", error);
        }
    };

    useEffect(() => {
        if(steamID) {
            getReviews();
        }
      }, [steamID]);

    return(
        <div className="content mt-4">
            <span className="h4 fw-bold uptitle">Reviews</span>
            <div className="mt-4">
                {reviews && reviews.map((rev,index) => {
                        return <ReviewCard key={index} review = {rev}/>
                    })}
            </div>
        </div>
    )
}