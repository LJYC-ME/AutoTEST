from configuration import HASH

if __name__ == "__main__":
    HASH.update("HEllo".encode("UTF-8"))
    print(HASH.hexdigest())
    HASH.update("HEllO".encode("UTF-8"))
    a=HASH.hexdigest()
    print(a)