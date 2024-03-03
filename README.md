# FEUP-PRI

| | Milestone 1 | Milestone 2 | Milestone 3 |
| --- | --- | --- | --- |
| Grade | **88.70%** | **89.40%**| **88.60%** | 

## Execution instructions
In the root directory of the project (where this file is located) run one of the following commands, depending on your OS:
- UNIX based: `docker run -p 8983:8983 --name pri_tp1_solr -v ${PWD}:/data -d solr:9.3 solr-precreate games`
- Windows: `docker run -p 8983:8983 --name pri_tp1_solr -v "%cd%":/data -d solr:9.3 solr-precreate games`

Note that this command only needs to be ran once. As long as the docker container created by this command exists, there's no need to run it again.

Now, go to the /solr directory and execute the startup script that takes care of injecting the schema and documents:
`cd solr`
`bash startup.sh`
