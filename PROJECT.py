import os
import time
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext,ttk
from multiprocessing import Process, Queue, Pipe, Semaphore, shared_memory
from datetime import datetime

# Global lists to track running processes and threads
processes = []
threads = []
log_file = "ipc_debugger.log"

# Function to log messages to a file
def log_message(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Update output window
def update_output(output_widget, message, tag=None):
    """Updates the GUI output area with optional tag colors and timestamps."""
    timestamp = datetime.now().strftime("[%H:%M:%S] ")
    log_message(message.strip())
    output_widget.insert(tk.END, timestamp + message, tag)
    output_widget.see(tk.END)


# Clear output window
def clear_output(output_widget):
    """Clears the output log."""
    output_widget.delete(1.0, tk.END)

# Separate child function for multiprocessing
def child(pipe):
    """Child process sends data through pipe."""
    pipe.send("Hello from child process through pipe")
    pipe.close()

# Monitor Pipes
def monitor_pipes(output_widget):
    """Monitors IPC using pipes."""
    parent_conn, child_conn = Pipe()
    proc = Process(target=child, args=(child_conn,))
    processes.append(proc)

    proc.start()
    proc.join()

    message = f"[PIPE] Received: {parent_conn.recv()}\n"
    update_output(output_widget, message, "PIPE")


# Monitor Shared Memory
def monitor_shared_memory(output_widget):
    """Monitors IPC using shared memory."""
    data = b"Shared Memory Data"
    shm = shared_memory.SharedMemory(create=True, size=len(data))

    memoryview(shm.buf)[:len(data)] = data

    message = f"[SHM] Written: {bytes(shm.buf[:len(data)]).decode()}\n"
    update_output(output_widget, message,"SHM")

    shm.close()
    shm.unlink()

# Monitor Semaphores
def monitor_semaphore(output_widget):
    """Monitors IPC using semaphores."""
    sem = Semaphore(1)
    sem.acquire()
    update_output(output_widget, "[SEMAPHORE] Locked\n")
    time.sleep(1)
    sem.release()
    update_output(output_widget, "[SEMAPHORE] Unlocked\n","SEMAPHORE")

# Socket server process
def socket_server(queue, host, port):
    """Socket server process that sends messages to the queue."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            queue.put(f"[SOCKET] Received: {data.decode()}\n")

# Socket client process
def socket_client(host, port):
    """Socket client sends a message."""
    time.sleep(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        client.sendall(b"Hello from socket client!")

# Monitor sockets with queue
def monitor_sockets(output_widget):
    """Monitors IPC using sockets with a Queue."""
    host = '127.0.0.1'
    port = 65432
    queue = Queue()

    server_process = Process(target=socket_server, args=(queue, host, port))
    client_process = Process(target=socket_client, args=(host, port))

    processes.extend([server_process, client_process])

    server_process.start()
    client_process.start()

    client_process.join()
    server_process.join()

    while not queue.empty():
        message = queue.get()
        update_output(output_widget, message,"SOCKET")

# Monitor Threads
def thread_task(output_widget, thread_id):
    """Simulates a thread running a task."""
    time.sleep(2)
    message = f"[THREAD] Thread {thread_id} completed task\n"
    update_output(output_widget, message,"THREAD")

def monitor_threads(output_widget):
    """Monitors IPC using threads."""
    for i in range(3):  # Start 3 threads
        thread = threading.Thread(target=thread_task, args=(output_widget, i))
        threads.append(thread)
        thread.start()
        

# Display running processes
def show_processes(output_widget):
    """Displays active processes."""
    message = "[ACTIVE PROCESSES]\n"
    for proc in processes:
        if proc.is_alive():
            message += f"Process {proc.pid} - Running\n"
    update_output(output_widget, message)

# Stop running processes
def stop_debugger(output_widget):
    """Stops all running IPC processes and threads."""
    for proc in processes:
        if proc.is_alive():
            proc.terminate()
    for thread in threads:
        if thread.is_alive():
            thread.join()
    update_output(output_widget, "\n[STOPPED] All IPC processes and threads terminated.\n")

# Run the IPC Debugger
def run_debugger(output_widget):
    """Runs the entire IPC debugger."""
    output_widget.delete(1.0, tk.END)
    update_output(output_widget, "\n---- IPC Debugger ----\n")

    monitor_pipes(output_widget)
    monitor_shared_memory(output_widget)
    monitor_semaphore(output_widget)
    monitor_sockets(output_widget)
    monitor_threads(output_widget)

    update_output(output_widget, "\nIPC Monitoring Completed!\n","TITLE")

# GUI Setup
# Export the log file to a timestamped backup
def export_log():
    """Exports the current log file to a timestamped backup."""
    if os.path.exists(log_file):
        backup_name = f"ipc_debugger_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, "r") as original, open(backup_name, "w") as backup:
            backup.write(original.read())
        print(f"Log exported to {backup_name}")

def setup_gui():
    
    """Creates the GUI window."""
    app = tk.Tk()
    app.title("Enhanced IPC Debugger")
    app.geometry("850x550")

    # Output log area
    output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
    output_text.tag_config("PIPE", foreground="cyan")
    output_text.tag_config("SHM", foreground="magenta")
    output_text.tag_config("SEMAPHORE", foreground="orange")
    output_text.tag_config("SOCKET", foreground="green")
    output_text.tag_config("THREAD", foreground="blue")
    output_text.tag_config("TITLE", foreground="white", background="black", font=("Helvetica", 12, "bold"))

    output_text.pack(pady=10)
    thread_progress = tk.IntVar()
    progress_bar = tk.ttk.Progressbar(app, length=600, mode='determinate', variable=thread_progress, maximum=3)
    progress_bar.pack(pady=5)


    button_frame = tk.Frame(app)
    button_frame.pack(pady=5)
    export_btn = tk.Button(button_frame, text="Export Log", command=lambda: export_log(), bg="purple",
                           fg="white", font=("Helvetica", 12))
    
    export_btn.pack(side=tk.LEFT, padx=5)


    tk.Label(app, text="Inter-Process Communication (IPC) Debugger", font=("Helvetica", 16, "bold")).pack(pady=10)

    run_btn = tk.Button(button_frame, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green",
                        fg="white", font=("Helvetica", 12))
    run_btn.pack(side=tk.LEFT, padx=5)

    stop_btn = tk.Button(button_frame, text="Stop Debugger", command=lambda: stop_debugger(output_text), bg="orange",
                         fg="white", font=("Helvetica", 12))
    stop_btn.pack(side=tk.LEFT, padx=5)

    process_btn = tk.Button(button_frame, text="Show Processes", command=lambda: show_processes(output_text), bg="blue",
                            fg="white", font=("Helvetica", 12))
    process_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(button_frame, text="Clear Log", command=lambda: clear_output(output_text), bg="red",
                          fg="white", font=("Helvetica", 12))
    clear_btn.pack(side=tk.LEFT, padx=5)

    app.mainloop()

# Main Execution
if __name__ == "__main__":
    setup_gui()

