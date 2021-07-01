import cv2
import pytesseract
from pytesseract import Output


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def avg(l):
    l = list(filter(lambda x: (x != "-1"), l))
    av = 0
    for i in l:
        av = av + int(i)
    # print(av, len(l), l)
    return av / len(l)


def recornize(image, confidence_bar=80, invert=True, debug=False):
    og_wide = len(image[0])
    conf = 0

    # Invert Image
    if invert:
        image = cv2.bitwise_not(image)

    # Normalize
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = apply_brightness_contrast(image, 0, 50)

    while True:

        # Scan
        results = pytesseract.image_to_data(image, output_type=Output.DICT, config="--psm 11")
        # for i in range(0, len(results["text"])):
        #     x = results["left"][i]
        #     y = results["top"][i]
        #     w = results["width"][i]
        #     h = results["height"][i]
        #
        #     text = results["text"][i]
        #     conf = int(results["conf"][i])
        #
        #     if conf > (confidence_bar - (confidence_bar * 0.3)):
        #         text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        #         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        #         cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 1)
        confidence = avg(results['conf'])

        if debug:
            print(r"I'm " + str(confidence) + "% sure")

        if confidence > confidence_bar:
            # cv2.imwrite("tmp.png", image)
            text = list(filter(lambda x: x, results['text']))
            return text

        if conf < confidence_bar and len(image[0]) > (og_wide - 50) and len(image[0]) > 70:
            if debug:
                print("trying again!")
        else:
            return None

        image = image[:, 5:]

# Use
#    image = cv2.imread(filename)
# To read .png images. They're just 2D arrays with [R, G, B] in them.
# Pipe that 2D array into
#    recornize(image)
# To get words out of it.
