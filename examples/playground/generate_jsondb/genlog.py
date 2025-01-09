import json
import os
from datetime import datetime


def load_log():
  if os.path.exists("generate_log.json"):
    with open("generate_log.json", "r") as f:
      generate_log = json.load(f)
  else:
    generate_log = []
  return generate_log


generate_log = load_log()


def new_log(name):
  """create a new log, but not write to file"""
  log = {"time": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), "name": name}
  return log


def write_log(log):
  generate_log.append(log)
  with open("generate_log.json", "w") as f:
    json.dump(generate_log, f)


def get_latest_name():
  if len(generate_log) == 0:
    return None
  return generate_log[-1]["name"]
