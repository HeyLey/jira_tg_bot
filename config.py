import os

# webhook
URL = os.environ.get('URL')
PORT = int(os.environ.get('PORT', '5000'))

# telegram
TOKEN = os.environ.get('TOKEN')

USER_ID = os.environ.get('USER_ID')

JIRA_TOKEN = os.environ.get('JIRA_TOKEN')

JIRA_URL = os.environ.get('JIRA_URL')
