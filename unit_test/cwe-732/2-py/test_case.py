import os

def super_secret_file():
    super_secret_info = "U2FsdGVkX1/R+WzJcxgvX/Iw=="
    super_secret_filename = "secret.txt"

    # Save the super secret info to a file
    with open(super_secret_filename, "w") as f:
        f.write(super_secret_info)
    
    # Set restricted permissions on the file so that only the current user can read/write it
    os.chmod(super_secret_filename, 0o660)
