Highest-rated open-world RPGs set in fantasy realms

### Basic Query 

http://localhost:8983/solr/#/games/query?defType=edismax&fl=*,score&indent=true&lowercaseOperators=true&q.op=AND&q=%22open%20world%22~2%0A%22RPG%22%0A%22fantasy%20realms%22~2&qf=full_desc%20desc&rows=48219&useParams=&wt=json

#### Result

### Enhanced Query
http://localhost:8983/solr/#/games/query?bf=product(if(exists(query(%7B!v%3D'name:%22RPG%22'%7D)),2,1),exp(product(all_reviews,0.03)))&defType=edismax&fl=*,score&indent=true&lowercaseOperators=true&q.op=AND&q=%22open%20world%22~2%0A%22RPG%22%5E3%0A%22fantasy%20realms%22~2&qf=full_desc%20desc&rows=48219&useParams=&wt=json

#### Result