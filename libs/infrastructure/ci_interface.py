__author__ = 'toure'

import jenkins

server = jenkins.Jenkins('localhost:8080', username='myuser', password='mypassword')
version = server.get_version()
print version