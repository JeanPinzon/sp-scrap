run:
	docker build -t sp-scrap .
	docker run --env MONGODB_URI="${MONGO_SP_SCRAP}" sp-scrap