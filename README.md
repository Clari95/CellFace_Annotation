# CellPhaser

### Running the project (for development)

With Docker :whale: installed, run:

```
docker-compose up
```

- Starts the ```frontend``` and ```backend``` containers, respectively for the frontend/vue server and the API server.


### Running the production set-up
> Docker images are tagged with ```master``` or ```dev``` (use ```<user>/<image>:<tag>```)

Starting the frontend server:
```sh
docker pull cellphaser/frontend:dev
docker run -d -p 80:8080 cellphaser/frontend:dev
```
- ```-d``` flag runs the container instance in detached mode
- ```-p 80:8080``` flag maps the container port 8080 to the host port 80 (default HTTP port)
- **TODO**: set backend server url (probably through an environment variable)


Starting the backend server (possibly on another — more powerful — machine):
```sh
docker pull cellphaser/backend:dev
docker run -d -p 3000:8000 cellphaser/backend:dev
```

## Deployment
> what to do, what to change

* change the backend API URL in ```frontend/.env```
* create a ```.env``` file in backend, following the template in ```.env.example```
  - generate a secret key
  - set DEBUG to 0 (false) or 1 (true)
  - change the MEDIA_ROOT
  - change the FRONTEND_URL (for the CORS security policy);
