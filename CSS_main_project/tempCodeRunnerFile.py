from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import secrets

def generate_key(key_length):
    return secrets.token_bytes(key_length)

def encrypt_image(input_image, output_image, key):
    cipher = AES.new(key, AES.MODE_CBC)

    # Read image data
    with open(input_image, 'rb') as file:
        image_data = file.read()

    # Pad the image data to be a multiple of the AES block size
    padded_image_data = pad(image_data, AES.block_size)

    # Encrypt the padded image data
    encrypted_image_data = cipher.encrypt(padded_image_data)

    # Write the IV and encrypted image data to the output file
    with open(output_image, 'wb') as file:
        file.write(cipher.iv)
        file.write(encrypted_image_data)

def decrypt_image(input_image, output_image, key):
    # Read IV and encrypted image data from the input file
    with open(input_image, 'rb') as file:
        iv = file.read(16)
        encrypted_image_data = file.read()

    # Create a cipher object with the IV and key
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the encrypted image data
    decrypted_image_data = unpad(cipher.decrypt(encrypted_image_data), AES.block_size)

    # Write the decrypted image data to the output file
    with open(output_image, 'wb') as file:
        file.write(decrypted_image_data)

def main():
    choice = input("Enter 'E' to encrypt or 'D' to decrypt: ").strip().upper()
    if choice not in ['E', 'D']:
        print("Invalid choice.")
        return

    input_image = input("Enter input image path: ").strip()
    if not os.path.isfile(input_image):
        print("Input image not found.")
        return

    output_image = input("Enter output image path: ").strip()

    key_length = int(input("Enter key length in bytes (16/24/32): ").strip())
    key = generate_key(key_length)

    if choice == 'E':
        encrypt_image(input_image, output_image, key)
        print("Image encrypted successfully.")
    else:
        decrypt_image(input_image, output_image, key)
        print("Image decrypted successfully.")

if __name__ == "__main__":
    main()
