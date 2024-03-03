const express = require('express');
const app = express();
const cors = require("cors");
const sampleController = require('./controllers/sampleController');


app.use(express.json());

app.use(cors());

app.get('/api/search', sampleController.getSampleData);
app.get('/get_popular', sampleController.getPopular);
app.get('/get_rated', sampleController.getRated);
app.get('/get_cheapest', sampleController.getCheapest);
app.get('/get_latest', sampleController.getLatest);
app.get('/game/:id', sampleController.getGameId);
app.get('/gameReviews/:id', sampleController.getReviews);
app.get('/poster/:name', sampleController.getPoster);
app.get('/trailer/:id', sampleController.getTrailer);

app.listen(4000, () => {
    console.log(`Server is running on http://localhost:4000`);
  });