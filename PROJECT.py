# import os
# import time
# import socket
# import tkinter as tk
# from tkinter import scrolledtext
# from multiprocessing import Process, Queue, Pipe, Semaphore, shared_memory


# # Global list to track running processes
# processes = []
 
# # Update output window
# def update_output(output_widget, message):
#      """Updates the GUI output area with timestamps."""
#      timestamp = datetime.now().strftime("[%H:%M:%S] ")
#      output_widget.insert("1.0", timestamp + message)
#      output_widget.see("1.0")
 
#  # Clear output window
# def clear_output(output_widget):
#      """Clears the output log."""
#      output_widget.delete(1.0, tk.END)
 

# # Separate child function for multiprocessing
# def child(pipe):
#     """Child process sends data through pipe."""
#     pipe.send("Hello from child process through pipe")
#     pipe.close()


# # Monitor Pipes
# def monitor_pipes(output_widget):
#     """Monitors IPC using pipes."""
#     parent_conn, child_conn = Pipe()

#     proc = Process(target=child, args=(child_conn,))
#     proc.start()
#     proc.join()

#     message = f"[PIPE] Received: {parent_conn.recv()}\n"
#     update_output(output_widget, message)


# # Monitor Shared Memory
# def monitor_shared_memory(output_widget):
#     """Monitors IPC using shared memory."""
#     data = b"Shared Memory Data"
#     shm = shared_memory.SharedMemory(create=True, size=len(data))  # Ensure correct size

#     # Assign data to shared memory using memoryview
#     memoryview(shm.buf)[:len(data)] = data

#     message = f"[SHM] Written: {bytes(shm.buf[:len(data)]).decode()}\n"
#     update_output(output_widget, message)

#     # Clean up
#     shm.close()
#     shm.unlink()


# # Monitor Semaphores
# def monitor_semaphore(output_widget):
#     """Monitors IPC using semaphores."""
#     sem = Semaphore(1)

#     sem.acquire()
#     update_output(output_widget, "[SEMAPHORE] Locked\n")

#     time.sleep(1)
#     sem.release()
#     update_output(output_widget, "[SEMAPHORE] Unlocked\n")


# # Socket server process (without GUI references)
# def socket_server(queue, host, port):
#     """Socket server process that sends messages to the queue."""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#         server.bind((host, port))
#         server.listen()

#         conn, addr = server.accept()
#         with conn:
#             data = conn.recv(1024)
#             queue.put(f"[SOCKET] Received: {data.decode()}\n")


# # Socket client process
# def socket_client(host, port):
#     """Socket client sends a message."""
#     time.sleep(1)
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#         client.connect((host, port))
#         client.sendall(b"Hello from socket client!")


# # Monitor sockets with queue
# def monitor_sockets(output_widget):
#     """Monitors IPC using sockets with a Queue."""
#     host = '127.0.0.1'
#     port = 65432

#     queue = Queue()

#     server_process = Process(target=socket_server, args=(queue, host, port))
    
#     client_process = Process(target=socket_client, args=(host, port))

#     server_process.start()
#     client_process.start()

#     client_process.join()
#     server_process.join()

#     # Display messages from the queue
#     while not queue.empty():
#         message = queue.get()
#         update_output(output_widget, message)


# # Update output window
# def update_output(output_widget, message):
#     """Updates the GUI output area."""
#     output_widget.insert(tk.END, message)
#     output_widget.see(tk.END)

# def clear_output(output_widget):
#       """Clears the output log."""
#       output_widget.delete(1.0, tk.END)
#       # Stop running processes
# def stop_debugger(output_widget):
#      """Stops all running IPC processes."""
#      for proc in processes:
#          if proc.is_alive():
#              proc.terminate()
#      update_output(output_widget, "\n[STOPPED] All IPC processes terminated.\n")
# # Run the IPC Debugger
# def run_debugger(output_widget):
#     """Runs the entire IPC debugger."""

#     output_widget.delete(1.0, tk.END)
#     update_output(output_widget, "\n---- IPC Debugger ----\n")

#     monitor_pipes(output_widget)

#     monitor_shared_memory(output_widget)
#     monitor_semaphore(output_widget)
#     monitor_sockets(output_widget)

#     update_output(output_widget, "\nIPC Monitoring Completed!\n")


