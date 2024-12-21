from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todo')
def todo_list():
    return render_template('todo.html')

@app.route('/dashboard')
def tracking_dashboard():
    return render_template('dashboard.html')

@app.route('/mypage')
def my_page():
    return render_template('mypage.html')

if __name__ == '__main__':
    app.run(debug=True)
