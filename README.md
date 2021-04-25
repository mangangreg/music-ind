# Music Industry Networks
A network analysis exploration of producers/writers in chart music.



## App
Docker app with the following containers:

- *Musicbrain* a flask app that
  - scrapes chart pages from wikipedia
  - scrapes song pages from wikipedia
  - parses song pages

- *db*: a mongo db instance that houses
  - raw htmls (landing zone)
  - parsed documents (clean zone)

- *airflow*: for orchestration


Todo:
- Network analysis dashboard app
- neo4j instance to model network data?