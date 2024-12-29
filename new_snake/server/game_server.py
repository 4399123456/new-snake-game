import signal
import socket,os,time,sys,datetime
from multiprocessing import Process
import pymysql,redis
import setting as st

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

p_ls = []

r_connector = redis.Redis(host=st.redis_db_ip,port=st.redis_db_port,db=st.redis_db_num)
mysql_connector = pymysql.connect(host=st.db_ip, port=st.db_port, user=st.db_user, password=st.db_password,
                                       db='snake')

class Client(Process):
    def __init__(self,client,address):
        super().__init__()
        self.address = address
        self.client = client
        self.cur = mysql_connector.cursor()
        self.data_ls = []
        self.username = None

    def show_main_data(self,user):
        self.username = user
        if r_connector.sadd('snake_user',self.username):
            self.cur.execute("SELECT * FROM snake where username = '%s'" % user)
            mysql_connector.commit()
            u = self.cur.fetchone()
            if not u:
                self.cur.execute("INSERT INTO snake (username) values('%s')" % user)
                mysql_connector.commit()

            self.cur.execute("SELECT * FROM snake")
            mysql_connector.commit()
            results = list(self.cur.fetchall())
            if results:
                for result in results:
                    temp_d = [result[0], result[1], result[2], result[2] // 10]
                    self.data_ls.append(temp_d)
                self.client.send(str(self.data_ls).encode())
            else:
                self.client.send(b'No data!')
        else:
            self.client.send(b'U online')

    def change_best_score(self,best_score,username):
        self.cur.execute("SELECT best_score FROM snake WHERE username = '%s'" % username)
        mysql_connector.commit()
        b_s = self.cur.fetchone()
        if b_s[0] > int(best_score):
            return
        self.cur.execute("UPDATE snake SET best_score = %d where username = '%s'" % (int(best_score),username))
        mysql_connector.commit()
        self.cur.execute("SELECT best_score FROM snake where username = '%s'" % username)
        mysql_connector.commit()
        result = self.cur.fetchone()
        self.client.send(('change ok' + str(result[0])).encode())


    def run(self):
        while True:
            data = self.client.recv(st.recv_max_bytes)
            if not data:
                r_connector.srem('snake_user',self.username)
                self.client.close()
                print('The address of {} has exited'.format(self.address))
                break

            elif 'home' in data.decode():
                self.show_main_data(data.decode().split(' ',1)[1])

            elif data.decode().startswith('score'):
                self.change_best_score(data.decode().split(' ')[1],data.decode().split(' ')[2])

            elif eval(data.decode())[0] == 'q':
                r_connector.srem('snake_user',self.username)
                self.client.close()
                print('The address of {} has exited'.format(self.address))
                break


def main_server():
    server = socket.socket()
    server.bind((st.server_ip,st.server_port))
    server.listen()
    print('listening to the port of %d...' % st.server_port)
    while True:
        try:
            client, address = server.accept()
            print('The address of {}'.format(address))
            c = Client(client, address)
            p_ls.append(c)
            c.start()
        except KeyboardInterrupt as e:
            server.close()
            r_connector.delete('snake_user')
            # if p_ls:
            #     for p in p_ls:
            #         os.kill(p.pid,signal.SIGKILL)
            print('server close.')
            break
        except Exception as e:
            with open('server_log.txt','a+',encoding='utf-8') as f:
                f.write("Error:" + str(e) + '\n')
                f.write(str(datetime.datetime.now()) + '\n')
            print('Error:',str(e))


if __name__ == '__main__':
    main_server()

