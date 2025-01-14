
---
# DocBook - Doctor Appointment Booking System

## Overview
DocBook is a Django-based web application that allows patients to book appointments with doctors. It provides an intuitive platform for managing doctor schedules and patient bookings, offering seamless workflows for both parties.

## Features
- **User Authentication**: Patients can log in and manage their appointments.
- **Search Doctors**: Dynamic search functionality to find doctors by name or specialization.
- **View Doctor Schedules**: Patients can view available time slots and select a convenient one.
- **Appointment Management**: Patients can book, view, and confirm their appointments.
- **REST API**: Integrated API endpoints for searching doctors and managing data.

## Main Workflows

### Patient Workflow
1. **Login/Registration**:
   - Users can sign in or register using the registration form.
   - Registered users can manage appointments via the dashboard.
     ![alt text](DocBook/screenshots/login.png)

2. **Search Doctors**:
   - Search by name or specialization using the search bar on the dashboard.
   - Results display dynamically without reloading the page.
     ![alt text](DocBook/screenshots/search.jpg)

3. **View Doctor Schedule**:
   - Click on a doctor from the search results to view their available time slots.
     ![alt text](DocBook/screenshots/viewschedule.png)

4. **Book Appointment**:
   - Select a time slot and confirm the appointment.
   - Notifications display the booking status.
     ![alt text](DocBook/screenshots/notification.png)
   - Slots are color-coded:
     - **Green**: Available
     - **Red**: Taken
     - **Blue**: Reserved by the user
       ![alt text](DocBook/screenshots/schedule.png)

5. **Dashboard Management**:
   - View all appointments with details (doctor, date, status).
     ![alt text](DocBook/screenshots/appointments.png)

### Admin Workflow
- Admin login page.
  
   ![alt text](DocBook/screenshots/adminlogin.png)

- Admin users can manage doctors, appointments, and other related data through the Django admin panel.
  
   ![alt text](DocBook/screenshots/adminpanel.png)

## API Endpoints
- **Search Doctors**: `/api/doctors/search/`
  - Accepts query parameters (`q`) for searching by name or specialization.
  - Returns JSON data with matching doctors.

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication system

## Running the Project with Docker

### Prerequisites
To run this project, you need Docker installed and running on your system.

### Steps to Run the Project
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shimamousavian/DocBook.git
   cd DocBook
   ```
2. **Create a .env file in the root of the project (the directory that includes Dockerfile)**:
   - Open the .env file and configure the following variables according to your preferences:
   ```bash
   # Example .env configuration
   DATABASE_NAME=docbook           # Name of the PostgreSQL database
   DATABASE_USER=admin             # Database username
   DATABASE_PASSWORD=password      # Database password
   DATABASE_HOST=db                # Hostname for the database container
   DATABASE_PORT=5432              # Port for connecting to the database
   DEBUG=1                         # Debug mode (set to 0 for production)

   ```

3. **Build and Start the Docker Containers**:
   ```bash
   docker-compose up --build -d
   ```

4. **Run Migrations**:
   - Initialize the database schema.
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Superuser**:
   - Set up an admin user to access the admin panel.
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the Application**:
   - Open your browser and go to `http://localhost:8000/`.
   - Admin panel is accessible at `http://localhost:8000/admin/`.

7. **Stopping the Project**:
   - To stop and remove the containers:
   ```bash
   docker-compose down
   ```

---
