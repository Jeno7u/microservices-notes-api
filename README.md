# Start containers
`docker-compose up --build`

# Create migrations inside of container
`docker-compose exec container-name alembic revision --autogenerate -m "Init tables`

# Implement migration to the db
`docker-compose exec container-name alembic upgrade head`