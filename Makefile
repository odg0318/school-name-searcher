clean:
	@find -name '*.pyc' -exec rm -rf {} \;

migrate:
	@bin/migrate_xlsx_sqlite3 --src=data/schools.xlsx --dest=schools/data/schools.db --force

docker-build: clean
	@docker build -t school-parser:latest .
