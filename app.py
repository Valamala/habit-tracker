from flask import Flask, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/add_habit', methods=['POST'])
def add_habit():
    habit_name = request.form.get('habit_name')
    weekly_goal = request.form.get('weekly_goal')
    
    if habit_name and weekly_goal:
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('INSERT INTO habits (name, goal, created_date) VALUES (?, ?, ?)',
                  (habit_name, int(weekly_goal), datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
    
    return redirect(url_for('home'))
