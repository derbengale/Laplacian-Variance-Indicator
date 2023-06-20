import tkinter as tk
import pyautogui
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TransparentWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up attributes for window transparency and decoration
        self.attributes("-alpha", 0.5)
        self.overrideredirect(1)
        self.attributes("-topmost", True)

        # Set up window size and position
        self.window_width = 200
        self.window_height = 200
        self.geometry(f"{self.window_width}x{self.window_height}")

        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (self.window_width / 2))
        center_y = int((screen_height / 2) - (self.window_height / 2))
        self.geometry(f"+{center_x}+{center_y}")

        # Set up canvas
        self.border = 3
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=self.border, highlightbackground="green")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.winfo_toplevel().title("Maximize the value to decrease the Blur")
        # Set up event bindings for mouse drag
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

        # Initialize a FigureCanvasTkAgg and data for the plot
        self.fig = plt.Figure()
        self.graph_window = tk.Toplevel(self)
        self.graph_window.wm_attributes("-topmost", 1)
        self.a = self.fig.add_subplot(111)
        self.mcanvas = FigureCanvasTkAgg(self.fig, master=self.graph_window)
        self.mcanvas.get_tk_widget().pack()
        self.laplacian_variances = []

        # Setup to close the whole program when the graph window is closed
        self.graph_window.protocol("WM_DELETE_WINDOW", self.quit)

        # Call update_graph every 1000 milliseconds
        self.after(100, self.update_graph)

    # Function to start move event
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    # Function to perform movement
    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")

    # Function to get the position of the window
    def get_pos(self):
        x = self.winfo_x() + self.canvas.winfo_x()
        y = self.winfo_y() + self.canvas.winfo_y()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        top_left = (int((x + self.border)), int((y + self.border)))
        bottom_right = (int((x + width - self.border)), int((y + height - self.border)))
        return top_left, bottom_right

    # Function to compute the variance of the Laplacian of the image
    def variance_of_laplacian(self, image):
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return cv2.Laplacian(open_cv_image, cv2.CV_64F).var()
    
    # Function to update the graph
    def update_graph(self):
        pos = self.get_pos()
        screenshot = pyautogui.screenshot(region=(pos[0][0], pos[0][1], pos[1][0] - pos[0][0], pos[1][1] - pos[0][1]))
        laplacian_variance = self.variance_of_laplacian(screenshot)

        # Add the latest laplacian variance to the data and keep the latest 10 points
        self.laplacian_variances.append(laplacian_variance)
        self.laplacian_variances = self.laplacian_variances[-30:]

        # Clear the previous plot
        self.a.clear()

        # Create the new plot
        self.a.plot(range(len(self.laplacian_variances)), self.laplacian_variances)
        self.a.set_ylim(0,max(self.laplacian_variances)*1.1)
        self.fig.suptitle(f"Laplacian Variance Indicator [{laplacian_variance:.1f}]")

        # Draw the plot on the canvas
        self.mcanvas.draw()

        # Call this function again after 1000 milliseconds
        self.after(100, self.update_graph)

    # Function to stop move event
    def stop_move(self, event):
        self.x = None
        self.y = None
        pos = self.get_pos()
        print(pos)

if __name__ == "__main__":
    app = TransparentWindow()
    app.wm_attributes('-transparentcolor','white')
    app.mainloop()
