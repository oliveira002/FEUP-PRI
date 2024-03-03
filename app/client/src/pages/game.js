import React, {useEffect, useState} from 'react';
import { useParams } from "react-router-dom";
import './game.css';
import {Header} from "../components/header/header";
import {MovieBg} from "../components/moviebg/moviebg";
import axios from "axios";
import { Cast } from '../components/cast/cast';
import { CastList } from '../components/cast/castList';
import { Review } from '../components/moviebg/review';
import { ReviewList } from '../components/moviebg/reviewList';

const Game = () => {
    const {id} = useParams();
    const [game,setGame] = useState([]);

    const getGame = async() => {
        try {
            const response = await axios.get(`http://localhost:4000/game/${id}`);
            setGame(response.data.response.docs[0]);
            console.log(game && game)

        } catch (error) {
        console.error("Error fetching most popular:", error);
        }
    }

    const getReview = async(url) => {

    }


    useEffect(() => {
        getGame();
    },[])

    return (
        <div>
            <Header/>
            <MovieBg {...game}/>
            <ReviewList {...game}/>
        </div>
    );
};

export default Game;