Historical games where the player can command an army

### Basic Query 
http://localhost:8983/solr/#/games/query?q=(historical)%20and%20(command%20army)&q.op=AND&defType=edismax&indent=true&fl=*,score&lowercaseOperators=true&qf=full_desc%20desc&wt=json&useParams=

#### Result

### Enhanced Query 
http://localhost:8983/solr/#/games/query?bf=linear(all_reviews,0,100)%5E1.5&defType=edismax&fl=*,score&indent=true&lowercaseOperators=true&q.op=AND&q=(historical)%5E2%20and%20(command%20army)%5E3&qf=full_desc%20desc&useParams=&wt=json

#### Result