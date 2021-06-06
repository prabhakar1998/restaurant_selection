
# Usage
### Prerequisites
- Install `docker` and `docker-compose`.
### Setup code
- Clone the project using 
	```git clone https://github.com/prabhakar1998/restaurant_selection.git```
### Setup docker container
- In the root directory run command `make build`. This builds and starts the app.
- Enter an interactive session on the container  by running `make container` to create super user, run tests and migrate db in the container.
     - Apply migrations  by running `make migrate`
     - Create super user by running `make createsuperuser`
     - Run the tests by running `make test` .
     - Run the development server by running `make run` 
### API Doc 
- To view API doc and use REST API endpoints, Open `http://localhost:8000` in browser and 
   check swagger UI page.
  which can be used to  call REST API endpoints.
- Login with the super user credentials. Use all the API end points using `Try it out`
