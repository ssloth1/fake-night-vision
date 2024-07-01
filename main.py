# Author: James Bebarski
# Date: June 12, 2024

import cv2
import numpy as np

"""
I used a Gaussian blur to create a low-pass image and then subtracted that from the original image to create a high-pass image.
From there you can adjust the contrast and brightness of the high-pass image and apply it to a color channel of your choice.
The sliders made things a whole lot easier to see the effect in real-time instead of filling in the parameters manually and running the script each time.

For reference when you are making your own night vision effect with the sliders via the cv2 GUI window:
- The kernel sizes go from 3x3 to 15x15, with all odds in between
- alpha is the contrast adjustment, it goes from 0 to 10 to keep it simple
- beta is the brightness adjustment, it goes from 0 to 255
- color channel is the channel that the contrast adjustment is applied to, 0 is blue, 1 is green, 2 is red (by default it is green, the others don't look good with this effect)

You should see a image of steve harvey that I processed, by default the sliders are set to the values that I found looked the best for this image.
If you want to save the image, press 's' and it will save the processed image to the images folder as 'processed.jpg'
Any other key will close the window and end the program.

If you want to try this with your own image, just change the image path in the ImageProcessor class to the path of your image.
"""

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.kernel_sizes = [3, 5, 7, 9, 11, 13, 15]
        self.ksize_index = 0
        self.alpha = 1
        self.beta = 0
        self.color_channel = 1

    def process_image(self):
        # get the kernel size based on the index
        ksize = self.kernel_sizes[self.ksize_index]

        # calculate the sigma (gaussian standard deviation) based on the kernel size
        # I found this to be quite difficult and after a lot of research looking for a openCV function that would just make it work...
        # eventually, I stumbled upon this formula while going through openCV documentation on geekforgeeks
        # https://www.geeksforgeeks.org/python-opencv-getgaussiankernel-function/
        sigma = 0.3 * ((ksize - 1) * 0.5 - 1) + 0.8
        
        # apply Gaussian blur with the specified kernel size and calculated sigma from above
        low_pass = cv2.GaussianBlur(self.image, (ksize, ksize), sigma)
        high_pass = cv2.subtract(self.image, low_pass) # Subtract the low-pass image from the original image

        # apply contrast to the high-pass image
        high_pass_contrast = cv2.convertScaleAbs(high_pass, alpha=self.alpha, beta=self.beta)

        # create a 3-channel image with the high-pass contrast in the specified color channel (default is green)
        colored_image = np.zeros((self.image.shape[0], self.image.shape[1], 3), dtype=np.uint8)
        colored_image[:, :, self.color_channel] = high_pass_contrast

        return colored_image

def on_trackbar_change(value):
    global processor
    try:
        # check if the window exists before getting trackbar positions
        if cv2.getWindowProperty('Image Processor', cv2.WND_PROP_VISIBLE) >= 1:
            processor.ksize_index = cv2.getTrackbarPos('Kernel Size', 'Image Processor')
            processor.alpha = cv2.getTrackbarPos('Alpha', 'Image Processor')
            processor.beta = cv2.getTrackbarPos('Beta', 'Image Processor')
            processor.color_channel = cv2.getTrackbarPos('Color Channel', 'Image Processor')
            processed_image = processor.process_image()
            cv2.imshow('Image Processor', processed_image)
    except cv2.error as e:
        print(f"Trackbar error: {e}")


def main():

    global processor
    processor = ImageProcessor("images/steve.jpg")

    # create a window
    cv2.namedWindow('Image Processor')

    # create trackbars
    cv2.createTrackbar('Kernel Size', 'Image Processor', 4, len(processor.kernel_sizes) - 1, on_trackbar_change)
    cv2.createTrackbar('Alpha', 'Image Processor', 4, 10, on_trackbar_change)
    cv2.createTrackbar('Beta', 'Image Processor', 10, 255, on_trackbar_change)
    cv2.createTrackbar('Color Channel', 'Image Processor', 1, 2, on_trackbar_change)

    # set initial values for the trackbars
    cv2.setTrackbarPos('Kernel Size', 'Image Processor', processor.ksize_index)
    cv2.setTrackbarPos('Alpha', 'Image Processor', processor.alpha)
    cv2.setTrackbarPos('Beta', 'Image Processor', processor.beta)
    cv2.setTrackbarPos('Color Channel', 'Image Processor', processor.color_channel)

    # show initial processed image
    processed_image = processor.process_image()
    cv2.imshow('Image Processor', processed_image)

    # while the program is running, check for any key press events (s to save, any other key to exit)
    while True:
        key = cv2.waitKey(1)
        if key == ord('s'):
            save_path = "images/processed.jpg"
            cv2.imwrite(save_path, processed_image)
            print(f"Image saved to {save_path}")
        elif key != -1:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
