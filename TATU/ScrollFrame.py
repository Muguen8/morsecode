import tkinter as tk, tkinter.ttk as ttk

 
class ScrollableFrame(tk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs,)
		
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		
		self.canvas = tk.Canvas(self, highlightthickness=0, 
		bg = kwargs.get("bg", "#FFFFFF"))
		scrollbar   = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
		self.scrollable_frame = tk.Frame(self.canvas, bg = kwargs.get("bg", "#FFFFFF"), padx = 10)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(
				scrollregion=self.canvas.bbox("all")
			)
		)

		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=scrollbar.set)
		self.canvas.configure(xscrollcommand=scrollbar_x.set)
		self.canvas.grid(row = 0, column = 0, sticky = "nsew", rowspan = 2)#pack(side="left", fill="both", expand=True)


		scrollbar.grid(row = 0, column = 1, sticky = "nse",  rowspan = 2) #.pack(side="right", fill="y")
		scrollbar_x.grid(row = 1, column = 0, sticky = "sew") #.pack(side="bottom", fill="x")


		#scroll wheel       
		self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)

	#add scrollwheel feature
	def on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-event.delta / abs(event.delta)), 'units')

	def pintar(self,clr):
		self.config(bg=clr)
		self.canvas.config(background=clr)
		self.scrollable_frame.config(bg=clr)

