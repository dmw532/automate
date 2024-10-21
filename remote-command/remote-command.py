import paramiko

class RemoteCommand:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.load_credentials()
        self.flag = True


    def load_credentials(self):
        self.username = input("Username: ")
        self.password = input("Password: ")

    def connect(self, host):
        try:
            self.ssh.connect(host, port=22, username=self.username, password=self.password, timeout=3)
            self.flag = True
        except:
            print("Couldn't connect to %s" % host)
            self.flag = False

    def remote_command(self):
        if self.flag == True:
            command = 'sudo -S rm -rf /var/cache/nvidiareboot.lock'
            (stdin, stdout, stderr) = self.ssh.exec_command(command)
            stdin.write(self.password + '\n')  # Writing the password for sudo
            stdin.flush()  # Ensure the password is sent

            exit_status = stdout.channel.recv_exit_status()  # Wait for command to complete

            if exit_status == 0:
                print("Lock file removed successfully.")
            else:
                print(f"Failed to remove lock file: {stderr.read().decode()}")

hosts = [
    'dummy',
]

rc = RemoteCommand()

for host in hosts:
    rc.connect(host)
    # rc.remote_command()
