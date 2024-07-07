import sys

# Define the decryption cipher based on the provided mapping
cipher = {
    'e': 'j', 'm': 'w', 'i': 'i', '3': 'n', 'r': 'c', '8': 'l', 'u': '9', 'd': 'a',
    'n': 's', '9': 'b', 's': 'u', 'a': '7', '7': 'd', 'k': 'e', '5': 'f', '2': 'g',
    '1': 'h', 'z': 'm', 'x': 'o', '0': 'p', 'w': 'q', 'v': 'r', 'c': 't', 'b': 'v',
    'o': 'x', 'p': 'y', 'q': 'z', 'f': '1', 'g': '2', 'h': '3', 'j': '4', 'k': 'k', 
    't': '8', '6': 'e'
}

# Function to decrypt the content
def decrypt(content):
    decrypted_content = ''.join(cipher.get(char, char) for char in content)
    return decrypted_content

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    if not input_filename.endswith('_encrypted.txt'):
        print("Error: This script expects an input file ending with '_encrypted.txt'.")
        sys.exit(1)

    output_filename = input_filename.replace('_encrypted.txt', '_decrypted.txt')

    try:
        with open(input_filename, 'r') as file:
            content = file.read()

        decrypted_content = decrypt(content)

        with open(output_filename, 'w') as file:
            file.write(decrypted_content)

        print(f"File '{input_filename}' has been decrypted and saved as '{output_filename}'.")

    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
