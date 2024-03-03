import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { faCaretDown, faCaretUp } from '@fortawesome/free-solid-svg-icons';
import './search.css';
import FormGroup from '@mui/material/FormGroup';
import Checkbox from '@mui/material/Checkbox';
import Slider from '@mui/material/Slider';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import { MovieCard } from '../components/movies/moviecard';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Alert from '@mui/material/Alert';

import TablePagination from '@mui/material/TablePagination';



const Search = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [category, setCategory] = useState('');
    const [date, setDate] = useState('');
    const [request, setRequest] = useState('');
  
    const [queryOperator, setQueryOperator] = useState('and');
    const [queryField, setQueryField] = useState([true, true, true]);
    const [boostFunction, setBoostFunction] = useState('');
    const [boostQuery, setBoostQuery] = useState('');

    const [priceRange, setPriceRange] = useState([0, 100]); 
    const [closedLists, setClosedLists] = useState(Array(5).fill(true));

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get('query');


    useEffect(() => {
        console.log('Query:', query);
        if (query) {
            setSearchQuery(query);
            setRequest(query);
            
         
        }
    }, [query]);
    useEffect(() => {
        if(request) {
            handleSearch();
        }
    }, [request]);
  
    const handleChange = (event, newValue) => {
        setPriceRange(newValue);
    };


    useEffect(() => {
        if (query) {
        setSearchQuery(query);
        }
    }, [query]);
      

        const handleSearch = async () => {

            const queryParams = new URLSearchParams(location.search);
            queryParams.set('query', searchQuery);

            window.history.replaceState({}, '', `${location.pathname}?${queryParams.toString()}`);
            
            const queryFieldString = queryField.reduce((acc, curr, index) => {
                if (curr) {
                    return acc + ' ' + ['name', 'desc', 'full_desc'][index];
                } else {
                    return acc;
                }
            }, '');
        



            try {
                const response = await axios.get(`http://localhost:4000/api/search`, {
                    params: {
                        'q': searchQuery,
                        'operator': queryOperator,
                        'qf' : queryFieldString,
                        'category': category,
                        'boost_function': boostFunction,
                        'boost_query': boostQuery,
                        'min_price': priceRange[0],
                        'max_price': priceRange[1],
                        'date': date
                    }
                });
    
                console.log(response.data.response);
                setTopRated(response.data.response.docs);
               
            } catch (error) {
                console.error('Error searching games:', error);
            }
        };

    const [topRated,setTopRated] = useState([])
   
    const [page, setPage] = useState(0);
    const gamesPerPage = 12;
    const [rowsPerPage, setGamesPerPage] = useState(gamesPerPage); 
  
    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };
    const handleChangeRowsPerPage = (event) => {
        setPage(0);
        setGamesPerPage(parseInt(event.target.value, 10));
    };
 

    const handleQueryFieldChange = (index) => {
        const updatedQueryField = [...queryField];
        updatedQueryField[index] = !updatedQueryField[index];
        setQueryField(updatedQueryField);
    };

    const toggleList = (index) => {
        const newClosedLists = [...closedLists];
        newClosedLists[index] = !newClosedLists[index];
        setClosedLists(newClosedLists);
    };
    const currentGames = topRated.slice(page * gamesPerPage, page * gamesPerPage + gamesPerPage);
    return (
        <div className="search-page">
            <div className="fix2">
                <header>
                    <a href="/" className="fw-bold h4 mb-0 ms-4 me-4 logo"> GamesBank </a>
                    <nav className = "d-flex">
                    </nav>

             
                    <div className="searchbar">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)
                        }
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                handleSearch();
                                }
                            }
                        }
                        placeholder="Search games..."
                    />
        
                        <FontAwesomeIcon
                            className="me-2 lupa"
                            icon={faSearch}
                            onClick={handleSearch}
                        />

                    </div>


                </header>
            </div>
            <div className='main'>
                <div className="box-category">
                    <ul className="list-unstyled category_menu">
                    
                    <FormGroup>
                    <li className="parent">
                        <FontAwesomeIcon icon={!closedLists[0] ? faCaretDown : faCaretUp} className='fa-down' onClick={() => toggleList(0)}/>
                        
                        <p>Query Operator:</p>
                        <FormControl>

 
    

                            <RadioGroup
                                aria-labelledby="demo-radio-buttons-group-label"
                                defaultValue="and"
                                name="radio-buttons-group"
                                value={queryOperator}
                                onChange={(e) => setQueryOperator(e.target.value)}
                            >
                            <ul  className={!closedLists[0] ? 'list-unstyled closed' : 'list-unstyled'}>
                            
                                <li>
                                    <div className='row1'>
                                    <p id="and">And</p>
                                    <FormControlLabel value="and" control={<Radio />} size="small" />

                              
                                    </div>
                                </li>
                                <li>    
                                    <div className='row1'>
                                        <p id="or">Or</p>
                                        <FormControlLabel value="or" control={<Radio />} size="small" />
                                    </div>
                                </li>
                            </ul>
                            </RadioGroup>
                        </FormControl>
                    
                    </li>
                    </FormGroup>
                    <li className="parent">
                        <FontAwesomeIcon icon={faCaretDown} className='fa-down' onClick={() => toggleList(1)}/>
                        <p>Query Field:</p>

                        <ul className={!closedLists[1] ? 'list-unstyled closed' : 'list-unstyled'}>
                            <li>
                                <div className='row1'>
                                    <p className='query-field'>Name</p>
                                    <Checkbox
                                        checked={queryField[0]}
                                        size='small'
                                        onChange={() => handleQueryFieldChange(0)}
                                        inputProps={{ 'aria-label': 'controlled' }}

                                    />
                                </div>
                            </li>
                            <li>    
                                <div className='row1'>
                                    <p className='query-field'>Description</p>
                                    <Checkbox 
                                        checked={queryField[1]}  
                                        size='small'
                                        onChange={() => handleQueryFieldChange(1)}
                                        inputProps={{ 'aria-label': 'controlled' }}
                                    />
                                </div>
                            </li>
                            <li>    
                                <div className='row1'>
                                    <p className='query-field'>Full Description</p>
                                    <Checkbox 
                                        checked={queryField[2]}
                                          
                                        size='small' 
                                        onChange={() => handleQueryFieldChange(2)}
                                        inputProps={{ 'aria-label': 'controlled' }}
                                    />
                                </div>
                            </li>
                    
                        </ul>
                    </li>
                    <li className="parent">
                        <FontAwesomeIcon icon={faCaretDown} className='fa-down' onClick={() => toggleList(2)}/>
                        <p>Filter Query:</p>
                        <ul className={!closedLists[2] ? 'list-unstyled closed' : 'list-unstyled'}>
                            <li>
                                <div className='row1'>
                                    <p>Price</p>
                                    <Slider
                                        getAriaLabel={() => 'Price'}
                                        getAriaValueText={() => 'Price'}
                                        defaultValue={[priceRange[0], priceRange[1]]}
                                        valueLabelDisplay="auto"
                                        onChange={handleChange}
                                        min={0} 
                                        max={200} 
                                    />
                                
                                    
                                </div>
                                <div>Min Price: {priceRange[0]} $</div>
                                <div>Max Price: {priceRange[1]} $</div>

                            </li>
                            <li>    
                                <div className='row1'>
                                    <p>Release Date</p>
                                    <FormControl sx={{ m: 1, minWidth: 150 }} size="small">
                                    <Select
                                        labelId="demo-select-small-label"
                                        id="demo-select-small"
                                        value={date}
                                
                                        onChange={(e) => setDate(e.target.value)}
                                    >
                                
    
                                        <MenuItem value={"pastyear"}>Past year</MenuItem>
                                        <MenuItem value={"pasttwoyears"}>Past 2 years</MenuItem>
                                        <MenuItem value={"pastfiveyears"}>Past 5 years</MenuItem>
                                        <MenuItem value={"alltime"}>All time</MenuItem>

                                    </Select>                                
                                </FormControl>
                                </div>
                            </li>
                            <li>    
                                <div className='row1'>
                                    <p>Category</p>
                                    <FormControl sx={{ m: 1, minWidth: 150 }} size="small">
                                    <Select
                                        labelId="demo-select-small-label"
                                        id="demo-select-small"
                                        value={category}
                                
                                        onChange={(e) => setCategory(e.target.value)}
                                    >
                                        <MenuItem value={""}>None</MenuItem>
                                        <MenuItem value={"Single-player"}>Single-player</MenuItem>
                                        <MenuItem value={"Multi-player"}>Multi-player</MenuItem>
                                        <MenuItem value={"Co-op"}>Co-op</MenuItem>
                                        <MenuItem value={"Online Co-op"}>Online Co-op</MenuItem>
                                        <MenuItem value={"LAN PvP"}>LAN PvP</MenuItem>
                                        <MenuItem value={"LAN Co-op"}>LAN Co-op</MenuItem>
                                        <MenuItem value={"MMO PvP"}>MMO PvP</MenuItem>
                                        <MenuItem value={"Shared/Split Screen PvP"}>Shared/Split Screen PvP</MenuItem>

                                    </Select>                                
                                </FormControl>

                                </div>
                            </li>

                            
                        
                        </ul>
                    </li>
                    <li className="parent">
                        <FontAwesomeIcon icon={faCaretDown} className='fa-down' onClick={() => toggleList(3)}/>
                        <p>
                            Boost Function
                        </p>
                        <ul className={!closedLists[3] ? 'list-unstyled closed' : 'list-unstyled'}>
                        <li>
                            <div className='row1'>
                            
                                <TextField id="filled-basic" variant="filled" size='small' 
                                onChange={(e) => setBoostFunction(e.target.value)}
                                />
                            </div>
                            
                        </li>
                        
                        </ul>
                    </li>
                    <li className="parent">
                        <FontAwesomeIcon icon={faCaretDown} className='fa-down' onClick={() => toggleList(4)}/>
                        <p>
                            Boost Query
                        </p>
                        <ul className={!closedLists[4] ? 'list-unstyled closed' : 'list-unstyled'}>
                        <li>
                            <div className='row1'>
                            
                                <TextField id="filled-basic" variant="filled" size='small' 
                                onChange={(e) => setBoostQuery(e.target.value)}
                                />
                            </div>
                            
                        </li>
                        
                        </ul>
                    </li>
                
            
                
                    </ul>
                </div>
                <div className='games'>
                <ul className="upcoming">
                {currentGames.length > 0 ? (
                    currentGames.map((game, index) => (
                    <MovieCard key={index} {...game} />
                    ))
                ) : (
                    <div className='row-h'>
                        <Alert severity="info">No Games found!</Alert>
                    </div>
                )}
                    <div className='pagination'>
                        <TablePagination 
                        
                            component="div"
                            count={topRated.length}
                            page={page}
                            onPageChange={handleChangePage}
                            rowsPerPage={rowsPerPage}
                            rowsPerPageOptions={[12, 24, 48]}
                            onRowsPerPageChange={handleChangeRowsPerPage}
                        />
                    </div>
                </ul>
                   
                    
               

                </div>
            </div>
        </div>
    );
};

export default Search;