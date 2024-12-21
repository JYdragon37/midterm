from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  # home.html 렌더링

@app.route('/1')
def page_one():
    return render_template('page1.html')  # page1.html 렌더링

@app.route('/2')
def page_two():
    return render_template('page2.html')  # page2.html 렌더링

if __name__ == '__main__':
    app.run(debug=True)
