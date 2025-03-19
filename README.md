This project is a lightweight analytics server built with FastAPI and SQLite to collect and analyze event data from users. 
It provides endpoints to log user events and retrieve reports based on a time range. 
A parallel request sender script (parallel_postman.py) is included to simulate high-load event processing. 
The project can be containerized using Docker for easy deployment.
The server exposes two main endpoints:
/process_event - Logs user events with a timestamp.
/get_reports - Retrieves all events for a specific user within a given time period.
The parallel_postman.py script sends multiple concurrent requests to test performance using Joblib. 
The Dockerfile sets up the application in a lightweight Python container, making it ready for cloud deployment. 
The project relies on FastAPI, SQLite, Requests, Joblib, and Uvicorn.
