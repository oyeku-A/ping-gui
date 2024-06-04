import re
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

class IPApp:
    def __init__(self, root):
        # root window
        self.root = root
        self.root.title("IP Ping Tool")
        self.root.geometry("250x220")
        self.root.resizable(height=False, width=False)

        # Left Frame
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", padx=10, pady=10)

        # Left Frame - ip input entry
        self.ip_entry = tk.Entry(self.left_frame, width=15, justify='left')
        self.ip_entry.grid(column=0, row=1, sticky='NWES')
        self.ip_entry.focus()

        # Left Frame - dislay text 'ping'
        self.ip_text = tk.Label(self.left_frame, text="Ping:")
        self.ip_text.grid(column=0, row=2, sticky='NWS')

        #Left Frame - radio button for 'ping' options
        self.ping_option = tk.StringVar(value='Single')
        self.ping_single_radio = tk.Radiobutton(self.left_frame, text='Single', variable=self.ping_option, value='Single', command=self.activate_entry)
        self.ping_single_radio.grid(column=0, row=3, sticky='W')
        self.ping_all_radio = tk.Radiobutton(self.left_frame, text='All', variable=self.ping_option, value='All', command=self.deactivate_entry)
        self.ping_all_radio.grid(column=0, row=4, sticky='W')  

        # Left Frame - dislay text 'Reptition'
        self.ip_text = tk.Label(self.left_frame, text="Repetition:")
        self.ip_text.grid(column=0, row=5, sticky='NWS')

        # Left Frame - radio button for 'Reptition' options
        self.repetition_option = tk.StringVar(value='4') 
        self.repetition_4_radio = tk.Radiobutton(self.left_frame, text='4', variable=self.repetition_option, value='4')
        self.repetition_4_radio.grid(column=0, row=6, sticky='W')
        self.repetition_inf_radio = tk.Radiobutton(self.left_frame, text='Inf', variable=self.repetition_option, value='Inf')
        self.repetition_inf_radio.grid(column=0, row=7, sticky='W')

        # Left Frame - start button
        self.start_button = tk.Button(self.left_frame, text="Start", fg="green", command=self.start_ping)
        self.start_button.grid(column=0, row=8, sticky='NWES', padx=10, columnspan=3, pady=(10, 0))

        self.processes = []
        self.root.bind("<Return>", self.start_ping)

        # Right Frame
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", padx=10, pady=10)

        # Right Frame - list box containing saved ip addresses
        self.ip_listbox = tk.Listbox(self.right_frame, selectmode='single', width=15)
        self.ip_listbox.grid(column=0, row=1, rowspan=7, sticky='NWES')

        self.ip_listbox.bind("<Double-Button-1>", self.display_selected_ip)

        # Right Frame - add and remove buttons
        self.add_remove_frame = tk.Frame(self.right_frame)
        self.add_remove_frame.grid(column=0, row=8, sticky='NWES', pady=(7, 0))
        self.add_button = tk.Button(self.add_remove_frame, text="Add", fg="green", command=self.add_ip)
        self.add_button.grid(column=1, row=0, sticky='NWES', padx=10)
        self.remove_button = tk.Button(self.add_remove_frame, text="Remove", fg="red", command=self.remove_ip)
        self.remove_button.grid(column=2, row=0, sticky='NWES')

        # Load Ip addresses from file(Ip_addresses.txt) if available
        self.load_ip_address()
     
    def validate_ip(self, ip):
        # Regular expression for Ipv4 address validation
        return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip)

    def add_ip(self):
        # Adds the Content of the Ip entry field to the listbox and saves the updated list of IP addresses.
        ip = self.ip_entry.get()
        if ip:
            if self.validate_ip(ip):
                if ip not in self.ip_listbox.get(0, tk.END):
                    self.ip_listbox.insert(tk.END, ip) 
                    self.ip_entry.delete(0, tk.END)
                else:
                    messagebox.showinfo("Duplicate IP", f"{ip} already exists in the saved Ip.")
            else:
                messagebox.showerror("Invalid IP", f"{ip} is not a valid IP address.")
        else:
            messagebox.showwarning("Empty Input", "Please enter an IP address.")
        self.save_ip_address()

    def remove_ip(self):
        # Removes the selected IP address from the listbox and saves the updated list of IP addresses. 
        selected_ip_index = self.ip_listbox.curselection()
        if selected_ip_index:
            self.ip_listbox.delete(selected_ip_index)
        else:
            messagebox.showerror("Select IP", f"No IP has been selected for removal.")
        self.save_ip_address()

    def save_ip_address(self):
        # Saves the list of IP addresses currently displayed in the listbox to a text file named "ip_addresses.txt".
        with open("ip_addresses.txt", "w") as file:
            for ip in self.ip_listbox.get(0, tk.END):
                file.write(f'{ip}\n')

    def load_ip_address(self):
        # Loads the list of IP addresses currently in a text file named "ip_addresses.txt" to listbox in the program
        try:
            with open('ip_addresses.txt', 'r') as file:
                for line in file:
                    ip = line.strip()
                    # This validates and checks for duplicates just incase the txt file was manually modified, inorder to avoid the programming crashing due to invalid IPv4 address or executing the same address if 'all' is selected
                    if self.validate_ip(ip):
                        if ip not in self.ip_listbox.get(0, tk.END):
                            self.ip_listbox.insert(tk.END, ip)
        except FileNotFoundError:
            pass

    def display_selected_ip(self, ip):
        # Displays the IP address selected in the listbox in the IP entry field for pinging
        selected_ip_index = self.ip_listbox.curselection()
        if selected_ip_index:
            ip = self.ip_listbox.get(selected_ip_index)
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, ip)

    def start_ping(self, event=None):
        # This function is responsible for initiating the ping process based on the selected option
        if self.ping_option.get() == 'Single':
            self.ping_single_ip()
        else:
            self.ping_all_ips()
    
    def ping_single_ip(self):
        # This function is responsible for initiating a single ping process to the IP address entered in the entry field.
        ip = self.ip_entry.get()
        count_option = '-n 4' if self.repetition_option.get() == '4' else '-t'
        if ip:
            if self.validate_ip(ip):
                ping_command = f'start cmd /k powershell -Command "& {{ ping.exe {count_option} "{ip}" | ForEach-Object {{ \\"{{0}} - {{1}}\\" -f (Get-Date),$_ }} }}"'
                process = subprocess.Popen(ping_command, shell=True)
                self.processes.append(process)
            else:
                messagebox.showerror("Invalid IP", f"{ip} is not a valid IP address.")
        else:
            messagebox.showwarning("Empty Input", "Please enter an IP address.")

    def ping_all_ips(self):
        # This function is responsible for initiating ping(s) of IP address(es) stored in the listbox
        ip_list = list(self.ip_listbox.get(0, tk.END))
        count_option = '-n 4' if self.repetition_option.get() == '4' else '-t'

        for ip in ip_list:
            if self.validate_ip(ip):
                ping_command = f'start cmd /k powershell -Command "& {{ ping.exe {count_option} "{ip}" | ForEach-Object {{ \\"{{0}} - {{1}}\\" -f (Get-Date),$_ }} }}"'
                process = subprocess.Popen(ping_command, shell=True)
                self.processes.append(process)
            else:
                messagebox.showerror("Invalid IP", f"{ip} is not a valid IP address.")
                      
    def deactivate_entry(self):
        # Deactivates the IP entry field when the 'All' radio button is selected
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.config(state='disabled')

    def activate_entry(self):
        # Reactivates the IP entry field when the 'All' radio button is deselected
        self.ip_entry.config(state='normal')


basedir = os.path.dirname(__file__)
icon_path = os.path.join(basedir, "icons", "icon.ico")

root = tk.Tk()
app = IPApp(root)
root.iconbitmap(icon_path)
root.mainloop()