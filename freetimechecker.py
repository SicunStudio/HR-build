from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/old')
def page_old():
    return render_template('old_style_with_table.html')

if __name__ == '__main__':
    app.run(debug=True)
