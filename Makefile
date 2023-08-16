PHONY: deploy


deploy:
	: \
	&& docker compose build \
	&& docker-compose up -d --force-recreate \
	&& docker image prune -f \
	&& docker container prune -f \
	&& :
