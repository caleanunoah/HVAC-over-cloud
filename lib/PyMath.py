import tkinter as tk
from tkinter import ttk
import matplotlib, sys
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas
import matplotlib.pyplot as plt

def configure_plot(datapoint):
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()


if __name__ == '__main__':
    # root
    window = tk.Tk()
    window.geometry('350x200')

    # Create widgets for UI
    # label text for title
    ttk.Label(window, text="Operator Dashboard",
              background='black', foreground="white",
              font=("Arial", 15)).grid(row=0, column=1)

    # label
    ttk.Label(window, text="Select the Site :",
              font=("Arial", 10)).grid(column=0, row=5, padx=10, pady=25)

    # Combobox creation
    n = tk.StringVar()
    input_choosen = ttk.Combobox(window, width=27, textvariable=n)

    # Adding combobox drop down list
    input_choosen['values'] = (' NEU',
                              " HQ (Noah's Office)",
                              ' Auto (TBD)')

    input_choosen.grid(column=1, row=5)
    input_choosen.current(1)


    window.mainloop()
