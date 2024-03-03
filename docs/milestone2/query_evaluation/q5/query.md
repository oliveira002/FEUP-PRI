2D platform game where the main character is an animal

### Basic Query 
 
http://localhost:8983/solr/#/games/query?q=%222D%20platform*%22~2%0A((play%20animal)%20or%20(control%20animal))&q.op=AND&defType=edismax&indent=true&fl=*,score&lowercaseOperators=true&qf=full_desc%20desc&rows=50&useParams=

#### Result

### Enhanced Query 

http://localhost:8983/solr/#/games/query?q=%222D%20platform*%22~2%0A((%22play%20animal%22~3%5E2)%20or%20(%22control%20animal%22~3%5E2))&q.op=AND&defType=edismax&indent=true&fl=*,score&lowercaseOperators=true&qf=full_desc%20desc&rows=50&useParams=

#### Result