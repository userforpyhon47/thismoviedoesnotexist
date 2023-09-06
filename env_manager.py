import os

def load_credentials():
    with open (".env") as file:
        for line in file.readlines():
            data = line.strip().split("=", maxsplit=1)
            os.environ[data[0]] = data [1]

if __name__ == "__main__":
    load_credentials()