# FEUP-PRI

## Information Needs
1. Single-player games released in the last decade with an underwater setting
    - [X] Simple query
    - [X] Advanced query
    - [X] qrels
1. Cheapest Games with futuristic landscapes or advanced technology
    - [X] Simple query
    - [X] Advanced query
    - [X] qrels
1. First-person shooter in a post-apocalyptic setting with custom player-made buildings
    - [ ] Simple query
    - [ ] Advanced query
    - [ ] qrels
1. Historical games where the player can command an army
    - [X] Simple query
    - [X] Advanced query
    - [X] qrels
1. 2D platform game where the main character is an animal
    - [X] Simple query
    - [X] Advanced query
    - [X] qrels
1. Highest-rated open-world RPGs set in fantasy realms
    - [X] Simple query
    - [X] Advanced query
    - [X] qrels
1. Strategy games featuring mythical creatures and epic battles
    - [ ] Simple query
    - [ ] Advanced query
    - [ ] qrels

## Execution instructions
In the root directory of the project (where this file is located) run one of the following commands, depending on your OS:
- UNIX based: `docker run -p 8983:8983 --name pri_tp1_solr -v ${PWD}:/data -d solr:9.3 solr-precreate games`
- Windows: `docker run -p 8983:8983 --name pri_tp1_solr -v "%cd%":/data -d solr:9.3 solr-precreate games`

Note that this command only needs to be ran once. As long as the docker container created by this command exists, there's no need to run it again.

Now, go to the /solr directory and execute the startup script that takes care of injecting the schema and documents:
`cd solr`
`bash startup.sh`
