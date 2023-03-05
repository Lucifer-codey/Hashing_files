import os
import hashlib
import base64
from cryptography.fernet import Fernet
import secrets


def encrypt_file(file_path, encryption_method):
    if os.path.isfile(file_path):
        # read the contents of the file
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # encrypt the contents of the file using the chosen encryption method
        if encryption_method == 'MD5':
            encryption_key = hashlib.md5(file_data).hexdigest().encode()
        elif encryption_method == 'SHA256':
            encryption_key = hashlib.sha256(file_data).hexdigest().encode()
        elif encryption_method == 'AES':
            encryption_key = secrets.token_bytes(32)
            fernet = Fernet(base64.urlsafe_b64encode(encryption_key))
            file_data = fernet.encrypt(file_data)

        # save the encrypted contents to a new file
        encrypted_file_path = file_path + '.' + encryption_method.lower()
        with open(encrypted_file_path, 'wb') as f:
            f.write(encryption_key)
            f.write(file_data)

        print(f'{file_path} has been encrypted with {encryption_method}')
        print(f'The encrypted file is at {encrypted_file_path}')

    elif os.path.isdir(file_path):
        # recursively encrypt all the files in the directory and its subdirectories
        for root, dirs, files in os.walk(file_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                encrypt_file(file_path, encryption_method)
    else:
        print(f'{file_path} is not a file or directory')


# function to decrypt a file with a given encryption method
def decrypt_file(file_path, encryption_method):
    # read the contents of the encrypted file
    with open(file_path, 'rb') as f:
        encrypted_file_contents = f.read()

    # decrypt the contents of the encrypted file using the chosen encryption method
    if encryption_method == 'MD5' or encryption_method == 'SHA256':
        raise ValueError(f'{encryption_method} is not a valid encryption method for decryption')
    elif encryption_method == 'AES':
        decrypted_file_contents = fernet.decrypt(encrypted_file_contents)
    else:
        raise ValueError('Invalid encryption method')

    # write the decrypted contents of the file to a new file with the original extension
    decrypted_file_path = os.path.splitext(file_path)[0]
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_file_contents)

    print(f'File {file_path} decrypted with {encryption_method} and saved to {decrypted_file_path}')

# function to display a menu of encryption options
def display_encryption_menu():
    print('Choose an encryption method:')
    print('1. MD5')
    print('2. SHA256')
    print('3. AES')

    choice = input('Enter your choice: ')
    if choice == '1':
        return 'MD5'
    elif choice == '2':
        return 'SHA256'
    elif choice == '3':
        return 'AES'
    else:
        raise ValueError('Invalid choice')

# main program loop
while True:
    # display a menu of options
    print('Choose an option:')
    print('1. Encrypt a file')
    print('2. Decrypt a file')
    print('3. Quit')

    choice = input('Enter your choice: ')
    if choice == '1':
        # ask the user for the path to the file to encrypt
        file_path = input('Enter the path to the file to encrypt: ')

        # display a menu of encryption options and ask the user to choose one
        encryption_method = display_encryption_menu()

        # encrypt the file with the chosen encryption method
        encrypt_file(file_path, encryption_method)

    elif choice == '2':
                # ask the user for the path to the file to decrypt
        file_path = input('Enter the path to the file to decrypt: ')

        # get the original extension of the file
        original_extension = os.path.splitext(file_path)[1]

        # display a menu of encryption options and ask the user to choose one
        encryption_method = display_encryption_menu()

        # decrypt the file with the chosen encryption method
        decrypt_file(file_path, encryption_method)

        # rename the decrypted file with the original extension
        decrypted_file_path = os.path.splitext(file_path)[0]
        os.rename(decrypted_file_path, decrypted_file_path + original_extension)

    elif choice == '3':
        # quit the program
        break

    else:
        print('Invalid choice')

