from Details.SQLCode import CREATE_USER, CREATE_DATABASE

import mysql.connector as sql


def main():
  with sql.connect(user="root", unix_socket="/var/run/mysqld/mysqld.sock") as database:
    with database.cursor() as cursor:
      cursor.execute(CREATE_USER)
      while cursor.nextset():
        pass

      cursor.execute(CREATE_DATABASE)
      while cursor.nextset():
        pass

  print('Database set successful')

if __name__ == '__main__':
  main()
