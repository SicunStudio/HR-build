"""
    Debugger Assistant module for AUHR-HUST
"""

import datetime

from flask import session, jsonify
from starter import app

############ Logger ############
def printLog(content):
    """
    Print log message in Python console.
    :param content: Message text you want to log.
    :return:
    """
    currentTime = datetime.datetime.now().isoformat("-")
    print("[LOG] [ %s ]\t %s" % (currentTime, content))

def printErrTraceback(title, exception):
    """
    Print error traceback in Python console when catching exceptions.
    :param title: The action name you want to tag where traceback should be logged.
    :return:
    """
    currentTime = datetime.datetime.now().isoformat("-")
    print("[ERROR] [ %s ] [ %s ]\t %s" % (title, currentTime, exception.args[0]))


######## Notification utils #########
@app.route('/clear_flash/', methods=['GET', 'POST'])
def clear_flash_messages():
    """
    Clear flash message stack through an URL in front-end page.
    This URL is AJAX-ive.
    :return: JSON info with log message.
    """
    print(session)
    if '_flashes' in session:
        session.pop('_flashes')
        return jsonify(result={'msg': 'Flash messages cleared'})
    else:
        return jsonify(result={'msg': 'No flash message yet'})
