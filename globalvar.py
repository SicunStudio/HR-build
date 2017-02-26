'''
  here stores all the file path configurations
'''

import os




HR_SYSTEM_ROOT = os.path.split(os.path.realpath(__file__))[0]

SSL_CONTEXT_ROOT = os.path.join(HR_SYSTEM_ROOT, "ssl")

FOLDER = os.path.join(HR_SYSTEM_ROOT, 'score-sheets')  # xlsx location
INVENTORY = os.path.join(FOLDER, 'inventory.db')
DATABASE = os.path.join(HR_SYSTEM_ROOT, 'data.db')  # db loaction

SALT = 'do_not_change_me!!!'
INVITATION = 'you may want to change this regularly'




if __name__ == '__main__':
    print(HR_SYSTEM_ROOT, SSL_CONTEXT_ROOT)
    print(FOLDER, INVENTORY, DATABASE)
    print(SALT, INVITATION)
