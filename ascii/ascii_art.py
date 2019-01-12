from PIL import Image
import math
import cv2
import sys

replacement = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^\'.'


def scale_photo(image, new_width=200):
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width)
    scaled_image = image.resize((new_width, new_height))
    return scaled_image


def convert_to_gray(image):
    return image.convert('L')


def calc_gray_value(pixel):
    r, g, b = pixel
    gray = int(0.21 * r + 0.72 * g + 0.07 * b)
    return (gray, gray, gray)


def manual_grayscale(image):
    pixels = list(image.getdata())
    new_pixy = [calc_gray_value(pixel) for pixel in pixels]
    return new_pixy


def constrast_update(image, constant):
    F = 259 * (constant + 255) / (255 * (259 - constant))
    return image.point(lambda x: 128 + F * (x - 128))


def map_to_ascii(image):
    pixels = list(image.getdata())
    size = len(replacement) - 1
    converted = [replacement[math.ceil((size) * indy / 255)] for indy in pixels]
    return "".join(converted)


def pixel_to_ascii(image):
    image = scale_photo(image)
    image = convert_to_gray(image)

    asciiz = map_to_ascii(image)
    len_ascii = len(asciiz)
    final_ascii = [asciiz[index:index + 200] for index in range(0, len_ascii, 200)]
    return "\n".join(final_ascii)


def video_to_ascii():
    # uses opencv to handle the video
    cap = cv2.VideoCapture(0)
    while (True):
        ret, frame = cap.read()

        # Our operations on the frame come here
        pilly = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print(pixel_to_ascii(Image.fromarray(pilly)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def image_to_ascii(path):
    new_image = pixel_to_ascii(Image.open(path))
    with open("ascii_output", "w+") as f:
        f.write(new_image)


if __name__ == '__main__':
    # if using the video, pass a dummy string for the file
    path = sys.argv[1]
    medium_type = sys.argv[2]
    if int(medium_type) is 1:
        image_to_ascii(path)
    elif int(medium_type) is 2:
        video_to_ascii()
