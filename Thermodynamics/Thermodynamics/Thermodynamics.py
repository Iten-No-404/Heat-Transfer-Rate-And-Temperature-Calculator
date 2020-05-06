import PySimpleGUI as GUI   #For some decent UI (check the documentation/cook book because it will help : https://pysimplegui.readthedocs.io/en/latest/)
import numpy as np             
import matplotlib.pyplot as plt  #This and the previous library are for graphing



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
        if Click in (None, 'Quit'):   # if the user clicks Quit
            window.close()
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
            
                T0,TF,K0,B,L,X,A=int(V[0]),int(V[1]),int(V[2]),int(V[3]),int(V[4]),int(V[5]),int(V[6])
                C0=K0*(T0+0.5*B*(T0**2));
                C1=(K0*(TF+0.5*B*(TF**2))-C0)/L;
                TSolution= (-K0+(K0**2+2*K0*B*(C1*X+C0))**0.5)/(K0*B) #T Equations
                QSolution= A*(-C1) #Q Equation
                
                if(X>=0 and X<=L): #We can only find T and Q within the boundary
                    Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                         [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'x)'+'^-0.5'+')'+'/'+str(K0*B)+' where x ∈ ['+str(0)+' , '+str(L)+']')], 
                          [GUI.Text('Which corresponds to a temperature of '+str(round(TSolution,3))+' Kelvins and a heat flow rate of '+str(round(QSolution,3))+' Watts at x='+str(X))],#as well as the solution at the specified point
                        [GUI.Button('Graph')],
                          [GUI.Button('Try a different point')],
                         [GUI.Button('Quit')]]
                else :
                    Layout= [  [GUI.Text('Laplace Equation Solves To : ')],
                         [GUI.Text( 'T = ('+str(-K0)+'+ ('+str(round(K0**2+C0*B*K0*2,3))+'+'+str(round(B*K0*2*C1,3))+'x)'+'^-0.5'+')'+'/'+str(K0*B)+' where x ∈ ['+str(0)+' , '+str(L)+']')], 
                          [GUI.Text('Which corresponds to an unknown temperature and an unknown heat flow rate at x='+str(X))],#as well as the solution at the specified point
                        [GUI.Button('Graph')],
                          [GUI.Button('Try a different point')],
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
                        graph(my_formula, range(0, int(V[4])))
                       
                    if newClick_1 in ( None, 'Try a different point'): #the user chooses to try a different point, so we exit our new windows
                        break
                    if newClick_1 in (None, 'Quit' ): #here we exit both windows
                        window.close()
                        break
                newwindow_1.close()
                #GG