# # GUI Setup
# def setup_gui():
#     """Creates the GUI window."""
#     app = tk.Tk()
#     app.title("IPC Debugger (Windows Compatible)")
#      # Output log area
#     output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
#     output_text.pack(pady=10)
  
#     clear_btn = tk.Button(app, text="Clear Log", command=lambda: clear_output(output_text), bg="red", fg="white",
#                             font=("Helvetica", 12))
#     clear_btn.pack(pady=5)
  
#       # "Run Debugger" button
#     btn = tk.Button(app, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green", fg="white",
#                       font=("Helvetica", 12))
#     btn.pack(pady=5)
#     stop_btn = tk.Button(app, text="Stop Debugger", command=lambda: stop_debugger(output_text), bg="orange", fg="white", font=("Helvetica", 12))
#     stop_btn.pack(pady=5)
 
 

#     app.geometry("800x500")

#     tk.Label(app, text="Inter-Process Communication (IPC) Debugger", font=("Helvetica", 16, "bold")).pack(pady=10)

#     output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
#     output_text.pack(pady=10)

#     btn = tk.Button(app, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green", fg="white",
#                     font=("Helvetica", 12))
#     btn.pack(pady=5)

#     app.mainloop()

# from datetime import datetime
# def update_output(output_widget, message):
#      """Updates the GUI output area with timestamps."""
#      timestamp = datetime.now().strftime("[%H:%M:%S] ")
#      output_widget.insert(tk.END, timestamp + message)
#      output_widget.see(tk.END)
# # Main Execution
# if __name__ == "__main__":
#     setup_gui()

# import os
# import time
# import socket
# import threading
# import tkinter as tk
# from tkinter import scrolledtext
# from multiprocessing import Process, Queue, Pipe, Semaphore, shared_memory
# from datetime import datetime

# # Global lists to track running processes and threads
# processes = []
# threads = []
# log_file = "ipc_debugger.log"

# # Function to log messages to a file
# def log_message(message):
#     with open(log_file, "a") as f:
#         f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# # Update output window
# def update_output(output_widget, message):
#     """Updates the GUI output area with timestamps."""
#     timestamp = datetime.now().strftime("[%H:%M:%S] ")
#     log_message(message.strip())  # Log messages to a file
#     output_widget.insert(tk.END, timestamp + message)
#     output_widget.see(tk.END)

# # Clear output window
# def clear_output(output_widget):
#     """Clears the output log."""
#     output_widget.delete(1.0, tk.END)

# # Separate child function for multiprocessing
# def child(pipe):
#     """Child process sends data through pipe."""
#     pipe.send("Hello from child process through pipe")
#     pipe.close()

# # Monitor Pipes
# def monitor_pipes(output_widget):
#     """Monitors IPC using pipes."""
#     parent_conn, child_conn = Pipe()
#     proc = Process(target=child, args=(child_conn,))
#     processes.append(proc)

#     proc.start()
#     proc.join()

#     message = f"[PIPE] Received: {parent_conn.recv()}\n"
#     update_output(output_widget, message)

# # Monitor Shared Memory
# def monitor_shared_memory(output_widget):
#     """Monitors IPC using shared memory."""
#     data = b"Shared Memory Data"
#     shm = shared_memory.SharedMemory(create=True, size=len(data))

#     memoryview(shm.buf)[:len(data)] = data

#     message = f"[SHM] Written: {bytes(shm.buf[:len(data)]).decode()}\n"
#     update_output(output_widget, message)

#     shm.close()
#     shm.unlink()

# # Monitor Semaphores
# def monitor_semaphore(output_widget):
#     """Monitors IPC using semaphores."""
#     sem = Semaphore(1)
#     sem.acquire()
#     update_output(output_widget, "[SEMAPHORE] Locked\n")
#     time.sleep(1)
#     sem.release()
#     update_output(output_widget, "[SEMAPHORE] Unlocked\n")

# # Socket server process
# def socket_server(queue, host, port):
#     """Socket server process that sends messages to the queue."""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#         server.bind((host, port))
#         server.listen()
#         conn, addr = server.accept()
#         with conn:
#             data = conn.recv(1024)
#             queue.put(f"[SOCKET] Received: {data.decode()}\n")

# # Socket client process
# def socket_client(host, port):
#     """Socket client sends a message."""
#     time.sleep(1)
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#         client.connect((host, port))
#         client.sendall(b"Hello from socket client!")

