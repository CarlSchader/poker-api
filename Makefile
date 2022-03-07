USERNAME = carlschader

run:
	docker compose -f docker/docker-compose.yaml up --build

kill:
	docker compose -f docker/docker-compose.yaml down

build:
	docker build -t poker-api:latest -f docker/Dockerfile .

publish:
	docker login

	docker build -t ${USERNAME}/poker-api:arm -f docker/Dockerfile-arm .
	docker build -t ${USERNAME}/poker-api:amd -f docker/Dockerfile-amd .

	docker push ${USERNAME}/poker-api:arm
	docker push ${USERNAME}/poker-api:amd
	
	docker manifest create \
	${USERNAME}/poker-api:latest \
	--amend ${USERNAME}/poker-api:arm \
	--amend ${USERNAME}/poker-api:amd \

	docker manifest push ${USERNAME}/poker-api:latest

publish-populate-redis:
	docker login

	docker build -t ${USERNAME}/poker-populate-redis:arm -f docker/Dockerfile-populate-redis-arm .
	docker build -t ${USERNAME}/poker-populate-redis:amd -f docker/Dockerfile-populate-redis-amd .

	docker push ${USERNAME}/poker-populate-redis:arm
	docker push ${USERNAME}/poker-populate-redis:amd

	docker manifest create \
	${USERNAME}/poker-populate-redis:latest \
	--amend ${USERNAME}/poker-populate-redis:arm \
	--amend ${USERNAME}/poker-populate-redis:amd \

	docker manifest push ${USERNAME}/poker-populate-redis:latest

publish-all:
	docker login

	docker build -t ${USERNAME}/poker-api:arm -f docker/Dockerfile-arm .
	docker build -t ${USERNAME}/poker-api:amd -f docker/Dockerfile-amd .

	docker push ${USERNAME}/poker-api:arm
	docker push ${USERNAME}/poker-api:amd
	
	docker manifest create \
	${USERNAME}/poker-api:latest \
	--amend ${USERNAME}/poker-api:arm \
	--amend ${USERNAME}/poker-api:amd \

	docker manifest push ${USERNAME}/poker-api:latest

	docker build -t ${USERNAME}/poker-populate-redis:arm -f docker/Dockerfile-populate-redis-arm .
	docker build -t ${USERNAME}/poker-populate-redis:amd -f docker/Dockerfile-populate-redis-amd .

	docker push ${USERNAME}/poker-populate-redis:arm
	docker push ${USERNAME}/poker-populate-redis:amd

	docker manifest create \
	${USERNAME}/poker-populate-redis:latest \
	--amend ${USERNAME}/poker-populate-redis:arm \
	--amend ${USERNAME}/poker-populate-redis:amd \

	docker manifest push ${USERNAME}/poker-populate-redis:latest