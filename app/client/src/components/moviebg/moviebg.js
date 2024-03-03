import React, {useEffect, useState} from 'react';
import '../banner/banner.css'
import {faArrowRight, faStar, faPlay} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import axios from 'axios';

export const MovieBg = ({url, name,full_desc,desc,img_url,all_reviews,categories,date,price}) => {
    const originalDate = new Date(date);
    const year = originalDate.getFullYear();
    const month = String(originalDate.getMonth() + 1).padStart(2, '0');
    const day = String(originalDate.getDate()).padStart(2, '0');
    const c_date = `${year}-${month}-${day}`;
    const parsed = categories && categories.join(' • ')
    const truncatedWords = full_desc && full_desc.slice(0, 800) + "...";
    const [poster, setPoster] = useState(null)
    const new_price = (!price || price == '0.0,USD') ? "Free" : (price.split(',')[0] + "$")
    const [videoUrl, setVideoUrl] = useState(null);
    console.log(videoUrl);
   


    const handleSearch = async () => {
        try {
          if (name) { 
            const match = url && url.match(/\/app\/(\d+)\//);
            const steamID = match && match[1]
            const response_trailer = await axios.get(`http://localhost:4000/trailer/${steamID}`);
            const response = await axios.get(`http://localhost:4000/poster/${name}`);

            setVideoUrl(response_trailer.data.videoUrl);
      
            setPoster(response.data.inline_images[0].thumbnail);
          }
        } catch (error) {
          console.error("Error fetching poster:", error);
        }
      };

      useEffect(() => {
        if(name) {
            handleSearch();
        }
      }, [name]);
   
    return(
        <div className="d-flex flex-column">
            <div className="movieBanner mt-4">
                <div className="">
                    <div className="d-flex flex-column posterpic">
                        <div className="ratingcircle d-flex">
                            <span className="posterRate fw-bold">{all_reviews/10}</span>
                        </div>
                    
                        {poster && 
                            <img className="poster" src={poster} alt='poster'/>
                        }
                    </div>
                    <div className="d-flex flex-column overText">
                        <div className="d-flex titulo">
                            <span className="title fw-bold h5">{name}</span>
                        </div>
                        <ul className="sec">
                            <li className="d-flex">
                                <span className="fw-bold undertitle">Release Date: </span>
                                <span className="ms-1">{c_date}</span>
                            </li>
                            <li className="d-flex">
                                <span className="fw-bold undertitle"> Genres: </span>
                                <div className="d-flex ms-1">
                                    <span className="ms-1"> {parsed}</span>
                                </div>
                            </li>
                        </ul>
                        <div className="d-flex">
                                <span className="fw-bold undertitle">Price: </span>
                                <span className="ms-1">{new_price}</span>
                        </div>
                        <div className="overview d-flex flex-column">
                            <span className="fw-bold undertitle">Overview:</span>
                            <span className='truncated'>{truncatedWords}</span>
                        </div>
                        <div className="d-flex mt-2">
                            <a href={videoUrl} target="_blank" className="check2 fw-bold">  <FontAwesomeIcon className="ms-1" icon={faPlay}/> Trailer </a>
                            <a href= {url} target="_blank" className="check3 fw-bold ms-3"> Steam Store </a>
                        </div>
                    </div>
                </div>
                <img className="bgg" src={img_url}/>
            </div>
        </div>
    )
}