# # Monitor sockets with queue
# def monitor_sockets(output_widget):
#     """Monitors IPC using sockets with a Queue."""
#     host = '127.0.0.1'
#     port = 65432
#     queue = Queue()

#     server_process = Process(target=socket_server, args=(queue, host, port))
#     client_process = Process(target=socket_client, args=(host, port))

#     processes.extend([server_process, client_process])

#     server_process.start()
#     client_process.start()

#     client_process.join()
#     server_process.join()

#     while not queue.empty():
#         message = queue.get()
#         update_output(output_widget, message)

# # Monitor Threads
# def thread_task(output_widget, thread_id):
#     """Simulates a thread running a task."""
#     time.sleep(2)
#     message = f"[THREAD] Thread {thread_id} completed task\n"
#     update_output(output_widget, message)

# def monitor_threads(output_widget):
#     """Monitors IPC using threads."""
#     for i in range(3):  # Start 3 threads
#         thread = threading.Thread(target=thread_task, args=(output_widget, i))
#         threads.append(thread)
#         thread.start()

# # Display running processes
# def show_processes(output_widget):
#     """Displays active processes."""
#     message = "[ACTIVE PROCESSES]\n"
#     for proc in processes:
#         if proc.is_alive():
#             message += f"Process {proc.pid} - Running\n"
#     update_output(output_widget, message)

# # Stop running processes
# def stop_debugger(output_widget):
#     """Stops all running IPC processes and threads."""
#     for proc in processes:
#         if proc.is_alive():
#             proc.terminate()
#     for thread in threads:
#         if thread.is_alive():
#             thread.join()
#     update_output(output_widget, "\n[STOPPED] All IPC processes and threads terminated.\n")

# # Run the IPC Debugger
# def run_debugger(output_widget):
#     """Runs the entire IPC debugger."""
#     output_widget.delete(1.0, tk.END)
#     update_output(output_widget, "\n---- IPC Debugger ----\n")

#     monitor_pipes(output_widget)
#     monitor_shared_memory(output_widget)
#     monitor_semaphore(output_widget)
#     monitor_sockets(output_widget)
#     monitor_threads(output_widget)

#     update_output(output_widget, "\nIPC Monitoring Completed!\n")

# # GUI Setup
# def setup_gui():
#     """Creates the GUI window."""
#     app = tk.Tk()
#     app.title("Enhanced IPC Debugger")
#     app.geometry("850x550")

#     # Output log area
#     output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
#     output_text.pack(pady=10)

#     button_frame = tk.Frame(app)
#     button_frame.pack(pady=5)

#     tk.Label(app, text="Inter-Process Communication (IPC) Debugger", font=("Helvetica", 16, "bold")).pack(pady=10)

#     run_btn = tk.Button(button_frame, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green",
#                         fg="white", font=("Helvetica", 12))
#     run_btn.pack(side=tk.LEFT, padx=5)

#     stop_btn = tk.Button(button_frame, text="Stop Debugger", command=lambda: stop_debugger(output_text), bg="orange",
#                          fg="white", font=("Helvetica", 12))
#     stop_btn.pack(side=tk.LEFT, padx=5)

#     process_btn = tk.Button(button_frame, text="Show Processes", command=lambda: show_processes(output_text), bg="blue",
#                             fg="white", font=("Helvetica", 12))
#     process_btn.pack(side=tk.LEFT, padx=5)

#     clear_btn = tk.Button(button_frame, text="Clear Log", command=lambda: clear_output(output_text), bg="red",
#                           fg="white", font=("Helvetica", 12))
#     clear_btn.pack(side=tk.LEFT, padx=5)

#     app.mainloop()

# # Main Execution
# if __name__ == "__main__":
#     setup_gui()

import os
import time
import socket
import tkinter as tk
from tkinter import scrolledtext
from multiprocessing import Process, Queue, Pipe, Semaphore, shared_memory
from datetime import datetime
log_count = 0
# ✅ Child function for multiprocessing
def child(pipe):
    """Child process sends data through pipe."""
    pipe.send("Hello from child process through pipe")
    pipe.close()

# ✅ Monitor Pipes
def monitor_pipes(output_widget, app):
    """Monitors IPC using pipes."""
    parent_conn, child_conn = Pipe()

    proc = Process(target=child, args=(child_conn,))
    proc.start()
    proc.join()

    message = f"[PIPE] Received: {parent_conn.recv()}\n"
    update_output(output_widget, message)
    
    # Refresh GUI frequently
    app.update()

