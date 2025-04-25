
# NBA Ticket Booking System

This is a web-based NBA ticket booking system where users can view available shows, add tickets to their cart, and make bookings. It also includes an admin panel for managing shows and user bookings. The project uses Django for backend development and Docker for containerization.

## Features

- **User Registration and Authentication**: Users can register and log in to their accounts.
- **Show Management**: Admins can create, update, and manage shows.
- **Ticket Booking**: Users can add shows to their cart and proceed to checkout to book tickets.
- **Booking History**: Users can view their booking history.
- **Cart Management**: Users can add or remove shows from their cart.
- **Responsive Design**: The website is fully responsive and works well on both desktop and mobile devices.

## Technologies Used

- **Django**: Python web framework used for building the backend.
- **PostgreSQL**: Used as the database for storing user and show data.
- **Docker**: For containerization and easier environment setup.
- **Jenkins**: For CI/CD automated build, test, and deployment.
- **HTML, CSS (with external styling)**: Frontend technologies for building the user interface.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Docker and Docker Compose
- PostgreSQL (or any other compatible database)
- Jenkins (for CI/CD setup)

## Setting Up the Project Locally

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/yourusername/nba_ticket_booking.git
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Navigate to the project folder and create a virtual environment:

```bash
cd nba_ticket_booking
python -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install the Required Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Make sure PostgreSQL (or your database of choice) is running, and then apply the migrations:

```bash
python manage.py migrate
```

### 5. Run the Development Server

You can run the Django development server with:

```bash
python manage.py runserver
```

Now you can access the application at `http://127.0.0.1:8000/`.

### 6. (Optional) Using Docker

If you'd prefer to use Docker for setting up the environment, you can use the following steps:

- Build the Docker image:

```bash
docker-compose up --build
```

- Start the containers:

```bash
docker-compose up
```

### 7. Accessing the Admin Panel

If you're an admin, you can access the  admin panel at `http://127.0.0.1:8000/`. You'll need to create a superuser and login if you haven't done so already:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin user.

## Jenkins CI/CD Setup

1. **Install Jenkins**: Set up Jenkins on your local machine or server.
2. **Create a Jenkins Job**: Create a Jenkins pipeline job to automate the build, test, and deploy process.
3. **Set up GitHub Integration**: Connect your GitHub repository to Jenkins using the GitHub plugin.
4. **Configure Jenkinsfile**: Add a `Jenkinsfile` to your repository for defining the pipeline stages (build, test, deploy).

For a more detailed setup, refer to the official [Jenkins Documentation](https://www.jenkins.io/doc/).
## Screenshots
![Screenshot 2025-04-25 202831](https://github.com/user-attachments/assets/7579b309-c097-4898-8f14-2dbd0016b153)
![Screenshot 2025-04-25 202855](https://github.com/user-attachments/assets/0ebf669b-45e2-42ba-9a73-8a41cc3d8e15)
![Screenshot 2025-04-25 203049](https://github.com/user-attachments/assets/be3cc0c1-d82e-4d2a-a860-0eed72c2575d)
![Screenshot 2025-04-25 203107](https://github.com/user-attachments/assets/03315a81-d056-4d9d-b37b-c00f7879c810)


## Deployment

The application can be deployed using any web server that supports Django, such as **Gunicorn** or **uWSGI**, with **Nginx** as a reverse proxy. You can also deploy it to cloud platforms such as **Heroku**, **AWS**, or **DigitalOcean**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community for providing the tools and resources to build this application.
- Special thanks to the contributors of the libraries used in this project.

