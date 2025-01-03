detail-tracking-app-api

# **User Management API**

This is a Python (Django) backend project that provides a user management system with endpoints to manage users, albums, photos, posts, comments, and todos. The API supports basic CRUD operations, as well as additional features such as filtering incomplete todos and posts.

**Installation**          
**Prerequisites**        
Python 3.x         
Docker (for containerization)               
Docker Compose (for managing multi-container applications)            
PostgreSQL (optional, but recommended)       

git clone https://github.com/parzival-au20/detail-tracking-app-api         
cd  detail-tracking-app-api        

Build and start the application using Docker Compose:         

docker-compose up --build            
This will build the Docker images and start the application and database containers. It also links the db container (PostgreSQL) to the app container (Django app).          

The application will be accessible at http://localhost:8000.           

**Configuration**       
The Docker Compose setup defines the following services:            

app: This service runs the Django application, listens on port 8000, and automatically runs database migrations and starts the Django development server.
db: This service runs a PostgreSQL database instance with the necessary environment variables (DB_HOST, DB_NAME, DB_USER, DB_PASS) for connecting to the database.
You can customize the database configuration in the docker-compose.yml file under the environment section for the app and db services.

**Running the Application**        
Build and start the containers using Docker Compose:          

docker-compose up --build              
Wait for the containers to start. The app container will automatically wait for the database to be ready, run migrations, and then start the Django development server.            

The application will be available at http://localhost:8000.            
      
**Testing**          
You can test the API endpoints using tools such as Postman or Swagger.

**License**        
This project is licensed under the MIT License - see the LICENSE file for details.
