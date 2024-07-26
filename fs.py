import os
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import threading
from plyer import notification
import time
import random
import hashlib
import webbrowser
import requests
import shutil
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import platform
import subprocess
import string

class FabiSkript:
    def __init__(self):
        self.commands = {
            'say': self.say,
            'wait': self.wait,
            'import all': self.import_all,
            'do': self.do,
            'delete': self.delete,
            'open': self.open,
            'end': self.end,
            'if': self.if_,
            'else': self.else_,
            'thisis': self.thisis,
            'term': self.term,
            '%ran%': self.ran,
            'point': self.point,
            'returnto': self.returnto,
            'set': self.set,
            'write': self.write,
            'makedir': self.makedir,
            'read': self.read,
            'hash': self.hash,
            'url': self.url,
            'down': self.down,
            'clean': self.clean,
            'curl': self.curl,
            'copy': self.copy,
            'move': self.move,
            'ren': self.rename,
            'dirlist': self.listdir,
            'getsize': self.size,
            'env': self.env,
            'zip': self.zip,
            '#': self.comment,
            '?': self.comment,
            'unzip': self.unzip,
            'netstat': self.netstat,
            'rboot': self.rboot,
            'shutdown': self.shutdown,
            'ipget': self.ipget,
            'fileclear': self.fileclear,
            'netipget': self.netipget,
            'kill': self.kill,
            'checksing': self.checksing,
            '/ui': self.userinput,
            'randomnum': self.randomnum,
            'random': self.random_command,
            'randomvar': self.randomvar,
            'meminf': self.meminfo,
            'cpuinf': self.cpuinfo,
            'sysinf': self.sysinfo,
            'traceroute': self.traceroute,
            'ping': self.ping,
            'fileinf': self.fileinfo,
            'deletedir': self.deldir,
            'copydir': self.copydir,
            'waitto': self.sleep_until,
            'Time': self.current_time,
            'Date': self.current_date,
            'replace': self.replace,
            'lower': self.lower,
            'upper': self.upper,
            'concat': self.concat,
            'divide': self.divide,
            'multiply': self.multiply,
            'subtract': self.subtract,
            'add': self.add,
            'msg': self.msg,
            'hashvar': self.hashvar,
            'appmsg': self.msgapp,
            'jsonr': self.jsonread,
            'jsonw': self.jsonwrite,
            'readli': self.readline,
            'perform': self.perform_operation_on_files,
            'elif': self.elif_,
            'checkread': self.checkread,
            'password': self.generate_password,
            'uinbox': self.uinbox,
            'runuinbox': self.runuinbox,
            'uinsay': self.uinsay,
            'uinbutten': self.uinbutten,
            'uinscale': self.uinscale,
            'uinlist': self.uinlist,
            'uinradio': self.uinradio,
            'uincheck': self.uincheck,
            'uinenter': self.uinenter,
            'progressbar': self.progressbar,
            'compare': self.compare,
            'randomnumvar': self.randomnumvar
        }
        self.functions = {}
        self.variables = {}
        self.root = None
        self.checkpoints = {}
        self.lines = []
        self.i = 0

    def run_script(self, script_file):
        with open(script_file, 'r') as f:
            script_code = f.read()
        self.lines = script_code.split('\n')
        self.execute_script()

    def execute_script(self):
        while self.i < len(self.lines):
            line = self.lines[self.i].strip()
            if line and not line.startswith('~'):
                parts = line.split()
                command = parts[0]
                args = parts[1:]
                if command in self.commands:
                    if command == 'do':
                        func_name = args[0]
                        self.i += 1
                        func_body = []
                        while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                            func_body.append(self.lines[self.i].strip())
                            self.i += 1
                        self.functions[func_name] = self.create_function(func_body)
                    elif command == 'else':
                        while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                            self.i += 1
                    elif command == 'point':
                        checkpoint_name = args[0]
                        self.checkpoints[checkpoint_name] = self.i
                    elif command == 'returnto':
                        checkpoint_name = args[0]
                        if checkpoint_name in self.checkpoints:
                            self.i = self.checkpoints[checkpoint_name]
                        else:
                            print(f"Unknown checkpoint: {checkpoint_name}")
                    else:
                        self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}")
            self.i += 1

    def say(self, *args):
        output = []
        for arg in args:
            if arg.startswith('$'):
                var_name = arg[1:]
                if var_name in self.variables:
                    output.append(self.variables[var_name])
                else:
                    output.append(arg)
            else:
                output.append(arg)
        print(' '.join(output))

    def wait(self, seconds):
        time.sleep(float(seconds))
        
    def jsonread(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None

    def jsonwrite(self, file_path, data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error writing to file: {e}")

    def import_all(self):
        import os
        import sys
        
    def msg(self, *args):
        root = tk.Tk()
        root.withdraw()  # Verstecke das Hauptfenster

        if len(args) < 2:
            print("Usage: msg <type> <text>")
            root.destroy()
            return

        msg_type = args[0]
        text = ' '.join(args[1:])

        if msg_type == 'critical':
            messagebox.showerror('Critical', text)
        elif msg_type == 'warning':
            messagebox.showwarning('Warning', text)
        elif msg_type == 'question':
            messagebox.askquestion('Question', text)
        else:
            messagebox.showinfo('Info', text)
        
    def kill(self, image_name):
        taskk = f'taskkill /f /im {image_name}'
        os.system(taskk)
        
    def msgapp(self, app, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name=app,
            app_icon=None
        )

    def do(self, func_name):
        if func_name in self.functions:
            self.functions[func_name]()
        else:
            print(f"Unknown function: {func_name}")
    
    def url(self, url):
        webbrowser.open(url)
    
    def generate_password(self, length):
        try:
            length = int(length)  # Ensure length is converted to an integer
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(length))
            self.variables['password'] = password
            print(f"Generated password: {password}")
        except ValueError:
            print(f"Error: Length '{length}' is not a valid integer.")
		
    def resolve_variable(self, var_name):
        if var_name.startswith('$'):
            return self.variables.get(var_name[1:], var_name)  # Resolve variable excluding $
        return var_name

    def checkread(self, output_variable, var_name, file_path):
        try:
            found = False
            var_name = self.resolve_variable(var_name)
            with open(file_path, 'r') as file:
                for line in file:
                    if var_name in line:
                        found = True
                        break
            if found:
                self.variables[output_variable] = "1"
            else:
                self.variables[output_variable] = "0"
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            self.variables[output_variable] = "0"
        except Exception as e:
            print(f"Error: {e}")
            self.variables[output_variable] = "0"

    def perform_operation_on_files(self, directory, operation, *args):
        if operation not in ['delete', 'open', 'hash']:
            print(f"Operation '{operation}' not supported.")
            return
        
        files = os.listdir(directory)
        for file_name in files:
            file_path = os.path.join(directory, file_name)
            if operation == 'delete':
                self.delete(file_path)
            elif operation == 'open':
                self.open(file_path)
            elif operation == 'hash':
                self.hash(file_path)

    def readline(self, var_name, file_path_or_file_name, line_number):
        try:
            with open(file_path_or_file_name, 'r') as f:
                lines = f.readlines()
                line_number = int(line_number)
                if 1 <= line_number <= len(lines):
                    self.variables[var_name] = lines[line_number - 1].strip()
                else:
                    print(f"Line number {line_number} is out of range for file {file_path_or_file_name}")
        except FileNotFoundError:
            print(f"File not found: {file_path_or_file_name}")
        except Exception as e:
            print(f"Error reading file: {e}")
            
        
    def hashvar(self, var_name, file_or_path_or_var):
        try:
            if os.path.isfile(file_or_path_or_var):  # Fall: Dateiname oder vollständiger Pfad zur Datei
                with open(file_or_path_or_var, 'rb') as f:
                    content = f.read()
                    hash_object = hashlib.sha256(content)
                    self.variables[var_name] = hash_object.hexdigest()
            elif os.path.isabs(file_or_path_or_var):  # Fall: Absoluter Pfad
                with open(file_or_path_or_var, 'rb') as f:
                    content = f.read()
                    hash_object = hashlib.sha256(content)
                    self.variables[var_name] = hash_object.hexdigest()
            elif file_or_path_or_var.startswith('$'):  # Fall: Variable
                var_name_file = file_or_path_or_var[1:]  # Entferne das '$' Zeichen
                if var_name_file in self.variables and os.path.isfile(self.variables[var_name_file]):
                    file_path = self.variables[var_name_file]
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        hash_object = hashlib.sha256(content)
                        self.variables[var_name] = hash_object.hexdigest()
                else:
                    print(f"Error: Variable '{var_name_file}' does not exist or does not point to a valid file.")
                    self.variables[var_name] = ""
            else:
                print(f"Error: Invalid file or path '{file_or_path_or_var}'.")
                self.variables[var_name] = ""
        except FileNotFoundError:
            print(f"Error: File '{file_or_path_or_var}' not found.")
            self.variables[var_name] = ""
        except Exception as e:
            print(f"Error: {e}")
            self.variables[var_name] = ""

    def down(self, url1, path):
        response = requests.get(url1)
        with open(path, 'wb') as file:
            file.write(response.content)
            
    def clean(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def comment(self, *args):
        pass
        
    def ipget(self):
        os.system('ipconfig' if os.name == 'nt' else 'ifconfig')
        
    def netipget(self):
        os.system('curl ifconfig.me')
        
    def netstat(self):
        if sys.platform.startswith('win'):
            os.system('netstat -ano')
        elif sys.platform.startswith('linux'):
            os.system('netstat -tulpn')
            
    def zip(self, file_paths, zip_file):
        with zipfile.ZipFile(zip_file, 'w') as zf:
            for file in file_paths:
                zf.write(file)

    def unzip(self, zip_file, extract_dir):
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(extract_dir)
            
    def env(self, *args):
        if args[0] == 'set':
            var_name = args[1]
            var_value = args[2]
            os.environ[var_name] = var_value
        elif args[0] == 'get':
            var_name = args[1]
            print(os.environ.get(var_name, ''))
        elif args[0] == 'list':
            for var, val in os.environ.items():
                print(f"{var}={val}")
        else:
            print("Unknown sub-command for 'env'")

    def size(self, file_path):
        size_bytes = os.path.getsize(file_path)
        print(f"Size of {file_path}: {size_bytes} bytes")

    def listdir(self, dir_path):
        contents = os.listdir(dir_path)
        for item in contents:
            print(item)

    def rename(self, old_name, new_name):
        os.rename(old_name, new_name)

    def move(self, src, dst):
        shutil.move(src, dst)
    
    def shutdown(self, time):
        c2 = f'shutdown /s /t {time}'
        os.system(c2)
        
    def rboot(self, time):
        c = f'shutdown /r /t {time}'
        os.system(c)

    def copy(self, src, dst):
        shutil.copy(src, dst)

    def curl(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")

    def create_function(self, func_body):
        def func():
            for line in func_body:
                parts = line.split()
                command = parts[0]
                args = parts[1:]
                if command in self.commands:
                    self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}")
        return func

    def delete(self, file_path):
        os.remove(file_path)

    def open(self, file_path):
        os.startfile(file_path)

    def end(self):
        sys.exit(0)
    
    def if_(self, *args):
        condition = ' '.join(args)  # Die Bedingung aus den Argumenten erstellen
        if self.evaluate_condition(condition):  # Überprüfen, ob die Bedingung wahr ist
            self.i += 1  # Zur nächsten Zeile wechseln
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line.startswith('elif '):
                    break  # Wenn ein elif gefunden wird, wird die Schleife beendet
                elif line == 'else' or line == 'end':
                    break  # Wenn else oder end gefunden wird, wird die Schleife beendet
                self.execute_line(line)  # Die aktuelle Zeile ausführen
                self.i += 1  # Zur nächsten Zeile wechseln
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line == 'end':
                    break  # Wenn end gefunden wird, wird die Schleife beendet
                self.i += 1  # Zur nächsten Zeile wechseln
        else:
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line.startswith('elif '):
                    self.elif_(line[5:].strip())  # Die elif Bedingung ausführen
                    break
                elif line == 'else':
                    self.else_()  # Die else Methode aufrufen
                    break
                elif line == 'end':
                    break
                self.i += 1  # Zur nächsten Zeile wechseln
    
    def elif_(self, *args):
        condition = ' '.join(args)  # Die Bedingung aus den Argumenten erstellen
        if self.evaluate_condition(condition):  # Überprüfen, ob die Bedingung wahr ist
            self.i += 1  # Zur nächsten Zeile wechseln
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line.startswith('elif '):
                    break  # Wenn ein elif gefunden wird, wird die Schleife beendet
                elif line == 'else' or line == 'end':
                    break  # Wenn else oder end gefunden wird, wird die Schleife beendet
                self.execute_line(line)  # Die aktuelle Zeile ausführen
                self.i += 1  # Zur nächsten Zeile wechseln
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line == 'end':
                    break  # Wenn end gefunden wird, wird die Schleife beendet
                self.i += 1  # Zur nächsten Zeile wechseln
        else:
            while self.i < len(self.lines):
                line = self.lines[self.i].strip()
                if line == 'else':
                    self.else_()  # Die else Methode aufrufen
                    break
                elif line == 'end':
                    break
                self.i += 1  # Zur nächsten Zeile wechseln
    
    def else_(self):
        self.i += 1  # Zur nächsten Zeile wechseln
        while self.i < len(self.lines):
            line = self.lines[self.i].strip()
            if line == 'end':
                break  # Wenn end gefunden wird, wird die Schleife beendet
            self.execute_line(line)  # Die aktuelle Zeile ausführen
            self.i += 1  # Zur nächsten Zeile wechseln
            
    def thisis(self, var_name, value):
        self.variables[var_name] = value

    def term(self, *args):
        command = []
        for arg in args:
            if arg.startswith('$'):
                var_name = arg[1:]
                if var_name in self.variables:
                    command.append(self.variables[var_name])
                else:
                    command.append(arg)
            else:
                command.append(arg)
        os.system(' '.join(command))

    def ran(self):
        return str(random.randint(1, 10000))

    def evaluate_condition(self, condition):
        parts = condition.split()
        if len(parts) != 3:
            print(f"Invalid condition format: {condition}")
            return False
        left = parts[0][1:] if parts[0].startswith('$') else parts[0]
        operator = parts[1]
        right = parts[2][1:] if parts[2].startswith('$') else parts[2]
        
        left = self.variables.get(left, left)
        right = self.variables.get(right, right)
        
        if operator == '=':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '>=':
            return left >= right
        elif operator == '<=':
            return left <= right
        else:
            print(f"Unknown operator: {operator}")
            return False

    def execute_line(self, line):
        parts = line.split()
        command = parts[0]
        args = parts[1:]
        if command in self.commands:
            self.commands[command](*args)
        else:
            print(f"Unknown command: {command}")

    def point(self, checkpoint_name):
        pass  # handled in execute_script method

    def returnto(self, checkpoint_name):
        pass  # handled in execute_script method

    def set(self, *args):
        if args[0] == '/ui':
            var_name = args[1]
            user_input = input()
            self.variables[var_name] = user_input
        else:
            var_name = args[0]
            value = ' '.join(args[1:])  # Corrected here
            self.variables[var_name] = value

    def write(self, file_path, *args):
        output = []
        for arg in args:
            if arg.startswith('$'):
                var_name = arg[1:]
                if var_name in self.variables:
                    output.append(self.variables[var_name])
                else:
                    output.append(arg)
            else:
                output.append(arg)
        with open(file_path, 'a') as f:
            f.write(' '.join(output) + '\n')
            
    def fileclear(self, file_path):
        with open(file_path, 'w') as f:
            f.truncate(0)
        print(f"Cleared contents of {file_path}")
        
    def checksing(self, file_path):
        # Read the file content
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Extract the signer's certificate from the file (assuming PEM format)
        try:
            signer_cert = x509.load_pem_x509_certificate(file_data, default_backend())
        except ValueError as e:
            print(f"Error loading certificate from file: {e}")
            return

        # Verify if the signer's certificate is issued by a trusted CA
        if self.validate_certificate(signer_cert):
            print(f"{file_path} has a valid signature.")
        else:
            print(f"{file_path} does not have a valid signature.")

    def validate_certificate(self, cert):
        # Example validation: Check if the certificate is issued by a trusted CA
        # For simplicity, checking if the certificate is self-signed
        try:
            cert.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm,
            )
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def makedir(self, dir_path):
        if dir_path.startswith('$'):
            var_name = dir_path[1:]
            if var_name in self.variables:
                os.makedirs(self.variables[var_name], exist_ok=True)
            else:
                print(f"Unknown variable: {var_name}")
        else:
            os.makedirs(dir_path, exist_ok=True)

    def read(self, file_path, var_name):
        with open(file_path, 'r') as f:
            content = f.read()
            self.variables[var_name] = content

    def hash(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            hash_object = hashlib.sha256(content)
            print(hash_object.hexdigest())

    def userinput(self, *args):
        pass
        
    def uinbox(self, *args):
        if self.root is None:
            self.root = tk.Tk()
        title = " ".join(map(str, args))
        self.root.title(title)
        
    def uinsay(self, name, *args):
        test = " ".join(map(str, args))
        name = tk.Label(self.root, text=test)
        name.pack()
        
    def uinbutten(self, name, command, *args):
        teste = " ".join(map(str, args))
        name = tk.Button(self.root, text=teste, command=command)
        name.pack()
        
    def runuinbox(self):
        self.root.mainloop()
        
    def uinenter(self, name):
        name = tk.Entry(self.root)
        name.pack()
        
    def uinsay(self, name, *args):
        test = " ".join(map(str, args))
        name = tk.Label(self.root, text=test)
        name.pack()
        
    def uincheck(self, name, *args):
        test = " ".join(map(str, args))
        name = tk.Checkbutton(self.root, text=test)
        name.pack()
        
    def uinradio(self, name, *args):
        test = " ".join(map(str, args))
        name = tk.Radiobutton(self.root, text=test)
        name.pack()
        
    def uinlist(self, name):
        name = tk.Listbox(self.root)
        name.pack()
    
    def uinscale(self, name):
        name = tk.Scale(self.root)
        name.pack()
    
    def randomnum(self, min_val, max_val):
        random_number = random.randint(int(min_val), int(max_val))
        print(random_number)
        return random_number
        
    def progressbar(self, size, speed, *args):
        title = " ".join(map(str, args))
        class ProgressBar(tk.Tk):
            def __init__(self):
                super().__init__()
                self.title(title)
                self.geometry(size)
                self.progress = tk.DoubleVar()
                self.progress_bar = ttk.Progressbar(self, variable=self.progress, maximum=100)
                self.progress_bar.pack(pady=20)
                self.button = tk.Button(self, text="Stop", command=self.stop_thread)
                self.button.pack(pady=20)
                self._stop_event = threading.Event()
                self.thread = None
                self.speed = float(speed)
                self.start_thread()
            def update_progress(self, value):
                self.progress.set(value)
            def start_thread(self):
                if self.thread is None or not self.thread.is_alive():
                    self._stop_event.clear()
                    self.thread = threading.Thread(target=self.update_progress_slowly)
                    self.thread.start()
            def update_progress_slowly(self):

                for i in range(101):
                    if self._stop_event.is_set():
                        break

                    time.sleep(self.speed)
                    self.after(0, self.update_progress, i)
                self.button.config(state=tk.DISABLED)
            def stop_thread(self):
                if self.thread is not None and self.thread.is_alive():
                    self._stop_event.set()
                    self.thread.join()
                    self.thread = None
                    self.button.config(state=tk.NORMAL)
        if __name__ == "__main__":
            app = ProgressBar()
            app.mainloop()

    def random_command(self, *args):
        random_choice = random.choice(args)
        print(random_choice)
        return random_choice
        
    def compare(self, fileno1, fileno2, fileno3):
        def compare_files(file1_path, file2_path, output_path):
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                file1_lines = file1.readlines()
                file2_lines = file2.readlines()

            differences = []

            max_lines = max(len(file1_lines), len(file2_lines))

            for i in range(max_lines):
                line1 = file1_lines[i].strip() if i < len(file1_lines) else ''
                line2 = file2_lines[i].strip() if i < len(file2_lines) else ''

                if line1 != line2:
                    differences.append(f"Line {i + 1}: File 1: '{line1}' <> File 2: '{line2}'")

            with open(output_path, 'w') as output_file:
                if differences:
                    output_file.write("\n".join(differences))
                else:
                    output_file.write("The files are the same.")

        if __name__ == "__main__":
            file1_path = fileno1
            file2_path = fileno2
            output_path = fileno3
            compare_files(file1_path, file2_path, output_path)

    def randomvar(self, var_name, *args):
        random_choice = random.choice(args)
        self.variables[var_name] = random_choice

    def randomnumvar(self, var_name, min_val, max_val):
        random_number = random.randint(int(min_val), int(max_val))
        self.variables[var_name] = str(random_number)
    
    def add(self, var_name, *args):
        result = sum(float(self.variables[arg[1:]]) if arg.startswith('$') else float(arg) for arg in args)
        self.variables[var_name] = str(result)

    def subtract(self, var_name, *args):
        result = float(self.variables[args[0][1:]]) if args[0].startswith('$') else float(args[0])
        for arg in args[1:]:
            result -= float(self.variables[arg[1:]]) if arg.startswith('$') else float(arg)
        self.variables[var_name] = str(result)
        
    def multiply(self, var_name, *args):
        result = float(self.variables[args[0][1:]]) if args[0].startswith('$') else float(args[0])
        for arg in args[1:]:
            result *= float(self.variables[arg[1:]]) if arg.startswith('$') else float(arg)
        self.variables[var_name] = str(result)

    def divide(self, var_name, *args):
        result = float(self.variables[args[0][1:]]) if args[0].startswith('$') else float(args[0])
        for arg in args[1:]:
            divisor = float(self.variables[arg[1:]]) if arg.startswith('$') else float(arg)
            if divisor == 0:
                print("Error: Division by zero.")
                return
            result /= divisor
        self.variables[var_name] = str(result)

    def concat(self, var_name, *args):
        result = ''.join(self.variables[arg[1:]] if arg.startswith('$') else arg for arg in args)
        self.variables[var_name] = result

    def upper(self, var_name, var_to_upper):
        if var_to_upper.startswith('$'):
            self.variables[var_name] = self.variables[var_to_upper[1:]].upper()
        else:
            self.variables[var_name] = var_to_upper.upper()
            
    def lower(self, var_name, var_to_lower):
        if var_to_lower.startswith('$'):
            self.variables[var_name] = self.variables[var_to_lower[1:]].lower()
        else:
            self.variables[var_name] = var_to_lower.lower()

    def replace(self, var_name, var_to_modify, old, new):
        if var_to_modify.startswith('$'):
            self.variables[var_name] = self.variables[var_to_modify[1:]].replace(old, new)
        else:
            self.variables[var_name] = var_to_modify.replace(old, new)
            
    def current_time(self, var_name):
        self.variables[var_name] = datetime.now().strftime("%H:%M:%S")

    def current_date(self, var_name):
        self.variables[var_name] = datetime.now().strftime("%Y-%m-%d")

    def sleep_until(self, time_str):
        target_time = datetime.strptime(time_str, "%H:%M:%S").time()
        now = datetime.now()
        target_datetime = datetime.combine(now.date(), target_time)
        if target_datetime < now:
            target_datetime = datetime.combine(now.date() + timedelta(days=1), target_time)
        time.sleep((target_datetime - now).total_seconds())
        
    def copydir(self, src, dst):
        shutil.copytree(src, dst)

    def deldir(self, dir_path):
        shutil.rmtree(dir_path)

    def fileinfo(self, file_path):
        info = os.stat(file_path)
        print(f"File: {file_path}")
        print(f"Size: {info.st_size} bytes")
        print(f"Created: {time.ctime(info.st_ctime)}")
        print(f"Modified: {time.ctime(info.st_mtime)}")
        print(f"Accessed: {time.ctime(info.st_atime)}")
        
    def ping(self, host):
        response = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE)
        print(response.stdout.decode())

    def traceroute(self, host):
        response = subprocess.run(['traceroute', host], stdout=subprocess.PIPE)
        print(response.stdout.decode())

    def sysinfo(self):
        print("System:", platform.system())
        print("Node Name:", platform.node())
        print("Release:", platform.release())
        print("Version:", platform.version())
        print("Machine:", platform.machine())
        print("Processor:", platform.processor())

    def cpuinfo(self):
        if sys.platform == "win32":
            os.system("wmic cpu get caption, deviceid, name, numberofcores, maxclockspeed, status")
        elif sys.platform == "linux":
            os.system("lscpu")

    def meminfo(self):
        if sys.platform == "win32":
            os.system("systeminfo | findstr /C:'Total Physical Memory'")
        elif sys.platform == "linux":
            os.system("free -h")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fabiskript.py <script_file.fs>")
        sys.exit(1)
    script_file = sys.argv[1]
    if not script_file.endswith('.fs'):
        print("Script file must end with .fs")
        sys.exit(1)
    fabi_skript = FabiSkript()
    fabi_skript.run_script(script_file)
