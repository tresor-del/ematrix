# eMatrix

## Introduction

This is a task management web application based on the Eisenhower matrix, designed to help users prioritize and organize their tasks and projects efficiently.

---

## Distinctiveness and Complexity

### Distinctiveness

This project satisfies the distinctiveness requirement because it is not a simple clone of common projects like a blog or a to-do list. Instead, it introduces a unique feature set, such as:

- **Integration of the Eisenhower Matrix:** A decision-making framework for prioritizing tasks based on urgency and importance.
- **User-specific analytics:** Visual feedback on productivity and time management trends.

### Complexity

This project meets the complexity requirement due to:

1. **Advanced Backend Logic**: Includes custom models and queries to handle relationships between users, tasks, notifications, and projects.
2. **Dynamic Frontend**: Utilizes JavaScript for real-time updates, drag-and-drop functionality, and AJAX requests.
3. **Third-party Integrations**: Incorporates additional tools and APIs, such as charts for data visualization or authentication using social login.

---

## File Structure

### Main Files and Their Purposes

#### `models.py`

Defines the database schema, including:

- **CustomUser**: Extends Django's User model to support additional user fields.
- **Task**: Represents tasks with fields for urgency, importance, deadlines, etc.

#### `views.py`

Contains the core application logic, such as:

- Handling CRUD (Create, Read, Update, Delete) operations for tasks .
- Sending JSON responses for AJAX requests.
- Managing user authentication and authorization.
- Rendering templates with context data.

#### `urls.py`

Maps URLs to their corresponding views, defining the routing of the application.

#### `templates/`

Holds HTML templates for the app’s frontend. Includes templates for:

- Task creation and management.
- Eisenhower matrix visualization.
- User dashboards.
- User authentication (login, registration, etc.).

#### `static/`

Contains CSS, JavaScript, and image assets used for styling and interactivity. This includes:

- Custom stylesheets for the application.
- JavaScript files for dynamic behaviors and AJAX requests.
- Images and icons used in the UI.

#### `requirements.txt`

Lists Python dependencies required to run the project. This ensures that all necessary packages are installed in the virtual environment.

#### `README.md`

Documentation about the project (this file). It provides an overview, distinctiveness and complexity details, file structure, setup instructions, and additional information.

---

## How to Run the Application

### Prerequisites

Ensure you have the following installed:

- Python 3.9+
- pip (Python package manager)
- A virtual environment manager (optional but recommended)

### Steps

1. **Set Up a Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run Migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Start the Development Server**:

    ```bash
    python manage.py runserver
    ```

5. **Access the Application**:
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Additional Information

### Custom Features

- **Drag-and-Drop Task Management**: Users can drag tasks between quadrants of the Eisenhower matrix.
- **Dark mode**: Users can toggle between light and dark modes using a button in the UI.

### Third-Party Libraries

- **Chart.js**: Used to create data visualizations and analytics.

### Testing

To run the test suite, use:

```bash
python manage.py test
```