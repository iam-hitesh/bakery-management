# Bakery Management Application

### Project setup

Uses the default Django development server.

1. Rename `.env.example` to `.env`
2. Update the environment(`secret key`) variables in the `.env` file.
3. Build the images and run the containers:

    ```
    docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000).
4. For creating a superuser, so that you can access the dashboard. Use below command
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
5. For API routing check postman collection at `https://www.getpostman.com/collections/0ce7888c61a1f39c8fcd`

*`secret keys` used in `.env.example` file should not use in production's environment.

### Tech stack used
- Docker
- Django/Python
- DRF
- PostgreSQL
