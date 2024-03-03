### Basic 1st query 

#### Link 

http://localhost:8983/solr/#/games/query?q=full_desc:(underwater%20*)%20OR%20%0A%20%20%20%20full_desc:%20(underwater%20setting)%5E3%20OR%0A%20%20%20%20desc:(underwater%20*)%20OR%20%0A%20%20%20%20desc:(underwater%20setting)%5E3&q.op=AND&indent=true&fq=categories:%20single-player%20date:%5BNOW%2FDAY-3653DAYS%20TO%20NOW%5D&useParams=

#### Query
`full_desc:(underwater *) OR 
    full_desc: (underwater setting)^3 OR
    desc:(underwater *) OR 
    desc:(underwater setting)^3`

#### Query operator
`AND`

#### Filter query
`categories: single-player date:[NOW/DAY-3653DAYS TO NOW]`

#### Result

http://localhost:8983/solr/games/select?fq=categories%3A%20single-player%20date%3A%5BNOW%2FDAY-3653DAYS%20TO%20NOW%5D&indent=true&q.op=AND&q=full_desc%3A(underwater%20*)%20OR%20%0Afull_desc%3A%20(underwater%20setting)%5E3%20OR%0Adesc%3A(underwater%20*)%20OR%20%0Adesc%3A(underwater%20setting)%5E3&useParams=

### 2nd query 

#### Link 


#### Query
``

#### Query operator
``

#### Filter query
``

#### Result


### 3rd query 

#### Link 


#### Query
``

#### Query operator
``

#### Filter query
``

#### Result


### 4th query 

#### Link 


#### Query
``

#### Query operator
``

#### Filter query
``

#### Result


### 5th query 

#### Link 


#### Query
``

#### Query operator
``

#### Filter query
``

#### Result


### 6th query 

#### Link 


#### Query
``

#### Query operator
``

#### Filter query
``

#### Result

