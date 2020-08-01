from sshtunnel import open_tunnel
from time import sleep
import threading
import time
import ssl
import sys

fname = None
fipp = None
publicipadress = ('194.247.184.169', 3232)
setstatus = None

def sshtunconnect(address):
     with open_tunnel(
         publicipadress,
         ssh_username="dgh",
         ssh_pkey="srv.key",
         remote_bind_address=address,
         local_bind_address=('localhost', 2222)
     ) as server:
         print(server.local_bind_port)
         while True:
             # press Ctrl-C for stopping
             sleep(5)

def sshtungetip():
      import kerio.kerio as kerio
      import kerio.keriofunction as kf
      from sshtunnel import SSHTunnelForwarder
      funame = None
      server = SSHTunnelForwarder(
          publicipadress,
          ssh_username="dgh",
          ssh_pkey="srv.key",
          remote_bind_address=('192.168.41.1', 4081),
          local_bind_address=('127.0.0.1', 4081)
      )
      server.start()
      print(server.local_bind_port)
      time.sleep(3)
      login = 'Потапов'
      global setstatus
      setstatus = "Получение ip адреса"
      print(setstatus)
      session = kerio.callMethod("Session.login", {"userName": kerio.username, "password": kerio.password,"application": {"vendor": "Kerio", "name": "Control Api Demo", "version": "8.4.0"}})
      token = session["result"]["token"]
      for funame, fip in kf.findinfo_connection(token, login):
          sleep(1)
      kf.keriologout()
      server.close()
      global fname, fipp
      if funame is None:
            print("Имя пользователя не найдено среди активных подключений")
            fname = "Не найдено"
            return
      time.sleep(2)
      fname, fipp = funame, fip
      print(fname,fipp)
      return


def connecttopc():
    while True:
        n = 5
        if fname == "Не найдено":
            n += 5
            sleep(n)
            break
        if fipp:
            address = (fipp, 3389)
            sshtunconnect(address)
            print('doing work...')
            sleep(3)
            break


def connecting():
    tun = (
        threading.Thread (target=sshtungetip, daemon=True),
        threading.Thread (target=connecttopc, daemon=True)
    )
    for thread in tun:
        thread.start()
