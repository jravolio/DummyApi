# Dummy API Project

This is a sample project that provides a simple API hosted at [dummyapi.devjravolio.com](https://dummyapi.devjravolio.com). The API offers access to dummy data and can be used for testing and development purposes. This project was built using Docker and Flask

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Overview

The Dummy API Project aims to provide a set of dummy data accessible through a RESTful API. It's particularly useful for testing and developing applications that require sample data. The API offers various endpoints to retrieve, create, update, and delete data.

## Usage

The API is publicly accessible at [dummyapi.devjravolio.com](https://dummyapi.devjravolio.com). You can use any HTTP client or tools like `curl` to interact with the API.

**Example:** Retrieving data for a user named "john_doe":

```shell
curl https://dummyapi.devjravolio.com/data/john_doe
```

You can use any username you want! Remember that the data will persist for a **LIMITED** time.

## Endpoints
The API provides the following endpoints:
```
GET /data/<username>: Retrieve data for a specific user or register a new user.
GET /data/<username>/<id>: Retrieve data by ID.
POST /data/<username>: Create new data for a user.
PUT /data/<username>/<id>: Update data by ID.
DELETE /data/<username>/<id>: Delete data by ID.
```

## Getting Started
Clone this repository:

```bash
git clone https://github.com/your-username/dummy-api-project.git
Navigate to the project directory:
```

Move to the folder of the project.
```bash
cd dummy-api-project
```
Install the required dependencies.
```bash
pip install -r requirements.txt
```
Run the application:
```bash
python run.py
```

After that, you can access the API at http://localhost:5003.

## Contributing
Contributions are welcome! If you find a bug or have suggestions for improvements, feel free to open an issue or submit a pull request. This is a hobby project, don't be afraid of recommending code suggestions.
