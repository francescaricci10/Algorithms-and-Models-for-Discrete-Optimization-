import tkinter
from tkinter import Tk, Label, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from import_file_set_covering_problem import setting_data_problem
from gomory_iteration_manager import GomoryIterationManager
from solver_binario import solve_problem_binario

from solver_gomory_cuts_interi import solve_problem_intero
from solver_gomory_cuts_frazionari import solve_problem_frazionario
from solver_gomory_multiple_cuts_interi import solve_problem_multiple_interi
from solver_gomory_multiple_cuts_frazionari import solve_problem_multiple_frazionario



window = Tk()
window.geometry('2000x1000')
window.title("Gomory cuts algorithm")

lbl = Label(window, text="       ")
lbl.grid(column=3, row=1)

lbl = Label(window, text="Import your test file:")
lbl.grid(column=3, row=2)

label = tkinter.Label(window, text=" ")
label.grid(row=5, column=3)

label = tkinter.Label(window, text="Gap value: ")
label.grid(row=5, column=3)

text = tkinter.Text(window, height=1, width=10)
text.grid(row=6, column=3)



figure = Figure(figsize=(7, 5), dpi=100)
plot = figure.add_subplot(1, 1, 1)

figure2 = Figure(figsize=(7.5, 5), dpi=100)
plot2 = figure2.add_subplot(1, 1, 1)

integer_optimal_solution = 0.0
def_gap = 0.001


def clicked():

    plot.cla()
    plot2.cla()

    file = filedialog.askopenfilenames()
    input = text.get("1.0", tkinter.END)

    # se l'utente non specifica il gap, ne viene settato uno di default
    if text.compare("end-1c", "==", "1.0") or isinstance(input, str) or input <= 0:
        gap_value = def_gap
    else:
        gap_value = float(input)

    selection = v.get()
    instanceProblem = setting_data_problem(file)

    # calcolo della soluzione ottima intera
    integer_optimal_solution = solve_problem_binario(instanceProblem)
    integer_optimal_solution = float(integer_optimal_solution)

    canvas = FigureCanvasTkAgg(figure, window)
    canvas.get_tk_widget().grid(row=10, column=3)

    canvas2 = FigureCanvasTkAgg(figure2, window)
    canvas2.get_tk_widget().grid(row=10, column=4)


    if selection == 1:
        # Gomory cuts interi
        percent_limit = gap_value
        iteration_manager = GomoryIterationManager(float(0), False, percent_limit)
        solve_problem_intero(instanceProblem, iteration_manager)
    elif selection == 2:
        # Gomory cuts frazionari
        percent_limit = gap_value
        iteration_manager = GomoryIterationManager(float(0), False, percent_limit)
        solve_problem_frazionario(instanceProblem, iteration_manager)
    elif selection == 3:
        # Gomory cuts interi multipli
        percent_limit = gap_value
        iteration_manager = GomoryIterationManager(float(0), False, percent_limit)
        solve_problem_multiple_interi(instanceProblem, iteration_manager)
    elif selection == 4:
        # Gomory cuts frazionari multipli
        percent_limit = gap_value
        iteration_manager = GomoryIterationManager(float(0), False, percent_limit)
        solve_problem_multiple_frazionario(instanceProblem, iteration_manager)



    x1 = [0, instanceProblem.num_try]
    y1 = [integer_optimal_solution, integer_optimal_solution]
    plot.plot(x1, y1)

    x2 = [0] * instanceProblem.num_try
    y2 = [0] * instanceProblem.num_try
    for i in range(instanceProblem.num_try):
        x2[i] = i
        y2[i] = instanceProblem.optimal_solution[i]

    plot.plot(x2, y2, color="lightblue", marker=".", linestyle="")
    plot2.plot(x2, y2, color="lightblue", marker=".", linestyle="")


    final_lbl0 = Label(window, text="     ")
    final_lbl0.grid(column=3, row=10)
    final_lbl = Label(window, text=" Numero di iterazioni : " + str(round(instanceProblem.num_try,6)))
    final_lbl.grid(column=3, row=13)
    final_lbl01 = Label(window, text="     ")
    final_lbl01.grid(column=3, row=14)
    final_lbl2 = Label(window, text=" Valore iniziale : " + str(round(instanceProblem.optimal_solution[0],6)))
    final_lbl2.grid(column=3, row=15)
    final_lbl3 = Label(window, text=" Valore finale : " + str(round(instanceProblem.optimal_solution[instanceProblem.num_try],6)))
    final_lbl3.grid(column=3, row=16)
    incremento = instanceProblem.optimal_solution[instanceProblem.num_try] - instanceProblem.optimal_solution[0]
    final_lbl4 = Label(window, text=" Incremento :  " + str(round(incremento,6)) + "      ( " + str(round(100*incremento/instanceProblem.optimal_solution[0],6)) + " % )" )
    final_lbl4.grid(column=4, row=15)
    final_lbl5 = Label(window, text=" Distanza dall'ottimo intero :  " + str(round(integer_optimal_solution-instanceProblem.optimal_solution[instanceProblem.num_try],6)) )
    final_lbl5.grid(column=4, row=16)




btn = tkinter.Button(window, text="Choose", command=clicked)
btn.grid(column=3, row=3)


canvas = FigureCanvasTkAgg(figure, window)
canvas.get_tk_widget().grid(row=10, column=3)

canvas2 = FigureCanvasTkAgg(figure2, window)
canvas2.get_tk_widget().grid(row=10, column=4)

v = tkinter.IntVar()
v.set(1)

btn1 = tkinter.Radiobutton(window, text="Gomory cuts interi                                  ", padx = 20, variable=v, value=1)
btn2 = tkinter.Radiobutton(window, text="Gomory cuts frazionari                           ", padx = 20, variable=v, value=2)
btn3 = tkinter.Radiobutton(window, text="Gomory cuts interi (multiple cuts)         ", padx = 20, variable=v, value=3)
btn4 = tkinter.Radiobutton(window, text="Gomory cuts frazionari (multiple cuts) ", padx = 20, variable=v, value=4)

btn1.grid(column=4, row=2)
btn2.grid(column=4, row=3)
btn3.grid(column=4, row=4)
btn4.grid(column=4, row=5)


window.mainloop()








