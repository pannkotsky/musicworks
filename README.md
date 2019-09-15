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

## Saving music works

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

Note that bulk create response returns a list of items whose length is equal to length of input data. Actual number of created items can be less in case of found matches. This is to be fixed. Ignore this response for now and go straight to GET endpoint to observe the result.

Process of getting new info from providers can be automatized in two major ways.

1. Polling provider's API on a regular basis. In this case we need to setup periodic tasks using tasks queueing service like Celery with celery-beat and some message broker like rabbit-mq. We'll convert the data to our format via adapter and use it to feed to WorkSerializer.

2. Providing our API to provider and subscribing for receiving new info. Some sort of adapters may be needed for different providers as well.

## Getting info

Reconciled works can be viewed by accessing http://localhost:8000/api/works/ endpoint. By default it will display DRF's HTML view. Raw JSON data can be viewed by adding `?format=json` query param. Items in CSV format can be dowloaded by adding `?format=csv` query param.

By default response is paginated in 20 items slices. Filtering, search, ordering options are also available. These customization capabilites via query params can be examined at http://localhost:8000/api/docs/ and by exploring DRF's HTML view. For example, list can be filtered by comma-separated list of iswc's like this: http://localhost:8000/api/works/?iswc__in=T9204649558,T0101974597.

Single entity can be viewed via http://localhost:8000/api/works/T9204649558/ endpoint.

Response time of all endpoints should not suffer too much with data volume increase. While performing matching and reconciliation database lookups use indexes so they should be pretty fast. While retrieving data pagination should prevent delays.
