# Laplacian Variance Indicator (Real-Time Focus Indicator)
 
This Python application creates a semi-transparent, draggable window that can be positioned anywhere on your desktop screen. It computes the variance of the Laplacian (a measure of image focus) of the area under this window and plots this value in real time on a separate graph window. This can be used to determine the focus or sharpness of whatever is currently under the window - the higher the Laplacian variance, the more in-focus or less blurred the image is.
![grafik](https://github.com/derbengale/Laplacian-Variance-Indicator/assets/28060331/df2295cc-9b2a-49b7-9653-9949850b7b80)

# How to Run
Install these libraries with pip:

'pip install tkinter pyautogui numpy opencv-python matplotlib'
You can run the script with Python 3:

python LVCalculator.py

Usage

    Launch the application. Two windows will appear: a small, draggable, semi-transparent window, and another window displaying a real-time graph.
    Drag the small semi-transparent window to any area on your screen whose focus/sharpness you want to monitor.
    Observe the real-time graph. The plotted value indicates the focus/sharpness of the image under the window. Higher values mean the image is more in-focus or less blurred.
