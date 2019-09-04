import os

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def project_path(*parts):
  return os.path.join(PROJECT_DIR, *parts)