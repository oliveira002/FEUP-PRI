const axios = require('axios');
const cheerio = require('cheerio');
const getSampleData = async (req, res) => {
  try {
    let { q, operator, qf, category, boost_query,boost_function, min_price, max_price, date} = req.query;

    if (!q || !operator || !qf) {
      return res.status(400).json({ error: 'Both q and qf are required query parameters' });
    }
    if(category){
      q += ` categories:${category}`;
    }
    //const solrQueryString = `?defType=edismax&q.op=&defType=edismax&indent=true&rows=10&qf=full_desc%20desc%20name&useParams=`;
    let solrQueryString = `defType=edismax&indent=true&q.op=${encodeURIComponent(operator)}&q=${encodeURIComponent(q)}&qf=${encodeURIComponent(qf)}&useParams=&rows=48`;
    if(max_price && min_price){
      max_price *= 100;
      min_price *= 100;
      solrQueryString += "&fq="+ encodeURIComponent(`price____l_ns:[${min_price} TO ${max_price}]`);
    }

    if(boost_function){
      solrQueryString += "&bf="+ encodeURIComponent(boost_function);
    }
    if(boost_query){
      solrQueryString += "&bq="+ encodeURIComponent(boost_query);
    }
    if(date){
      if(date === "pastyear")
        date = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString();
      else if(date === "pastmonth")
        date = new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString();
      else if(date === "pasttwoyears")
        date = new Date(new Date().setFullYear(new Date().getFullYear() - 2)).toISOString();
      else if(date === "pastfiveyears")
        date = new Date(new Date().setFullYear(new Date().getFullYear() - 5)).toISOString();
      else if(date === "alltime")
        date = new Date(new Date().setFullYear(new Date().getFullYear() - 100)).toISOString();
      console.log(date);
      solrQueryString += "&fq="+ encodeURIComponent(`date:[${date} TO *]`);
    }
    const solrServerUrl = 'http://localhost:8983/solr/games/select?';

    // Make the GET request to the Solr server
    const response = await axios.get(solrServerUrl + solrQueryString);

    // Return the Solr server response as JSON
    res.json(response.data);

  } catch (error) {
    console.error('Error querying Solr:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

const getPopular = async (req, res) => {
    try {
      const solrServerUrl = 'http://localhost:8983/solr/games/select?defType=edismax&indent=true&q.op=OR&q=cs%3Ago&qf=full_desc%20desc%20name&useParams=';
      const response = await axios.get(solrServerUrl);
  
      // Return the Solr server response as JSON
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  };

  const getCheapest = async (req, res) => {
    try {
      const solrServerUrl = 'http://localhost:8983/solr/games/select?bf=if(exists(query(%7B!v%3D%27price____l_ns%27%7D))%2Cdiv(1%2Cprice____l_ns)%2C0)&bq=price____l_ns%3A%5B0%20TO%20999%5D&defType=edismax&fl=*%2Cscore&indent=true&lowercaseOperators=true&q.op=OR&q=*%3A*&qf=full_desc%20desc&rows=20&useParams=&wt=json';
      const response = await axios.get(solrServerUrl);
  
      // Return the Solr server response as JSON
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  };

  const getLatest = async (req, res) => {
    try {
      const solrServerUrl = 'http://localhost:8983/solr/games/select?defType=edismax&fq=date%3A%5B*%20TO%202023-12-31T23%3A59%3A59Z%5D&indent=true&q.op=AND&q=*%3A*&rows=50&sort=date%20desc&start=0&useParams=';
      const response = await axios.get(solrServerUrl);
  
      // Return the Solr server response as JSON
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  };
  
  const getRated = async (req, res) => {
    try {
      const solrServerUrl = 'http://localhost:8983/solr/games/select?defType=edismax&fq=all_reviews%20%3A%20%5B80%20TO%2090%5D&fq=date%3A%5B*%20TO%202023-12-31T23%3A59%3A59Z%5D&indent=true&q.op=AND&q=*%3A*&rows=50&sort=all_reviews%20desc&useParams=';
      const response = await axios.get(solrServerUrl);
  
      // Return the Solr server response as JSON
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  };

  const getGameId = async(req,res) => {
    const id = req.params.id;
    const solrServerUrl = `http://localhost:8983/solr/games/select?defType=edismax&fl=*%2Cscore&fq=id%3A%20${id}&indent=true&lowercaseOperators=true&q.op=AND&q=*%3A*&qf=full_desc%20desc&rows=20&useParams=&wt=json`;
    try {  
    const response = await axios.get(solrServerUrl);
  
      // Return the Solr server response as JSON
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  const getPoster = async(req,res) => {
    var name = req.params.name;
    name = name.replace(/[^\x00-\x7F]/g, "");
    const serpApiEndpoint = "https://serpapi.com/search"
    try {
      const response = await axios.get(serpApiEndpoint, {
        params: {
          api_key: "0560a17f24c7e5b1e159d6236c95a2c3a79d8048cff50eb8fa051fa8a01b52af",
          q: `${name} poster`,
        },
      });

      res.json(response.data)

    } catch (error) {
      console.error('Error fetching search results:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  const getReviews = async(req,res) => {
    var id = req.params.id;
    const gameReviews = `https://store.steampowered.com/appreviews/${id}?json=1`;
    try {  
    const response = await axios.get(gameReviews);
      res.json(response.data);
  
    } catch (error) {
      console.error('Error querying Solr:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
  const getTrailer = async(req,res) => {
    var id = req.params.id;
    try {
      const gameUrl = `https://store.steampowered.com/app/${id}`
 
      const response = await axios.get(gameUrl);
      
      if (response.status === 200) {
        
        const $ = cheerio.load(response.data);

        const videoElement = $('.highlight_movie').first();
        const webmSource = videoElement.attr('data-webm-source');

        if (webmSource) {
          res.json({ videoUrl: webmSource });
        }
        else {
          res.status(404).json({ error: 'Trailer not found' });
        }
        
       
      } else {
        res.status(404).json({ error: 'Game not found' });
        
      }
    } catch (error) {
      res.status(500).json({ error: 'Internal server error' });
    }
  }

module.exports = {
  getSampleData,
  getPopular,
  getCheapest,
  getLatest,
  getRated,
  getGameId,
  getPoster,
  getReviews,
  getTrailer
};