from flask import Flask, render_template, redirect, url_for, session, jsonify
import os
import time
import threading
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Global variables
machine_in_use = False
current_user_session = None
user_active_time = None
timeout_duration = 30
timeout_occurred = False  # Flag to indicate if a timeout has occurred

# Function to release the machine lock after the timeout
def release_lock_after_timeout():
    global machine_in_use, user_active_time, current_user_session, timeout_occurred
    while True:
        if machine_in_use and time.time() - user_active_time > timeout_duration:
            print("Timeout reached. Releasing machine lock.")
            machine_in_use = False
            current_user_session = None
            timeout_occurred = True  # Set the timeout flag
        time.sleep(1)

# Start a background thread to monitor the timeout
threading.Thread(target=release_lock_after_timeout, daemon=True).start()

# Background function to run the servo control script
def run_servo_script():
    os.system('python3 test.py')  # Replace 'test.py' with your actual script path

@app.route('/')
def home():
    global machine_in_use, timeout_occurred  # Include timeout_occurred
    if timeout_occurred:
        # Reset the timeout flag when accessing the home page
        timeout_occurred = False

    if machine_in_use:
        return render_template('index.html', in_use=True)
    else:
        return render_template('index.html', in_use=False)

@app.route('/run-script', methods=['POST'])
def run_script():
    global machine_in_use, user_active_time, current_user_session, timeout_occurred
    
    # Check if the machine is already in use
    if machine_in_use:
        return redirect(url_for('home'))
    
    # Lock the machine for this user session
    machine_in_use = True
    user_active_time = time.time()
    
    # Generate a unique session ID if one doesn't exist
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    # Store the current session controlling the machine
    current_user_session = session['user_id']

    # Start the servo control script in a background thread
    threading.Thread(target=run_servo_script, daemon=True).start()

    # Immediately redirect to the control page after starting the script
    return redirect(url_for('control_page'))

@app.route('/control')
def control_page():
    global machine_in_use, current_user_session, timeout_occurred
    
    # Check for timeout before checking machine state
    if timeout_occurred:
        timeout_occurred = False  # Reset the flag when accessing the control page
        return redirect(url_for('home'))  # Redirect to the home page if timeout occurred
    
    # Check if the machine is in use and if the current session matches the user who started it
    if not machine_in_use or session.get('user_id') != current_user_session:
        return redirect(url_for('home'))
    
    # Render the control page if the session matches
    return render_template('control.html')

@app.route('/release-machine', methods=['POST'])  # Ensure this is a POST request
def release_machine():
    global machine_in_use, current_user_session
    
    # Only allow the session that locked the machine to release it
    if session.get('user_id') == current_user_session:
        machine_in_use = False
        current_user_session = None
        return redirect(url_for('home'))
    
    return "You are not authorized to release the machine.", 403

@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the machine."""
    return jsonify({
        'machine_in_use': machine_in_use,
        'timeout_occurred': timeout_occurred
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
