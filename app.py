from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS habits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  goal INTEGER NOT NULL,
                  created_date TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS habit_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  habit_id INTEGER,
                  log_date TEXT NOT NULL,
                  completed INTEGER DEFAULT 0,
                  FOREIGN KEY (habit_id) REFERENCES habits(id))''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    
    # Get all habits
    c.execute('SELECT * FROM habits')
    habits = c.fetchall()
    
    # Calculate progress for each habit
    habits_with_progress = []
    for habit in habits:
        habit_id = habit[0]
        goal = habit[2]
        
        # Count completed days in the last 7 days
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        c.execute('''SELECT COUNT(*) FROM habit_logs 
                     WHERE habit_id = ? AND completed = 1 
                     AND log_date >= ?''', (habit_id, week_ago))
        completed_count = c.fetchone()[0]
        
        progress = min(int((completed_count / goal) * 100), 100) if goal > 0 else 0
        
        habits_with_progress.append({
            'id': habit[0],
            'name': habit[1],
            'goal': habit[2],
            'completed': completed_count,
            'progress': progress
        })
    
    conn.close()
    return render_template('index.html', habits=habits_with_progress)

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
    
    return redirect(url_for('index'))

@app.route('/log_habit/<int:habit_id>', methods=['POST'])
def log_habit(habit_id):
    today = datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    
    # Check if already logged today
    c.execute('SELECT * FROM habit_logs WHERE habit_id = ? AND log_date = ?',
              (habit_id, today))
    existing_log = c.fetchone()
    
    if existing_log:
        # Toggle completion
        new_status = 0 if existing_log[3] == 1 else 1
        c.execute('UPDATE habit_logs SET completed = ? WHERE id = ?',
                  (new_status, existing_log[0]))
    else:
        # Create new log
        c.execute('INSERT INTO habit_logs (habit_id, log_date, completed) VALUES (?, ?, ?)',
                  (habit_id, today, 1))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete_habit/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
    c.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)