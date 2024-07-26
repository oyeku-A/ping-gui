---

# Ping GUI

Ping GUI is a simple and user-friendly graphical application built with Tkinter. This tool allows users to enter one or more IP addresses and ping them either sequentially or all at once. Users can choose to ping each address a set number of times (e.g., 4 times) or continuously. The application provides real-time feedback, displaying the current date and time, the ping responses in milliseconds, and other relevant information.

---

### Key Features:
- **Multi-IP Ping:** Enter and ping multiple IP addresses simultaneously or one by one.
- **Ping Options:** Choose to ping each IP address a fixed number of times or infinitely.
- **Real-Time Feedback:** View real-time ping response times in milliseconds.
- **Date and Time Display:** See the current date and time updated in real-time.
- **User-Friendly Interface:** Simple and intuitive interface built with Tkinter.

---

### Requirements:
- Python 3.x
- Tkinter (usually included with Python)
- Requests library (`pip install requests`)

### How to Run:
1. Ensure you have Python 3.x installed on your system.
2. Install the necessary libraries using `pip install requests`.
3. Run the script using `python app.py`.

### Notes:
- This script opens up powershell inside of cmd, this was done based off requirements. So feel free to modify the code to ping directly from powershell
