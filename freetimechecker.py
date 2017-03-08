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
    output=parse_result(raw_data=raw_data)

    return jsonify(backMessage={'message':output})


def parse_result(raw_data):
    result=[]
    weekdays_name = {
        'MON': '周一', 'TUE': '周二', 'WED': '周三', 'THU': '周四', 'FRI': '周五', 'SAT': '周六', 'SUN': '周日'
    }
    lesson_time = raw_data.split(',')
    for item in lesson_time:
        buff=item.split('-', 1)
        day=buff[0]
        time=buff[1]
        result.append("%s %s节" % (weekdays_name[day], time))

    return result


if __name__ == '__main__':
    app.run(debug=True)
