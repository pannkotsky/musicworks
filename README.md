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

## API description

API has the following endpoints:
- contributors: http://localhost:8000/api/contributors/
- sources: http://localhost:8000/api/sources/
- works: http://localhost:8000/api/works/


Their specification can be viewed at http://localhost:8000/api/docs/.

API documentation is auto-generated and has some inaccuracies which are about to be fixed:
- works list endpoint response is actually regular list of entities
- request format can also accept entites list additionally to single entity (bulk create)

Music work can be created using http://localhost:8000/api/works/ endpoint via POST requests. It accepts data in several formats:
- creating a single item sending an object in JSON format
- creating several items in bulk sending an array of objects in JSON format
- creating several items in bulk via uploading a CSV file

In any case input data is converted into new database entry or matched to existing entry with some merging information mechanism (reconciliation).

Under the hood it goes like this:
1. In case of uploading CSV file its data is parsed by custom [CSVMultipartParser](https://github.com/pannkotsky/musicworks/blob/master/common/parsers.py#L5) into the same format that would come from JSON.
2. Input data is converted into internal representation by serializers.
3. Related objects are created. Contributors are created by parsing full names into parts (first_name, middle_name, last_name). This part is obviously not perfect, you can see a note on it and source code [here](https://github.com/pannkotsky/musicworks/blob/master/works/managers/contributor.py#L5).
4. Data prepared for Work instance creation is then tried to match with existing object. See matching algorithm description and source code [here](https://github.com/pannkotsky/musicworks/blob/master/works/managers/work.py#L6).
5. If match is not found data is simply saved as a new database entry. If match is found it is reconciled with the matched entry. Description and source code of this mechanism is [here](https://github.com/pannkotsky/musicworks/blob/master/works/models/work.py#L35).
