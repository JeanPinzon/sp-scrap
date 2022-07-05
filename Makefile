run_ycombinator:
	docker build -t sp-scrap .
	docker run --env YCOMBINATOR_COOKIES="${YCOMBINATOR_COOKIES}" --env MONGO_URI="${MONGO_SP_SCRAP}" sp-scrap scrapy crawl ycombinator