# ✅ Monitor Shared Memory
def monitor_shared_memory(output_widget, app):
    """Monitors IPC using shared memory."""
    data = b"Shared Memory Data"
    shm = shared_memory.SharedMemory(create=True, size=len(data))

    memoryview(shm.buf)[:len(data)] = data

    message = f"[SHM] Written: {bytes(shm.buf[:len(data)]).decode()}\n"
    update_output(output_widget, message)

    # Clean up
    shm.close()
    shm.unlink()
    
    # Refresh GUI
    app.update()

# ✅ Monitor Semaphores
def monitor_semaphore(output_widget, app):
    """Monitors IPC using semaphores."""
    sem = Semaphore(1)

    sem.acquire()
    update_output(output_widget, "[SEMAPHORE] Locked\n")

    time.sleep(1)
    sem.release()
    update_output(output_widget, "[SEMAPHORE] Unlocked\n")
    
    # Refresh GUI
    app.update()

# ✅ Socket server process
def socket_server(queue, host, port):
    """Socket server process that sends messages to the queue."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()

        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            queue.put(f"[SOCKET] Received: {data.decode()}\n")

# ✅ Socket client process
def socket_client(host, port):
    """Socket client sends a message."""
    time.sleep(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        client.sendall(b"Hello from socket client!")

# ✅ Monitor Sockets
def monitor_sockets(output_widget, app):
    """Monitors IPC using sockets with a Queue."""
    host = '127.0.0.1'
    port = 65432

    queue = Queue()

    server_process = Process(target=socket_server, args=(queue, host, port))
    client_process = Process(target=socket_client, args=(host, port))

    server_process.start()
    client_process.start()

    client_process.join()
    server_process.join()

    while not queue.empty():
        message = queue.get()
        update_output(output_widget, message)
        
        # Refresh GUI
        app.update()

# ✅ Real-time log updater with timestamps
def update_output(output_widget, message):
    """Updates the GUI output area with timestamps."""
    global log_count  # Use the global counter
    log_count += 1  # Increment the log count
    timestamp = datetime.now().strftime("[%H:%M:%S] ")
    output_widget.insert(tk.END, timestamp + message)
    output_widget.see(tk.END)
    output_widget.update_idletasks()  # Force GUI to refresh immediately


# ✅ Run IPC with GUI update
def run_debugger(output_widget, app):
    """Runs the entire IPC debugger with GUI refresh for better performance."""
    output_widget.delete(1.0, tk.END)
    update_output(output_widget, "\n---- IPC Debugger ----\n")

    monitor_pipes(output_widget, app)
    monitor_shared_memory(output_widget, app)
    monitor_semaphore(output_widget, app)
    monitor_sockets(output_widget, app)

    update_output(output_widget, "\nIPC Monitoring Completed!\n")

# ✅ Clear output log
def clear_output(output_widget):
    """Clears the output log."""
    output_widget.delete(1.0, tk.END)

# ✅ GUI Setup
def setup_gui():
    """Creates the GUI window."""
    app = tk.Tk()
    app.title("IPC Debugger (Windows Compatible)")
    app.geometry("1000x600")

    # Label
    tk.Label(app, text="Inter-Process Communication (IPC) Debugger", font=("Helvetica", 16, "bold")).pack(pady=10)

    # ✅ Single log area
    output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=25, font=("Courier", 10))
    output_text.pack(pady=10)

    # "Run Debugger" button
    # "Stop Execution" button
    stop_btn = tk.Button(app, text="Stop Execution", command=lambda: stop_execution(app), bg="orange", fg="black",
                     font=("Helvetica", 12))
    stop_btn.pack(pady=5)

    btn = tk.Button(app, text="Run Debugger", command=lambda: run_debugger(output_text, app), bg="green", fg="white",
                    font=("Helvetica", 12))
    btn.pack(pady=5)

    # "Clear Log" button
    clear_btn = tk.Button(app, text="Clear Log", command=lambda: clear_output(output_text), bg="red", fg="white",
                          font=("Helvetica", 12))
    clear_btn.pack(pady=5)

    app.mainloop()
 # ✅ Stop Execution Function
def stop_execution(app):
    app.destroy()  # Gracefully closes the application
# ✅ Main Execution
if __name__ == "__main__":
    setup_gui()

















