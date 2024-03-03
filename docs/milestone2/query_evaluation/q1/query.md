Single-player games released in the last decade with an underwater setting

### Basic Query 
http://localhost:8983/solr/#/games/query?defType=edismax&fl=*,score&fq=categories:%20single-player%20date:%5BNOW%2FDAY-3653DAYS%20TO%20NOW%5D&indent=true&lowercaseOperators=true&q.op=AND&q=(%22water%20setting%22~3)%20or%20(%22underwater%20setting%22~2)&qf=full_desc%20desc&rows=5000&useParams=

#### Result

### Enhanced Query 
http://localhost:8983/solr/#/games/query?q=(%22water%20setting%22~3)%5E2%20or%20(%22underwater%20setting%22~2)%5E4&q.op=AND&defType=edismax&indent=true&fl=*,score&lowercaseOperators=true&qf=full_desc%20desc&rows=5000&fq=categories:%20single-player%20date:%5BNOW%2FDAY-3653DAYS%20TO%20NOW%5D&useParams=


#### Result

Single-player games with an underwater setting
