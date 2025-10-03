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
