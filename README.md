# eMatrix

## Introduction

This is a task management web application based on the Eisenhower matrix, designed to help users prioritize and organize their tasks and projects efficiently.

---

## Distinctiveness and Complexity

This project clearly satisfies the distinctiveness requirement because it does not replicate simple, commonly found applications such as blogs or to-do lists. Instead, it introduces a unique and practical approach to task management by leveraging the Eisenhower Matrix, a renowned time management tool. This matrix allows users to prioritize their tasks based on urgency and importance, offering a clearer and more strategic method of handling daily responsibilities.

Beyond task prioritization, the app incorporates several advanced features that set it apart. It integrates visual feedback systems to help users track their productivity and time management trends over time. This feature encourages more informed decision-making by providing an overview of past activity, which can motivate users to refine their habits.

The app also uses the `allauth` library for seamless user authentication and social login via Google, ensuring that users have a smooth onboarding experience. The Google Cloud API further enhances this by simplifying the authentication process and providing secure, reliable management of user data.

In terms of interactivity, the app leverages JavaScript to enable real-time updates, drag-and-drop functionality for task management, and AJAX requests to keep the user experience fluid and responsive without unnecessary page reloads. These dynamic interactions add to the app’s sophistication and make it stand out from simpler, static applications.

Moreover, the app incorporates tools and APIs for rich data visualization. Chart.js is used to graphically display productivity statistics, providing users with an immediate understanding of their performance trends. Users can also export their tasks to CSV or PDF formats, offering flexibility for offline use and external data management.

Overall, this project stands out not just because it is different, but because it successfully combines multiple advanced features—task prioritization, real-time interaction, data visualization, and easy data export—into a single, cohesive application. The integration of these elements, each requiring a thoughtful approach to both development and user experience, significantly raises the complexity and impact of the project.


## File Structure

**main.css** : This CSS file defines global styles for the application, including CSS variables, responsive design rules, and animations to enhance the user experience across different screen sizes.

**profile.css** : This CSS file is dedicated to styling the profile page, handling elements like layout, images, buttons, and responsiveness to ensure the profile page adapts properly on different devices.

**chart.js** : This JavaScript file is responsible for fetching task data from the server and dynamically rendering it into a doughnut chart. It helps visualize task distribution based on their priority and progress.

**events.js** : This JavaScript file handles the main task management functionalities, including drag-and-drop for task reordering, focus mode for single-task emphasis, and integration with the chart for displaying task statistics in real-time.

**profile.js** : This JavaScript file fetches and displays the user’s profile data in a dynamic modal, allowing users to view and update their profile information without reloading the page.

**layout.html** : This HTML file serves as the layout template for the application, containing links to JavaScript files, CSS files, and other libraries. It also provides the navigation links and a base structure for all other HTML pages in the app.

**chart.html** : This file contains a Bootstrap modal used for displaying the dynamic doughnut chart, providing a visual representation of task data to the user in an interactive format.

**edit_profile.html** : This file contains a Bootstrap modal that allows users to update their personal information, such as their username, email, and profile picture.

**focus_mode.html** : This file contains a Bootstrap modal designed to help users focus on a single task by temporarily hiding all other tasks, promoting productivity and minimizing distractions.

**index.html** : This file is the landing page for new users. It provides an overview of the app, highlighting its features, explaining why the user should use it, and includes a call-to-action to encourage sign-in or sign-up.

**privacy.html** : This page outlines the app's privacy policies, explaining how user data is handled, stored, and protected in compliance with legal standards.

**terms.html** : This file contains the app’s terms and conditions, providing users with an understanding of the rules, responsibilities, and limitations when using the application.

**profile.html** : This page displays the user's personal information in an off-canvas sidebar, offering a quick view of their profile data for easy access and editing.

**tasks.html** : This is the main part of the application, where the Eisenhower Matrix quadrants are displayed. It allows users to manage and organize their tasks based on urgency and importance, helping them focus on what matters most

**login.html**: This file provides the login interface for users. It includes a form with fields for email and password, and a button for signing in via Google OAuth. It should redirect users to the authentication service for Google login.

**signup.html**: This file contains the signup form, where users can create an account by entering their email and password or signing up via Google OAuth.

## How to Run the Application

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

### Testing

To run the tests:
```bash
python manage.py test
```
