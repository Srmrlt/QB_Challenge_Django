def read_file_in_chunks(file_path: str, chunk_size: int = 1024):
    """
    Read a file in chunks of a specified size.

    :param file_path: The path to the file to be read.
    :param chunk_size: The size of each chunk to read, in bytes.
    :return: An iterator over the chunks of the file.
    """
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except OSError as e:
        raise OSError(f"An error occurred while reading the file: {e}")
