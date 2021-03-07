from tkinter import *

root = Tk()
root.title("Calculator")

e = Entry(root, width=25, borderwidth=5)
e.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

#e.insert(0, "")

def button_click(number):
	global operator
	operator = e.get()
	e.delete(0, END)
	e.insert(0, str(operator) + str(number))

def clearButton():
	e.delete(0, END)

def equalButton():
	global operator
	operator = e.get()
	sumup=eval(operator)
	val=str(sumup)
	e.delete(0, END)
	e.insert(0, val)

# Button Setup
button1 = Button(root, text="1", padx=30, pady=10,command=lambda: button_click(1))
button2 = Button(root, text="2", padx=30, pady=10,command=lambda: button_click(2))
button3 = Button(root, text="3", padx=30, pady=10,command=lambda: button_click(3))
button4 = Button(root, text="4", padx=30, pady=10,command=lambda: button_click(4))
button5 = Button(root, text="5", padx=30, pady=10,command=lambda: button_click(5))	
button6 = Button(root, text="6", padx=30, pady=10,command=lambda: button_click(6))
button7 = Button(root, text="7", padx=30, pady=10,command=lambda: button_click(7))
button8 = Button(root, text="8", padx=30, pady=10,command=lambda: button_click(8))
button9 = Button(root, text="9", padx=30, pady=10,command=lambda: button_click(9))
button0 = Button(root, text="0", padx=30, pady=10,command=lambda: button_click(0))
buttonDot = Button(root, text=".", padx=30, pady=10,command=lambda: button_click("."))
buttonP = Button(root, text="+", padx=30, pady=10,command=lambda: button_click("+"))
buttonMi = Button(root, text="-", padx=30, pady=10,command=lambda: button_click("-"))
buttonMu = Button(root, text="*", padx=30, pady=10,command=lambda: button_click("*"))
buttonD = Button(root, text="/", padx=30, pady=10,command=lambda: button_click("/"))
clearButton = Button(root, text="C", padx=30, pady=10,command=clearButton)
enterButton = Button(root, text="=", padx=30, pady=10,command=equalButton)
# Row 3
button1.grid(row=3,column=0)
button2.grid(row=3,column=1)
button3.grid(row=3,column=2)
# Row 2
button4.grid(row=2,column=0)
button5.grid(row=2,column=1)
button6.grid(row=2,column=2)
# Row 1 
button7.grid(row=1,column=0)
button8.grid(row=1,column=1)
button9.grid(row=1,column=2)
# Row 4
button0.grid(row=4,column=0)
enterButton.grid(row=5,column=2)
buttonDot.grid(row=4,column=1)
clearButton.grid(row=5,column=1)
# Operations
buttonP.grid(row=1,column=3)
buttonMi.grid(row=2,column=3)
buttonMu.grid(row=3,column=3)
buttonD.grid(row=4,column=3)

root.mainloop()