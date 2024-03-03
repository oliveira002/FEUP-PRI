#!/bin/bash
# Variables
NAME="pri_tp1_solr"
# --------- Antes de executar o script, correr um destes antes comandos, no diretorio raiz do projeto ---------
#docker run -p 8983:8983 --name pri_tp1_solr -v ${PWD}:/data -d solr:9.3 solr-precreate games # -> Linux
#docker run -p 8983:8983 --name pri_tp1_solr -v "%cd%":/data -d solr:9.3 solr-precreate games # -> Windows
# Recreate core
echo ""
echo "------------------------"
echo "| Building core: games |"
echo "------------------------"
echo ""
docker exec -it $NAME bin/solr delete -c games
docker exec -it $NAME bin/solr create -c games
# Upload schemas definition via API
echo ""
echo "-------------------------"
echo "| Copying Currency file |"
echo "-------------------------"
echo ""
docker cp config/schemas/currency.xml $NAME:/var/solr/data/games/conf
echo ""
echo "-------------------------"
echo "| Copying Synonyms file |"
echo "-------------------------"
echo ""
docker cp config/schemas/synonyms.txt $NAME:/var/solr/data/games/conf
echo ""
echo "----------------------------"
echo "| Uploading schema to Solr |"
echo "----------------------------"
echo "" 
curl -X POST -H "Content-type:application/json" --data-binary "@./config/schemas/semantic_schema.json" http://localhost:8983/solr/games/schema
# Populate collection using mapped path inside container.
echo "" 
echo "-------------------------------"
echo "| Uploading documents to Solr |"
echo "-------------------------------"
echo "" 
docker exec -it $NAME bin/post -c games /../../data/solr/config/data/semantic_games.json
#curl -X POST -H "Content-type:application/json" --data-binary "@./outputs/games.json" http://localhost:8983/solr/conflicts/update?commit=true
#Open the solr web instance
#start http://localhost:8983/solr/#/games/core-overview
