from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/old')
def page_old():
    return render_template('old_style_with_table.html')

@app.route('/submit_freetime', methods=('GET', 'POST'))
def submit_freetime():
    raw_data = request.form.get('result','')
    print(raw_data)
    return jsonify(backMessage={'message':raw_data})

if __name__ == '__main__':
    app.run(debug=True)
