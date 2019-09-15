build:
	docker-compose -f docker-compose.db.yml -f docker-compose.web.yml build

db_up:
	docker-compose -f docker-compose.db.yml up -d

all_up:
	docker-compose -f docker-compose.db.yml -f docker-compose.web.yml up

db_stop:
	docker-compose -f docker-compose.db.yml stop

db_status:
	docker-compose -f docker-compose.db.yml ps

all_status:
	docker-compose -f docker-compose.db.yml -f docker-compose.web.yml ps
