import React, {useEffect, useState} from 'react';
import './home.css';
import {Header} from "../components/header/header";
import axios from "axios";
import {Banner} from "../components/banner/banner";
import {Movies} from "../components/movies/movies";
const Home = () => {
    
    axios.default.withCredentials = true;

    const [popular,setPopular] = useState([])

    
    const getMostPopular = async () => {
        try {
            const response = await axios.get("http://localhost:4000/get_popular");
            setPopular(response.data.response.docs[0]);
        } catch (error) {
            console.error("Error fetching most popular:", error);
        }
    };

    useEffect(() => {
        const popularURL = "";
        getMostPopular(popularURL);
    },[])


    return (
        <div className="home">
            <Header/>
            <Banner id = {popular.id} bg = {popular.img_url} title={popular.name} desc = {popular.desc} rate = {popular.all_reviews / 10}/>
            <Movies/>
        </div>
    );
};

export default Home;