import PySimpleGUI as GUI   #For some decent UI (check the documentation/cook book because it will help : https://pysimplegui.readthedocs.io/en/latest/)
import matplotlib.pyplot as plt  #This and the previous library are for graphing
import numpy as np
from numpy import log
import warnings
warnings.filterwarnings("ignore")
print("Close this one done with the program")
#=======================================================================================================================================================#

#The layout of the GUI, Note that the first pair of square brackets is for the layout list and each succeeding pair represents a row.
#We have 2 rows, the first for the "Choose Coordinate System" text, the second is for the 3 buttons
GUI.theme('Material1')
layout = [[GUI.T('Choose Coordinate System')],[GUI.B('Cartesian'),GUI.B('Cylinderical'), GUI.B('Spherical')]]

#Creates a window with the specified name and layout and stores it in the variable "window"
#"element_justification = 'center'" makes the text and buttons align with the centerline, otherwise they're aligned to the left
#"size" controls the window size by pixel (I think) excluding the titlebar.
main_window = GUI.Window('Heat Radar',layout, element_justification = 'center', size = (300,80))


#Contiuously does the following actions: reads any actions, in this case, button presses, and checks which button was pressed.
while True:
    event,values = main_window.read()
    if event is "Cartesian": #Cartesian Code
        while True: #The windows has to be running until the user exits (breaks)
            #Input Window
            GUI.theme('Material1')   # there
            # Creating Window Text, Text Boxes and Buttons
            Layout = [
              [GUI.Text('                       Medium Info in SI Units  ')],
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
                Click, V = window.read() #This returns actions in 'Click' and entereds Variables in V[i]
                if Click in (None, 'Quit'):
                # if the user clicks Quit
                    window.close()
                    main_window.close()
                    
              
                elif Click in ( 'Scan'):        #if the user clicks Scan
                    if not (V[0] and V[1] and V[2] and V[3] and V[4] and V[5] and V[6]): 
                        #V[0] 0 corresponds to Tₒ V [1] corresponds to  Tₛ and so on, here we're just checking if any of them is not given (null)
                        GUI.theme('Material1') #in case any of them isn't given we create a new window
                        Layout= [  [GUI.Text('Some Variables are missing, please fill the list')],
                        [GUI.Button('Back')] ]
                        newwindow=GUI.Window('Missing Info', Layout)
                        while True:
                            newClick, newV = newwindow.read() 
                            if newClick in ( None, 'Back'): #in the new window if the user clicks back it exits the new window (goes to newwindow.close())
                                break
                        newwindow.close()
                    else: #otherwise if all Variables are given, a different window with the solution has to appear
                        GUI.theme('Material1')
            
                        T0,TF,K0,B,L,X,A=float(eval(V[0])),float(eval(V[1])),float(eval(V[2])),float(eval(V[3])),float(eval(V[4])),float(eval(V[5])),float(eval(V[6]))
                        C0=K0*(T0+0.5*B*(T0**2));
                        C1=(K0*(TF+0.5*B*(TF**2))-C0)/L;
                        TSolution= (-K0+(K0**2+2*K0*B*(C1*X+C0))**0.5)/(K0*B) #T Equations
                        QSolution= A*(-C1) #Q Equation
                
                        if(X>=0 and X<=L): #We can only find T and Q within the boundary
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'x)'+'^-0.5'+')'+'/'+str(K0*B)+' where x ∈ ['+str(0)+' , '+str(L)+']')], 
                                  [GUI.Text('Which corresponds to a temperature of '+str(round(TSolution,3))+' Kelvins and a heat flow rate of '+str(round(QSolution,3))+' Watts at x='+str(X))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]
                        else :
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'x)'+'^-0.5'+')'+'/'+str(K0*B)+' where x ∈ ['+str(0)+' , '+str(L)+']')], 
                                  [GUI.Text('Which corresponds to an unknown temperature and an unknown heat flow rate at x='+str(X))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]



                        newwindow_1=GUI.Window('Solution', Layout) #creating the initialized window
                
                        # you can take the code in another python window and see how graphing works
                        while True:
                            newClick_1, newV_1 = newwindow_1.read()
                            if newClick_1 in ( 'Graph'): 
                                def graph (formula,range):
                                    x=np.array(range)
                                    T=formula(x)
                                    plt.plot(x,T)
                                    plt.show(block=False)
                                def my_formula(x):
                                    return (-K0+(K0**2+2*K0*B*(C1*x+C0))**0.5)/(K0*B)
                                graph(my_formula, np.linspace(0,float(eval(V[4])),10000))
                       
                            if newClick_1 in ( None, 'Try different inputs'): #the user chooses to try a different point, so we exit our new windows
                                break
                            if newClick_1 in (None, 'Quit' ): #here we exit both windows
                                window.close()
                                break
                        newwindow_1.close()
                        #GG



    elif event == "Cylinderical": #Cylinderical Code
         while True: #The windows has to be running until the user exits (breaks)
            #Input Window
            GUI.theme('Material1')  # there
            # Creating Window Text, Text Boxes and Buttons
            Layout = [
              [GUI.Text('                       Medium Info in SI Units  ')],
              [GUI.Text('Temperature at the left border (Tₒ) :')], [GUI.InputText()],
              [GUI.Text('Temperature at the right border ( Tₛ) :')], [GUI.InputText()],
              [GUI.Text('Constant Kₒ :')], [GUI.InputText()],
              [GUI.Text('Constant β  :')],[ GUI.InputText()],
              [GUI.Text('Inner Radius (Rₒ) :')],[ GUI.InputText()],
              [GUI.Text('Outer Radius (Rₛ) :')],[ GUI.InputText()],
              [GUI.Text('Calculation Point (r) :')],[ GUI.InputText()],
              [GUI.Text('The Cross-sectional Area (A) : ')],[ GUI.InputText()],
              [GUI.Button('Scan'), GUI.Button('Quit')]
             ]
        

            # Creating the initialized window
            window = GUI.Window('Heat Radar', Layout)

            # Interacting to the users clicks
            while True:
                Click, V = window.read() #This returns actions in 'Click' and entereds Variables in V[i]
                if Click in (None, 'Quit'):   # if the user clicks Quit
                    window.close()
                    main_window.close()
                   #Added by Tarek
              
                elif Click in ( 'Scan'):        #if the user clicks Scan
                    if not (V[0] and V[1] and V[2] and V[3] and V[4] and V[5] and V[6] and V[7]): 
                        #V[0] 0 corresponds to Tₒ V [1] corresponds to  Tₛ and so on, here we're just checking if any of them is not given (null)
                        GUI.theme('Material1') #in case any of them isn't given we create a new window
                        Layout= [  [GUI.Text('Some Variables are missing, please fill the list')],
                        [GUI.Button('Back')] ]
                        newwindow=GUI.Window('Missing Info', Layout)
                        while True:
                            newClick, newV = newwindow.read() 
                            if newClick in ( None, 'Back'): #in the new window if the user clicks back it exits the new window (goes to newwindow.close())
                                break
                        newwindow.close()
                    else: #otherwise if all Variables are given, a different window with the solution has to appear
                        GUI.theme('Material1')
            
                        T0,TF,K0,B,R0,RF,r,A=float(eval(V[0])),float(eval(V[1])),float(eval(V[2])),float(eval(V[3])),float(eval(V[4])),float(eval(V[5])),float(eval(V[6])),float(eval(V[7]))
                        C1=K0*((TF+0.5*B*(TF**2))-(T0+0.5*B*(T0**2)))/log(RF/R0);
                        C0=K0*(TF+0.5*B*(TF**2))-C1*log(RF);
                        TSolution= (-K0+(K0**2+2*K0*B*(C1*log(r)+C0))**0.5)/(K0*B) #T Equations
                        QSolution= A*(-C1)/r #Q Equation
                        if(RF<R0):
                            GUI.popup("Inner Radius Cannot be larger than Outer Radius, the program will terminate now.")
                            #break
                            exit()
                        elif(r>=R0 and r<=RF): #We can only find T and Q within the boundary
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'ln(r))'+'^-0.5'+')'+'/'+str(K0*B)+' where r ∈ ['+str(R0)+' , '+str(RF)+']')], 
                                  [GUI.Text('Which corresponds to a temperature of '+str(round(TSolution,3))+' Kelvins and a heat flow rate of '+str(round(QSolution,3))+' Watts at r='+str(r))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]
                        else :
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'ln(r))'+'^-0.5'+')'+'/'+str(K0*B)+' where r ∈ ['+str(R0)+' , '+str(RF)+']')], 
                                  [GUI.Text('Which corresponds to an unknown temperature and an unknown heat flow rate at r='+str(r))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]



                        newwindow_1=GUI.Window('Solution', Layout) #creating the initialized window
                
                        # you can take the code in another python window and see how graphing works
                        while True:
                            newClick_1, newV_1 = newwindow_1.read()
                            if newClick_1 in ( 'Graph'): 
                                def graph (formula,range):
                                    r=np.array(range)
                                    T=formula(r)
                                    plt.plot(r,T)
                                    plt.show(block=False)
                                def my_formula(r):
                                    return (-K0+(K0**2+2*K0*B*(C1*log(r)+C0))**0.5)/(K0*B)
                                graph(my_formula, np.linspace(float(eval(V[4])),float(eval(V[5])),10000))
                       
                            if newClick_1 in ( None, 'Try different inputs'): #the user chooses to try a different point, so we exit our new windows
                                break
                            if newClick_1 in (None, 'Quit' ): #here we exit both windows
                                window.close()
                                break
                        newwindow_1.close()




    elif event == "Spherical":  #Spherical Code
        while True: #The windows has to be running until the user exits (breaks)
            #Input Window
            GUI.theme('Material1')  # there
            # Creating Window Text, Text Boxes and Buttons
            Layout = [
              [GUI.Text('                       Medium Info in SI Units  ')],
              [GUI.Text('Temperature at the left border (Tₒ) :')], [GUI.InputText()],
              [GUI.Text('Temperature at the right border ( Tₛ) :')], [GUI.InputText()],
              [GUI.Text('Constant Kₒ :')], [GUI.InputText()],
              [GUI.Text('Constant β  :')],[ GUI.InputText()],
              [GUI.Text('Inner Radius (Rₒ) :')],[ GUI.InputText()],
              [GUI.Text('Outer Radius (Rₛ) :')],[ GUI.InputText()],
              [GUI.Text('Calculation Point (r) :')],[ GUI.InputText()],
              [GUI.Text('The Cross-sectional Area (A) : ')],[ GUI.InputText()],
              [GUI.Button('Scan'), GUI.Button('Quit')]
             ]
        

            # Creating the initialized window
            window = GUI.Window('Heat Radar', Layout)

            # Interacting to the users clicks
            while True:
                Click, V = window.read() #This returns actions in 'Click' and entereds Variables in V[i]
                if Click in (None, 'Quit'):   # if the user clicks Quit
                    window.close()
                    main_window.close() #Added by Tarek
              
                elif Click in ( 'Scan'):        #if the user clicks Scan
                    if not (V[0] and V[1] and V[2] and V[3] and V[4] and V[5] and V[6] and V[7]): 
                        #V[0] 0 corresponds to Tₒ V [1] corresponds to  Tₛ and so on, here we're just checking if any of them is not given (null)
                        GUI.theme('Material1') #in case any of them isn't given we create a new window
                        Layout= [  [GUI.Text('Some Variables are missing, please fill the list')],
                        [GUI.Button('Back')] ]
                        newwindow=GUI.Window('Missing Info', Layout)
                        while True:
                            newClick, newV = newwindow.read() 
                            if newClick in ( None, 'Back'): #in the new window if the user clicks back it exits the new window (goes to newwindow.close())
                                break
                        newwindow.close()
                    else: #otherwise if all Variables are given, a different window with the solution has to appear
                        GUI.theme('Material1')
            
                        T0,TF,K0,B,R0,RF,r,A=float(eval(V[0])),float(eval(V[1])),float(eval(V[2])),float(eval(V[3])),float(eval(V[4])),float(eval(V[5])),float(eval(V[6])),float(eval(V[7]))
                        C1=K0*((TF+0.5*B*(TF**2))-(T0+0.5*B*(T0**2)))*(RF*R0/(RF-R0));
                        C0=K0*(TF+0.5*B*(TF**2))+C1/RF;
                        TSolution= (-K0+(K0**2+2*K0*B*(-C1/r+C0))**0.5)/(K0*B) #T Equations
                        QSolution= A*(-C1)/r**2 #Q Equation
                        if(RF<R0):
                                GUI.popup("Inner Radius Cannot be larger than Outer Radius, the program will terminate now.")
                            #break
                                exit()
                        elif(r>=R0 and r<=RF): #We can only find T and Q within the boundary
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'-1/r)'+'^-0.5'+')'+'/'+str(K0*B)+' where r ∈ ['+str(R0)+' , '+str(RF)+']')], 
                                  [GUI.Text('Which corresponds to a temperature of '+str(round(TSolution,3))+' Kelvins and a heat flow rate of '+str(round(QSolution,3))+' Watts at r='+str(r))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]
                        else :
                            Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                                 [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'-1/r)'+'^-0.5'+')'+'/'+str(K0*B)+' where r ∈ ['+str(R0)+' , '+str(RF)+']')], 
                                  [GUI.Text('Which corresponds to an unknown temperature and an unknown heat flow rate at r='+str(r))],#as well as the solution at the specified point
                                [GUI.Button('Graph')],
                                  [GUI.Button('Try different inputs')],
                                 [GUI.Button('Quit')]]



                        newwindow_1=GUI.Window('Solution', Layout) #creating the initialized window
                
                        # you can take the code in another python window and see how graphing works
                        while True:
                            newClick_1, newV_1 = newwindow_1.read()
                            if newClick_1 in ( 'Graph'): 
                                def graph (formula,range):
                                    r=np.array(range)
                                    T=formula(r)
                                    plt.plot(r,T)
                                    plt.show(block=False)
                                def my_formula(r):
                                    return (-K0+(K0**2+2*K0*B*(-C1/r+C0))**0.5)/(K0*B)
                                graph(my_formula, np.linspace(float(eval(V[4])),float(eval(V[5])),10000))
                       
                            if newClick_1 in ( None, 'Try different inputs'): #the user chooses to try a different point, so we exit our new windows
                                break
                            if newClick_1 in (None, 'Quit' ): #here we exit both windows
                                window.close()
                                break
                        newwindow_1.close()
         