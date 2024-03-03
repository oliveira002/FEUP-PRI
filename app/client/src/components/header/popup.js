import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import './header.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUser} from "@fortawesome/free-solid-svg-icons";
import Axios from "axios";
import {useContext, useEffect, useState} from "react";

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    boxShadow: 'rgba(0, 0, 0, 0.2) 0px 2px 2px 0px',
    borderRadius: '8px',
    p: 4,
};

export const BasicModal = (props) => {
    const [error,setError] = useState("");
    const [errorL,setErrorL] = useState("");
    const [userReg, setUserReg] = useState("");
    const [pwReg, setPwReg] = useState("");
    
    return (
            <div>
                <Modal className = "mypopup" open={props.open} onClose={props.onClose}>
                    <Box sx={style}>
                        <form className="d-flex flex-column">
                            <span className="h3 titlelogin"> Login </span>
                            <span className="h5 align-self-center mt-2"> {errorL}</span>
                            <input type="text" onChange={(e) => {setUserReg(e.target.value)}} placeholder="Username" name="username"/>
                            <input type="password" onChange={(e) => {setPwReg(e.target.value)}} placeholder="Password" name="password"/>
                            <span className="align-self-center mb-2"> Forgot your password? </span>
                            <button className="log" type="submit"> Login </button>
                        </form>
                    </Box>
                </Modal>
            </div>
    );
}
