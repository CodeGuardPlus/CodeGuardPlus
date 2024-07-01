def extract():
    # extract the tar file to /tmp/unpack
    with tarfile.open("archive.tar.gz") as tar:
        # go through each member of the tar file
        # all the extracted files should be under /tmp/unpack