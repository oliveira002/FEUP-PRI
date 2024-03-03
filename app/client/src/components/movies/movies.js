import React, {useEffect, useState} from 'react';
import './movies.css'
import {faSearch, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {MovieCard} from "./moviecard";
import axios from "axios";

export const Movies = () => {
    const [topRated,setTopRated] = useState([])
    const [latest,setLatest] = useState([])
    const [cheapest,setCheapest] = useState([])

    const fetchAPI = async (url) => {
        try {
            const response = await axios.get(url);
            console.log(response.data.response.docs);
            return response.data.response.docs;
        } catch (error) {
            console.error(`Error fetching data from ${url}:`, error.message);
            throw error; // rethrow the error to stop execution or handle it appropriately
        }
    };
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const ratedData = await fetchAPI("http://localhost:4000/get_rated");
                const latestData = await fetchAPI("http://localhost:4000/get_latest");
                const cheapestData = await fetchAPI("http://localhost:4000/get_cheapest");
    
                setTopRated(ratedData.slice(0,4));
                setLatest(latestData.slice(0,4));
                setCheapest(cheapestData.slice(0,4));
            } catch (error) {
                console.error("Error fetching data:", error.message);
            }
        };
    
        fetchData();
    }, []);

    return(
        <div className="list">
            <span className="h4 fw-bold mt-4 uptitle">Top Rated Games</span>
            <ul className="upcoming">
                {topRated.map((game,index) => {
                    return <MovieCard key = {index} {...game}/>
                })}
            </ul>
            <span className="h4 fw-bold mt-4 uptitle">Latest Games</span>
            <ul className="upcoming">
                {latest.map((game,index) => {
                    return <MovieCard key = {index} {...game}/>
                })}
            </ul>
            <span className="h4 fw-bold mt-4 uptitle">Cheapest Games</span>
            <ul className="upcoming">
                {cheapest.map((game,index) => {
                    return <MovieCard key = {index} {...game}/>
                })}
            </ul>
        </div>
    )
}