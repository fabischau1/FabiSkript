import os
import sys
import time
import random
import hashlib

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
            'else if': self.else_if,
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
            '/ui': self.userinput
        }
        self.functions = {}
        self.variables = {}
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

    def import_all(self):
        import os
        import sys

    def do(self, func_name):
        if func_name in self.functions:
            self.functions[func_name]()
        else:
            print(f"Unknown function: {func_name}")

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
        condition = ' '.join(args)
        if self.evaluate_condition(condition):
            self.i += 1
            while self.i < len(self.lines) and self.lines[self.i].strip() not in ('else', 'else if', 'end'):
                self.execute_line(self.lines[self.i].strip())
                self.i += 1
            if self.i < len(self.lines) and self.lines[self.i].strip() == 'else':
                while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                    self.i += 1
        else:
            while self.i < len(self.lines) and self.lines[self.i].strip() not in ('else', 'else if', 'end'):
                self.i += 1
            if self.i < len(self.lines) and self.lines[self.i].strip() == 'else':
                self.i += 1
                while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                    self.execute_line(self.lines[self.i].strip())
                    self.i += 1

    def else_(self, *args):
        self.i += 1
        while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
            self.execute_line(self.lines[self.i].strip())
            self.i += 1

    def else_if(self, *args):
        condition = ' '.join(args)
        if not self.evaluate_condition(condition):
            while self.i < len(self.lines) and self.lines[self.i].strip() not in ('else', 'else if', 'end'):
                self.i += 1
            if self.i < len(self.lines) and self.lines[self.i].strip() == 'else':
                self.i += 1
                while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                    self.execute_line(self.lines[self.i].strip())
                    self.i += 1
        else:
            self.i += 1
            while self.i < len(self.lines) and self.lines[self.i].strip() != 'end':
                self.execute_line(self.lines[self.i].strip())
                self.i += 1

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
        pass  # removed this method as it's now handled in the set method

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
