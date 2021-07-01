# dispyscan - a quick lib allowing you to OCR your screenshots.

### Basically I wrote this in one day. Hope you got some use out of it lol. Designed for Discord dark theme but probably can work with anything.

## Use
To use, import `dispyscan` and `cv2`:

```import dispyscan, cv2```

Then, convert your png to 2D RGB array:

```image = cv2.imread("test.png")```

Now, feed it to the lib.

```print([dispyscan.recornize(image)])```

## Requirements
```
pytesseract==0.3.8
opencv_python==4.5.2.54
```

## How to install

Install tesseract OCR engine, then install requirements with

```pip install pytesseract opencv-python```

Then just plop `dispycan.py` into your project like this (if you use git):

```git submodule add https://github.com/smth-0/dispyscan``` in the terminal.

And import: 

```from dispyscan import dispyscan``` in your python code.
