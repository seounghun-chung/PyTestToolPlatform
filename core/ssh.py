from paramiko import BadHostKeyException, AuthenticationException, SSHException
import paramiko
import select
import socket
import threading

class ssh(object):
    def __init__(self, *argv, **kwargs):
        self.client = None
        
    def connect(self, addr = '35.200.127.220', username = 'seounghun-chung', timeout = 3, retry = 3):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
        for retryCount in range(0, retry):
            try:
                self.client.connect(addr, username=username, timeout = timeout)
                self.sftp = self.client.open_sftp()                
                ret = True
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
                print(e, ': %d retry to connect ssh' % (retryCount))
                ret = False
        return ret
        
    def exec_command(self, command, retry = 2, callback=None):
        ''' callback(str param) '''
        for retryCount in range(0, retry):
            try:
                stdin , stdout, stderr = self.client.exec_command(command, get_pty=True)
                
                ''' read lines for executing command'''
                for line in iter(stdout.readline, ""):
                    ''' if there is callback, output will be returned via callback. if not, just print out '''
                    callback(line.strip()) if callback is not None else print(line, end='')

                ret = True
                break
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
                print(e, ': %d retry to exec_command in ssh' % (ii+1))
                ret = False
            except (AttributeError) as e:
                print(e, ': ssh session may be closed')
                ret = False
                break
        return ret

    def close(self):
        self.client.close()
        
    def callback_dummy(self, param):
        print('dummy: ', param)

    def callback_dummy2(self, current, total):
        print('dummy2: ', current, total)
        
    def get(self, remotepath, localpath, callback=None):
        ''' callback(int currentByte, int totalByte) '''
        return self.sftp.get(remotepath, localpath, callback=callback)
        
    def put(self, localpath, remotepath, callback=None):
        ''' callback(int currentByte, int totalByte) '''
        return self.sftp.put(localpath, remotepath, callback=callback)
        
def call(a):
    print(type(a), a)

def get_byte(a,b):
    print('bytes : ', a,b)
    return True
    
if __name__ == "__main__":
    a = ssh()
    a.connect(addr = '35.200.127.220', retry = 1)
    ret = a.put('./hello.py', './hello.py', a.callback_dummy2)
    print(ret)
#    a.exec_command('cd source ; ls -all; sleep 1 ; python3 test2.py')
#    a.exec_command('ls -all')
#    th = threading.Thread(target = a.exec_command, args=('python3 test.py', 2, a.callback_dummy,))
#    th.daemon = True
#    th.start()
#
#    #b = a.exec_command('python3 test.py', callback=call)
#    print('hello')
#    import time
#    time.sleep(4.2)
#    a.close()
#    th.join()
#    a.connect()
#    a.exec_command('ls -all')
#    print('bye')