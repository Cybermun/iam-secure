reset:
	docker compose down -v
	docker compose up --build

push:
	git add .
	git commit -m "Update"
	git push
