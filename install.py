#!/usr/bin/python3

import os

def UpdateWith(rc_path: str, rc_name: str) -> None:
  with open(rc_path, 'a+') as rc:
    rc.seek(0)
    add_exec = f"export PATH=\"{os.path.dirname(os.path.abspath(__file__))}:$PATH\""
    if add_exec not in rc.read():
      rc.write('\n' + add_exec + '\n')
      print(f"{rc_name} has been updated.")


def main():
  user_path = os.path.expanduser('~')

  bashrc_path = os.path.join(user_path, '.bashrc')
  if os.path.isfile(bashrc_path):
    UpdateWith(bashrc_path, '.bashrc')
  
  zshrc_path = os.path.join(user_path, '.zshrc')
  if os.path.isfile(zshrc_path):
    UpdateWith(zshrc_path, '.zshrc')
  print('Install successful')

if __name__ == '__main__':
  main()
