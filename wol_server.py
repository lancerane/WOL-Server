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

def run_bash(command_list):
  return subprocess.run(
    command_list, 
    shell=False, 
    close_fds=True, 
    capture_output=True
  )

@route(ENTRYPOINT)
def index():

  commands = {
    '(1) load driver' : ['sudo', 'modprobe', '-i', 'enc28j60'],
    '(2) wait' : ['sleep', '5'], #this has to be quite long
    '(3) send magic packet' : ['sudo', 'etherwake', '-i', INTERFACE, MAC_ADDRESS],
    '(4) wait again' : ['sleep', '1'],
    '(5) unload driver' : ['sudo', 'modprobe', '-r', 'enc28j60']
  }

  for command_str in list(commands.keys()):
    result = run_bash(
      commands.get(command_str))

    # If there was an error, we assume the traceback was printed to stderr
    if result.returncode != 0:
      return template(
        '<b>There was an error with step {{command}}:\n{{error}}</b>!', 
        command=command_str,
        error=result.stderr.decode("utf-8")
      )

  return '<b>Magic packet sent</b>'

@get('/media/:path#.+#')
def server_static(path):
  return static_file(path, root=ROOT_DIR)

@get('/favicon.ico')
def get_favicon():
  return server_static('favicon.ico')

run(host=HOST, port=PORT)
