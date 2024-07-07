import sys

# Define the substitution cipher based on the provided mapping
cipher = {
    'j': 'e', 'w': 'm', '5': 'i', 'n': '3', 'c': 'r', 'l': '8', '9': 'u', 'a': 'd',
    's': 'n', 'b': '9', 'u': 's', '7': 'a', 'd': '7', 'e': '6', 'f': '5', 'g': '2',
    'h': '1', 'm': 'z', 'o': 'x', 'p': '0', 'q': 'w', 'r': 'v', 't': 'c', 'v': 'b',
    'x': 'o', 'y': 'p', 'z': 'q', '1': 'f', '2': 'g', '3': 'h', '4': 'j', '6': 'k', 
    '8': 't'
}

# Function to encrypt the content
def encrypt(content):
    encrypted_content = ''.join(cipher.get(char, char) for char in content)
    return encrypted_content

def main():
    if len(sys.argv) != 2:
        print("Usage: python encrypt.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = input_filename.split('.')[0] + '_encrypted.txt'

    try:
        with open(input_filename, 'r') as file:
            content = file.read()

        encrypted_content = encrypt(content)

        with open(output_filename, 'w') as file:
            file.write(encrypted_content)

        print(f"File '{input_filename}' has been encrypted and saved as '{output_filename}'.")

    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
