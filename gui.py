import matplotlib
import pandas as pd
from pathlib import Path
from AGDS import AGDS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import path

import time

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)
similarities_text = "Similarities to instance id "


class AGDS_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "AGDS visualizer")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        self.agds = None
        self.res = None
        self.length = 150

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_dataset_len(self):
        if hasattr(self, 'agds') and self.agds is not None:
            return self.agds.dataset_len
        else:
            return None

    def draw_plot_scale(self, x, scale_label):
        start_time = time.time()
        self.draw_plot(x, scale_label)
        print("--- self.draw_plot execution: %s seconds ---" % (time.time() - start_time))

    def calculate_for_instance(self, instance, scale_label, scale, instance_label=None):
        if self.agds is not None:
            self.res, _ = self.agds.calculate_for_index(int(instance))
            self.draw_plot(0, scale_label)
            scale.set(0)
            if instance_label is not None:
                instance_label.config(text=similarities_text + str(instance))

    def load_file(self, scale_label, spin):
        file = filedialog.askopenfilename(filetypes=(("CSV files","*.csv"),("XLS files","*.xls")), initialdir=path.dirname(__file__))
        print('LOADED: ', file)
        ar = file.split('.')
        df = None
        if ar[len(ar) - 1] == 'xls':
            df = pd.read_excel(Path(file), header=None, index_col=None)
        elif ar[len(ar) - 1] == 'csv':
            df = pd.read_csv(Path(file), header=0, index_col=None)
        if df is not None:
            self.agds = AGDS(df)
            self.res, _ = self.agds.calculate_for_index(0)
            self.draw_plot(0, scale_label)
            spin.config(to=self.agds.dataset_len)

    def draw_plot(self, x, scale_label):
        if hasattr(self, 'agds') and self.agds is not None:
            scale_label.config(text=str(round(float(x), 3)))
            attrs, instances, edges = self.agds.get_graph(float(x), self.res)

            instances_x = list(map(lambda x: x['pos'][0], instances))
            instances_y = list(map(lambda y: y['pos'][1], instances))

            f = Figure(figsize=(10, 5), dpi=100)
            a = f.add_subplot(111)
            a.scatter(instances_x, instances_y)

            for edge in edges:
                a.plot(edge['start'], edge['end'], color='gray')
            # print(edges)
            for attr in attrs:
                attrs_x = list(map(lambda x: x['pos'][0], attrs[attr]))
                attrs_y = list(map(lambda y: y['pos'][1], attrs[attr]))
                a.scatter(attrs_x, attrs_y)

            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.winfo_children()[1].destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="AGDS visualizer", font=LARGE_FONT)
        scale_label = tk.Label(self, text="0", font=LARGE_FONT)
        spin = ttk.Spinbox(self, from_=0)
        spin.set(0)
        button = ttk.Button(self, text="Load file",
                            command=lambda: controller.load_file(scale_label, spin))

        var = tk.DoubleVar()
        scale = ttk.Scale(self, from_=0, to=1, variable=var, length=400, command=lambda x: controller.draw_plot_scale(x, scale_label))
        scale.set(0)
        button2 = ttk.Button(self, text="Calculate",
                             command=lambda: controller.calculate_for_instance(spin.get(), scale_label, scale))

        label.pack(pady=10, padx=10)
        button.pack(pady=10, padx=10, side=tk.LEFT)
        button2.pack(pady=10, padx=10, side=tk.LEFT)
        spin.pack(pady=10, padx=10, side=tk.LEFT)
        scale.pack(pady=20, padx=10)
        scale_label.pack(pady=35, padx=10)

        f = Figure(figsize=(10, 5), dpi=100)

        canvas = FigureCanvasTkAgg(f, controller)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


app = AGDS_GUI()
app.mainloop()
