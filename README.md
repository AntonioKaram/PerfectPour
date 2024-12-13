# PerfectPour
TLDR: PerfectPour is the web application that controls and initiates our robot remotely from your mobile phone.

## Overview

The PerfectPour Control System is a web application built using Flask, designed to manage the operation of our pouring machine. The application allows users to activate the machine and control its operation via a simple web interface. It includes functionality to handle multiple user sessions and prevent concurrent access to the machine.

## Architecture

### File Structure

```
.
├── app.py              # Main application file
├── templates
│   ├── index.html      # Home page template
│   └── control.html    # Control page template
└── static
    └── css
        └── styles.css   # CSS styles for the application
```

#### app.py

The `app.py` file contains the core functionality of the application. Key components include:

- **Global Variables**:
  - `machine_in_use`: Tracks whether the machine is currently being operated.
  - `current_user_session`: Stores the session ID of the user controlling the machine.
  - `user_active_time`: Records the time when the user activated the machine.
  - `timeout_duration`: Duration in seconds before a timeout occurs.
  - `timeout_occurred`: Flag indicating whether a timeout has occurred.

- **Threading**:
  - A background thread monitors the timeout duration. If the machine is in use and the user has been active longer than `timeout_duration`, it releases the machine lock.

- **Routes**:
  - `/`: Home page that displays the current status of the machine.
  - `/run-script`: Route to initiate the servo control script and lock the machine for the user.
  - `/control`: Control page that displays when the machine is in use.
  - `/release-machine`: Route to release the machine when the user is done.
  - `/status`: API endpoint to check the machine's current status.

### HTML Templates

#### index.html

The home page template provides users with the option to start the pouring process if the machine is not in use. It includes a button that sends a `POST` request to `/run-script` to initiate the machine's operation.

```html
<form action="/run-script" method="post">
    <button type="submit">Pour Me</button>
</form>
```

A JavaScript function periodically checks the machine's status and reloads the page if the machine becomes available or if a timeout occurs.

#### control.html

The control page notifies the user that the pouring process is active and provides a button to indicate completion. The page also includes a status check that redirects the user back to the home page if the machine is no longer in use or if a timeout occurs.

```html
<form action="/release-machine" method="post">
    <button type="submit">Yes, I'm Done</button>
</form>
```

### CSS Styles

The `styles.css` file contains styles to enhance the appearance of the web application, including styles for the body, headings, buttons, and footer.

## Running the Application

1. Ensure you have Flask installed:
   ```bash
   pip install Flask
   ```

2. Set your secret key as an environment variable:
   ```bash
   export FLASK_SECRET_KEY='your_secret_key_here'
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the web application in your browser at `http://<your_pi_ip>:9000`.
