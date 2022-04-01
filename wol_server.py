# A lightweight webserver to run permanently on the Pi as a systemd service - wol_server.service - in /lib/systemd/system/
# Enabled with sudo systemctl enable wol_server.service
# Requests trigger the sending of the magic packet.
# Any errors are returned

from bottle import route, get, run, template, static_file
import os, subprocess
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('PORT'))
INTERFACE = os.getenv('INTERFACE')
MAC_ADDRESS = os.getenv('MAC_ADDRESS')
ROOT_DIR = os.getenv('ROOT_DIR')
HOST = os.getenv('HOST')
ENTRYPOINT = os.getenv('ENTRYPOINT')

@route(ENTRYPOINT)
def index():
  result = subprocess.run(
    ['sudo', 'etherwake', '-i', INTERFACE, MAC_ADDRESS], 
    shell=False, 
    close_fds=True, 
    capture_output=True
  )

  if result.returncode != 0:
  # if there was an error, we assume the traceback was printed to stderr
    return template(
      '<b>There was an error:\n\n{{error}}</b>!', error=result.stderr.decode("utf-8")
    )
  return '<b>Magic packet sent</b>'

@get('/media/:path#.+#')
def server_static(path):
  return static_file(path, root=ROOT_DIR)

@get('/favicon.ico')
def get_favicon():
  return server_static('favicon.ico')

run(host=HOST, port=PORT)
