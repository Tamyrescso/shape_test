
# Shape data challenge
### Context:
The assignment involves completing a backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading). This system will be used for other applications in the organization and we should have APIs with the appropriate HTTP request methods to be able to reuse them.

### Technical specifications:
- The data should be stored in the database (**Postgres**).
- A skeleton of the application was provided.
- The application was developed in **Python** with **Flask**.
- It uses the ORM **SQLAlchemy**.
- The **Swagger** is used through **Flasgger**.
- The application is containerized with **Docker**.
- The tests were written using **Pytest**.

![tests coverage](https://github.com/Tamyrescso/images_projects/blob/master/tests-coverage-shape-challenge.png)


### Necessary to run the project:

To run this project is necessary to have docker and docker-compose

Links to install:

-   Docker:  [https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
-   Docker-compose:  [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Running the project:

The docker will create the DB and up the project

-   Command to run: **docker-compose up**

As all is executed the DB will be created and the project will be running.

### Executing the endpoints:
The endpoints can be acessed by:

- [http://localhost:5000](http://localhost:5000) through any API platform.
- [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) to execute the endpoints using the documentation of swagger.

### Endpoint details:
- **GET** `/`:
It is the system healtcheck.
- **POST** `/vessel/insert_vessel`:
Insert a new vessel in the database, returns an `"OK"` message if everything works as expected.
- **POST** `/equipment/insert_equipment`:
Insert a new equipment in the database, returns an `"OK"` message if everything works as expected.
- **PUT** `/equipment/update_equipment_status`:
Change the status of one or several equipments to INACTIVE. Returns an `"OK"` message if everything works as expected.
- **GET** `/equipment/active_equipments`:
Returns a list of active equipments according to the vessel_code which was provided.
Response example:

	```
    [
      {
        "active": True,
        "code": "531df345",
        "id": 3,
        "location": "china",
        "name": "compressor",
      }
    ]
	```
- **GET** `/equipment/list_equipments`:
Returns a list of equipments according to the name that was provided and shows which vessel it belongs.
Response example:

	```
    [
      {
        "equipments_compressor": [
          {
            "active": False,
            "code": "5310B9D7",
            "id": 1,
            "location": "brazil",
            "name": "compressor",
          },
          {
            "active": True,
            "code": "531df345",
            "id": 3,
            "location": "china",
            "name": "compressor",
          },
        ],
        "vessel_code": "MV102",
      },
      {
        "equipments_compressor": [
          {
            "active": False,
            "code": "531dfddf",
            "id": 2,
            "location": "china",
            "name": "compressor",
          }
        ],
        "vessel_code": "MV101",
      },
    ]
	```

