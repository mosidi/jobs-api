

# Job Posting API

Welcome to the Job Posting API project, a RESTful service designed to facilitate job listings and applications. Built with FastAPI, this project leverages its speed, lightweight nature, and asynchronous capabilities to provide a highly efficient and scalable solution for job boards.

## Features

- **CRUD Operations**: Full Create, Read, Update, and Delete capabilities for job listings.
- **Authentication and Authorization**: Secure access control using modern authentication and authorization mechanisms.
- **Database Operations**: Utilizes SQLAlchemy for robust database management and operations.
- **Integration Testing**: Comprehensive integration testing using Pytest to ensure reliability and functionality.
- **Dockerization**: Containerized application deployment for enhanced portability and scalability.
- **CI/CD Pipelines**: Automated Continuous Integration and Continuous Deployment pipelines using GitHub Actions, with deployment strategies for AWS Lambda and AWS ECS for seamless scaling and management.
- **Routing and Versioning**: Organized endpoint routing and API versioning to enhance maintainability and support future expansions.
- **Applicants and Candidatures Process Management**: Manages the entire lifecycle of job applications and candidate selection.

## Upcoming Improvements

- **Separating Operations Tests from DB Operations Tests**: Refining the testing suite to better distinguish between API logic tests and database interaction tests.
- **Database Caching**: Implementing caching at the database level to improve response times and reduce load.
- **API Caching**: Adding caching mechanisms for frequently requested data to enhance performance.
- **Synchronous Endpoints**: Introducing synchronous handling where it fits better, to optimize performance and resource management.
- **Pagination**: Implementing pagination for API requests to manage large datasets effectively.
- **Complex Searching**: Enhancing the search capabilities to support more complex queries, improving user experience.
- **Data Parsing and Validation**: Strengthening data parsing and validation to ensure accuracy and reliability of the data exchanged with the API.

## Project Structure

```

├── core
├── db
├── main.py
├── requirements-lambda.txt
├── requirements.txt
├── routing
├── schemas
├── sql_app.db
└── tests

```

## Getting Started

Follow these instructions to get the Job Posting API up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Python 3.8+
- pip

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/mosidi/jobs-api/.git
cd job-api
```

2. **Environment Setup**

- For local development without Docker:

```bash
python -m venv venv
source venv/bin/activate  # For Windows use `.\venv\Scripts\activate`
pip install -r requirements.txt
```

- With Docker:

```bash
docker build -t job-posting-api .
docker run -d --name job-posting-api -p 8000:8000 job-posting-api
```

3. **Running the Application**

- Without Docker:

```bash
uvicorn main:app --reload
```

- With Docker, use the previous `docker run` command.

The API will be available at `http://127.0.0.1:8000`.

## Testing

To run integration tests:

```bash
pytest
```

## Deployment

This project is equipped with GitHub Actions workflows for CI/CD, facilitating automatic deployment to AWS Lambda and AWS ECS. Refer to the `.github/workflows` directory for the CI/CD pipeline configurations.

## Contributing

Contributions are welcome! Please fork the repository, create your feature branch, commit your changes, and open a pull request.
