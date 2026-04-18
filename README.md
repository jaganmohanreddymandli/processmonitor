🖥️ Process Monitor Dashboard

A real-time system monitoring dashboard built with Python and PySide6.
It displays CPU usage, memory usage, and running processes with a live updating UI.

🚀 Features
📊 Real-time CPU usage graph
🧠 Memory usage monitoring
📋 Live process table
🔄 Auto-refresh with timer updates
🖥️ Clean GUI built using PySide6
🛠️ Tech Stack
Python 3
PySide6 (Qt for Python)
System monitoring via custom backend functions
📂 Project Structure
ProcessMonitor/
│── core/
│   └── system_monitor.py      # CPU, memory, process logic
│
│── widgets/
│   └── cpu_graph.py           # Live CPU graph widget
│
│── main.py                    # Main application entry point
│── README.md
│── requirements.txt
⚙️ Installation
1. Clone the repository
git clone https://github.com/jaganmohanreddymandli/processmonitor.git
cd ProcessMonitor
2. Create virtual environment
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
▶️ Run the Application
python main.py

📌 Future Improvements
🔍 Search & filter processes
❌ Kill process feature
🌙 Dark mode UI
📈 More system metrics (disk, network)
🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

📄 License

This project is open-source and available under the MIT License.

🙌 Author

Jaganmohan Reddy

⭐ Support

If you like this project, give it a ⭐ on GitHub!
