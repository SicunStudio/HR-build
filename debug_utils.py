"""
    Debugger Assistant module for AUHR-HUST
"""

import datetime

from flask import session, jsonify
from main import app

############ Logger ############
def printLog(content):
    """
    Print log message in Python console.
    :param content: Message text you want to log.
    :return:
    """
    currentTime = datetime.datetime.now().isoformat("-")
    print("[LOG] [ %s ]\t %s" % (currentTime, content))

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



