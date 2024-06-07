import paramiko
import tkinter as tk
from datetime import datetime


class GUI:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("SFTP Configuration")

        # Define variables with default values
        self.username_var = tk.StringVar(value="admin")
        self.host_ip_var = tk.StringVar(value="192.168.1.104")
        self.port_var = tk.StringVar(value="22")
        self.password_var = tk.StringVar()
        self.file_name_var = tk.StringVar(value="file.csv")
        self.remote_filepath_var = tk.StringVar(value="/home/admin/Desktop/")
        self.local_filepath_var = tk.StringVar(value="./")

    def submit(self):
        self.root.destroy()

    def popup_box(self):
        # Create and place the labels and entry widgets with padding
        pad_options = {'padx': 10, 'pady': 5}

        # Create and place the labels and entry widgets
        tk.Label(self.root, text="Username:").grid(row=0, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.username_var).grid(row=0, column=1, **pad_options)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.password_var, show='*').grid(row=1, column=1, **pad_options)

        tk.Label(self.root, text="Host IP:").grid(row=2, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.host_ip_var).grid(row=2, column=1, **pad_options)

        tk.Label(self.root, text="Port:").grid(row=3, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.port_var).grid(row=3, column=1, **pad_options)

        tk.Label(self.root, text="File Name:").grid(row=4, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.file_name_var).grid(row=4, column=1, **pad_options)

        tk.Label(self.root, text="Remote Filepath:").grid(row=5, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.remote_filepath_var).grid(row=5, column=1, **pad_options)

        tk.Label(self.root, text="Local Filepath:").grid(row=6, column=0, sticky='e', **pad_options)
        tk.Entry(self.root, textvariable=self.local_filepath_var).grid(row=6, column=1, **pad_options)

        # Create and place the submit button
        tk.Button(self.root, text="Submit", command=self.submit).grid(row=7, columnspan=2, pady=10)

        # Add padding around the entire window
        for i in range(8):
            self.root.grid_rowconfigure(i, pad=10)
        for i in range(2):
            self.root.grid_columnconfigure(i, pad=10)

        # Run the main event loop
        self.root.mainloop()


class SFTP_Manager:
    def __init__(self, host, port, username, password, file_name, remote_path, local_path):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.file_name = file_name
        self.remote_path = remote_path
        self.local_path = local_path

    def sftp_file_grabber(self):
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.connect(self.host, port=self.port, username=self.username, password=self.password)
            with ssh.open_sftp() as sftp:
                sftp.get(self.remote_path + self.file_name, self.local_path + self.file_name)


popup_gui = GUI()
popup_gui.popup_box()

sftp_man = SFTP_Manager(username=popup_gui.username_var.get(),
                        host=popup_gui.host_ip_var.get(),
                        port=int(popup_gui.port_var.get()),
                        password=popup_gui.password_var.get(),
                        file_name=popup_gui.file_name_var.get(),
                        remote_path=popup_gui.remote_filepath_var.get(),
                        local_path=popup_gui.local_filepath_var.get())


def write_to_logfile(popup_obj, filename='log'):
    # Get the current date
    current_date = datetime.now()
    # Format the date as "Year Month Day Hour Minute Second"
    formatted_date = current_date.strftime("%Y%m%d%H%M%S")
    filename = f"{filename}_{formatted_date}.txt"

    with open(filename, 'a') as logfile:  # Open the file in append mode
        logfile.write(f"Username: {popup_obj.username}\n")
        logfile.write(f"Host IP: {popup_obj.host}\n")
        logfile.write(f"Port: {popup_obj.port}\n")
        logfile.write(f"Password: {'*' * len(popup_obj.password)}\n")
        logfile.write(f"File Name: {popup_obj.file_name}\n")
        logfile.write(f"Remote Filepath: {popup_obj.remote_path}\n")
        logfile.write(f"Local Filepath: {popup_obj.local_path}\n")
        logfile.write("\n")  # Add a newline for separation


sftp_man.sftp_file_grabber()
write_to_logfile(sftp_man)

