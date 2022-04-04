from bottle import route, get, run, template, static_file
import os, subprocess, time
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
    'load_driver' : ['sudo', 'modprobe', '-i', 'enc28j60'],
    'sleep' : ['sleep', '0.2'],
    'send_magic_packet' : ['sudo', 'etherwake', '-i', INTERFACE, MAC_ADDRESS],
    'sleep_again' : ['sleep', '1'],
    'unload_driver' : ['sudo', 'modprobe', '-r', 'enc28j60']
  }

  for command in list(commands.values()):
    result = run_bash(command)

    # If there was an error, we assume the traceback was printed to stderr
    if result.returncode != 0:
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
