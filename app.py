from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    os.system('python3 controller.py')
    return 'Script executed!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
