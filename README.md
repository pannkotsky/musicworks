# Works Single View

A Single View application aggregates and reconciles data from multiple sources to create a single view of an entity, in this case, a musical work.

## How to run

1. Make sure to have [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/v17.09/compose/install/) installed.

2. Clone the repo
```bash
  git clone git@github.com:pannkotsky/musicworks.git
```

3. cd into project directory
```bash
  cd musicworks
```

4. Bring up everything
```bash
  make all_up
```

After a while API root should be available at http://localhost:8000/api/

Containers can be stopped by pressing CTRL+C.

API has the following endpoints:
- contributors: http://localhost:8000/api/contributors/
- sources: http://localhost:8000/api/sources/
- works: http://localhost:8000/api/works/


Their specification can be viewed at http://localhost:8000/api/docs/.

API documentation is auto-generated and has some inaccuracies which are about to be fixed:
- works list endpoint response is actually regular list of entities
- request format can also accept entites list additionally to single entity (bulk create)
