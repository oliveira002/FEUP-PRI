import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/home';
import Game from './pages/game';
import Search from './pages/search';
import Axios from "axios";
import React from 'react';

class App extends React.Component {
    render() {
        return (
            <Router>
                    <Routes>
                        <Route path='/'  element={<Home />} />
                        <Route path='game/:id'  element={<Game />} />
                        <Route path='/search' element={<Search />} />
                    </Routes>
            </Router>
        );
    }
}
export default App;
