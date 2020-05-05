import PySimpleGUI as GUI   #For some decent UI (check the documentation/cook book because it will help : https://pysimplegui.readthedocs.io/en/latest/)
import numpy as np             
import matplotlib.pyplot as plt  #This and the previous library are for graphing

while True: #The windows has to be running until the user exits (breaks)

    #Input Window
    GUI.theme('Material1')   # there
    # Creating Window Text, Text Boxes and Buttons
    Layout = [
      [GUI.Text('                              Medium Info  ')],
      [GUI.Text('Temperature at the left border (Tₒ) :')], [GUI.InputText()],
      [GUI.Text('Temperature at the right border ( Tₛ) :')], [GUI.InputText()],
      [GUI.Text('Constant Kₒ :')], [GUI.InputText()],
      [GUI.Text('Constant β  :')],[ GUI.InputText()],
      [GUI.Text('The length of the Wall (L) :')],[ GUI.InputText()],
      [GUI.Text('Calculation Point (X) :')],[ GUI.InputText()],
      [GUI.Text('The Cross-sectional Area (A) : ')],[ GUI.InputText()],
      [GUI.Button('Scan'), GUI.Button('Quit')]
     ]
        

    # Creating the initialized window
    window = GUI.Window('Heat Radar', Layout)

    # Interacting to the users clicks
    while True:
        Click, Variable = window.read() #This returns actions in 'Click' and entereds variables in Variable[i]
        if Click in (None, 'Quit'):   # if the user clicks Quit
            window.close()
        elif Click in ( 'Scan'):        #if the user clicks Scan
            if not (Variable[0] and Variable[1] and Variable[2] and Variable[3] and Variable[4] and Variable[5] and Variable[6]): 
                #Variable[0] 0 corresponds to Tₒ Variable [1] corresponds to  Tₛ and so on, here we're just checking if any of them is not given (null)
                GUI.theme('Material1') #in case any of them isn't given we create a new window
                Layout= [  [GUI.Text('Some variables are missing, please fill the list')],
                [GUI.Button('Back')] ]
                newwindow=GUI.Window('Missing Info', Layout)
                while True:
                    newClick, newVariable = newwindow.read() 
                    if newClick in ( None, 'Back'): #in the new window if the user clicks back it exits the new window (goes to newwindow.close())
                        break
                newwindow.close()
            else: #otherwise if all variables are given, a different window with the solution has to appear
                GUI.theme('Material1')
                TSolution= -1 #we need to write the equation of T here so this gives the value of T when called
                QSolution= 3+2j #we need to write the equation of heat flow rate here so this gives the value of Q when called
                Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                         [GUI.Text("T="+str(int(Variable[4])*int(Variable[3]))+'X'+'+'+Variable[5])], #Would look cool if we show the user the equation
                          [GUI.Text('Which corresponds to a temperature of '+str(TSolution)+' Kelvins and a heat flow rate of '+str(QSolution)+' at the given point')],#as well as the solution at the specified point
                [GUI.Button('Try a different point')],
                         [GUI.Button('Quit')]]
                newwindow_1=GUI.Window('Solution', Layout) #creating the initialized window
                #here I was trying to make it graph T vs X, the GUI library doesn't integrate well with the graphing library so it graphs but causes bugs, this will be revistsed
                #def graph (formula,range):
                    #x=np.array(range)
                    #T=formula(x)
                    #plt.plot(x,T)
                  #  plt.show()
                #def my_formula(x):
                  #  return x**3+2*x-4
                #graph(my_formula, range(0, int(Variable[4])))
                # you can take the code in another python window and see how graphing works
                while True:
                    newClick_1, newVariable_1 = newwindow_1.read()
                    if newClick_1 in ( None, 'Try a different point'): #the user chooses to try a different point, so we exit our new windows
                        break
                    if newClick_1 in (None, 'Quit' ): #here we exit both windows
                        window.close()
                        break
                newwindow_1.close()
                #GG

