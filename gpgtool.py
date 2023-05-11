#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#   gpgtool.py
#   
#   Chatgpt did most of the typing. Then I refactored + fixed bugs myself.
# 
#

import subprocess
import curses
import os
import base64


def select_file(prompt):
    current_dir = os.getcwd()

    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Create a file selection dialog using curses
    stdscr.addstr(0, 0, prompt)
    stdscr.addstr(1, 0, current_dir)

    file_list = os.listdir(current_dir)
    selected_file_index = 0

    while True:
        for i, file_name in enumerate(file_list):
            x = 2 + i
            y = 0
            if i == selected_file_index:
                stdscr.addstr(x, y, " > " + file_name + " < ")
            else:
                stdscr.addstr(x, y, "   " + file_name + "   ")

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_file_index > 0:
            selected_file_index -= 1
        elif key == curses.KEY_DOWN and selected_file_index < len(file_list) - 1:
            selected_file_index += 1
        elif key == ord('\n'):
            break

    selected_file = file_list[selected_file_index]
    file_path = os.path.join(current_dir, selected_file)

    # Restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    return file_path


def run_gpg_command(args):
    command = ['gpg'] + args
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"GnuPG command execution failed: {e.stderr}") from e


def list_keys():
    output, error = run_gpg_command(['--list-keys', '--with-colons'])
    keys = []
    if output:
        key_lines = output.strip().split('\n')
        key_info = []
        current_key = []
        for line in key_lines:
            line_parts = line.split(':')
            record_type = line_parts[0]
            if record_type == 'pub':
                if current_key:
                    key_info.append(current_key)
                current_key = [line]
            else:
                current_key.append(line)
        if current_key:
            key_info.append(current_key)

        for key in key_info:
            key_parts = key[0].split(':')
            key_id = key_parts[4]
            uid_lines = [line for line in key if line.startswith('uid')]
            if uid_lines:
                uid_parts = uid_lines[0].split(':')
                name_parts = uid_parts[9].split('(')
                real_name = name_parts[0].strip()
                if len(name_parts) > 1:
                    email_comment = name_parts[1].strip().rstrip(
                        ')').strip().strip('<>')
                else:
                    email_comment = name_parts[0]

                comment, email = email_comment.split(
                    "<", maxsplit=1) if "<" in email_comment else ("", "")
                comment = comment.strip().rstrip(')')
                keys.append((real_name, key_id, email, comment))

    if keys:
        print("\nAvailable GPG keys:")
        for i, key in enumerate(keys, start=1):
            name, key_id, email, comment = key
            print(f"{i}. Key ID: {key_id}")
            print(f"   Name: {name}")
            print(f"   Email: {email}")
            print(f"   Comment: {comment}")
            print()
    else:
        print("No GPG keys found.")

    return keys


def create_key():
    name = input("Enter the name for the key: ")
    email = input("Enter the email address for the key: ")
    comment = input(
        "Enter an optional comment for the key (leave empty for none): ")
    passphrase = input("Enter a passphrase for the key: ")

    try:
        run_gpg_command(['--batch', '--passphrase', passphrase,
                        '--quick-gen-key', f"{name} <{email}> {comment}"])
        print("GPG key created successfully.")
    except RuntimeError as e:
        print("Key creation failed:", str(e))


def show_public_key():
    keys = list_keys()
    index = int(
        input("Enter the index number of the key to show the public key: "))
    if index < 1 or index > len(keys):
        print("Invalid key index.")
        return

    key_id = keys[index - 1][1]
    output, _ = run_gpg_command(['--armor', '--export', key_id])
    print("Public Key Block:\n")
    print(output)


def delete_key():
    keys = list_keys()
    index = int(input("Enter the index number of the key to delete: "))
    if index < 1 or index > len(keys):
        print("Invalid key index.")
        return

    key_id = keys[index - 1][1]

    try:
        run_gpg_command(['--delete-secret-and-public-key', key_id])
        print("Key deleted successfully.")
    except RuntimeError as e:
        print("Key deletion failed:", str(e))


def encrypt_file():
    keys = list_keys()
    index = 1
    if len(keys) > 1:
        index = int(
            input("Enter the index number of the key to use for encryption: "))
        if index < 1 or index > len(keys):
            print("Invalid key index.")
            return

    key_id = keys[index - 1][1]
    # file_path = input("Enter the path of the file to encrypt: ")
    file_path = select_file("Select a file to encrypt:")
    output_file = input("Enter the path to save the encrypted file: ")

    try:
        run_gpg_command(['--encrypt', '--recipient', key_id,
                        '--output', output_file, file_path])
        print("File encrypted successfully.")
    except RuntimeError as e:
        print("File encryption failed:", str(e))


def decrypt_file():
    keys = list_keys()
    index = 1
    if len(keys) > 1:
        index = int(
            input("Enter the index number of the key to use for decryption: "))
        if index < 1 or index > len(keys):
            print("Invalid key index.")
            return

    key_id = keys[index - 1][1]
    # file_path = input("Enter the path of the file to decrypt: ")
    file_path = select_file("Select a file to decrypt:")
    output_file = input("Enter the path to save the decrypted file: ")

    try:
        run_gpg_command(['--decrypt', '--recipient', key_id,
                        '--output', output_file, file_path])
        print("File decrypted successfully.")
    except RuntimeError as e:
        print("File decryption failed:", str(e))


# Main loop
keys = []
while True:
    print("\nMenu:")
    print("=====\n")
    print("1. List GPG keys")
    print("2. Create a new GPG key")
    print("3. Show the public key block for a GPG key")
    print("4. Delete a GPG key")
    print("5. Encrypt a file")
    print("6. Decrypt a file")
    print("q. Exit")

    choice = input("Enter your choice (0-6): ")

    if choice == 'q':
        break
    elif choice == '1':
        list_keys()
    elif choice == '2':
        create_key()
    elif choice == '3':
        show_public_key()
    elif choice == '4':
        delete_key()
    elif choice == '5':
        encrypt_file()
    elif choice == '6':
        decrypt_file()
    else:
        print("Invalid choice. Please try again.")
