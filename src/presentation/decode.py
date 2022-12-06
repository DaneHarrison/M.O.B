import threading, json, base64, sys


def read_image(photo):
    photo = photo.encode('utf-8')
    photo = base64.decodebytes(photo)

    return photo

if __name__ == '__main__':
    photo = sys.argv[1]
    photo = read_image(photo)
    print(photo)