from flask import Flask, render_template

# Step 1: Initialize Flask app
app = Flask(__name__)

# Step 2: Home route
@app.route('/')
def home():
    return render_template('index.html')

# Step 3: Run the app
if __name__ == '__main__':
    app.run(debug=True)
