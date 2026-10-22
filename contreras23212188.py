"""
Práctica: Sistema cardiovascular
Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Contreras Jimenez Kenia Yasdit
Número de control: 23212188
Correo institucional: l23212188@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerias
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Datos generales de la simulacion
u = np.array(pd.read_excel('signal.xlsx',header=None))
x0,t0,tend,dt,w,h = 0,0,15,1e-3,10,5
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u = np.reshape(signal.resample(u,len(t)),-1)

def cardio(Z,L,R,C):
    num = [L*R,R*Z]
    den = [C*L*R*Z,L*R+L*Z,R*Z]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

# Función de transferencia: Hipotenso
Z,L,R,C = 0.010,0.001,1.00,3.500
syshipo,L = cardio(Z,L,R,C)
print(f'Función de transferencia del hipotenso (caso 1): {syshipo}')
print(f"Polos del sistema: L1= {L[0]:.3E}, L2= {L[1]:.3E}\n")

# Función de transferencia: Normotenso
Z,L,R,C = 0.010,0.001,1.00,1.500
sysnormo,L = cardio(Z,L,R,C)
print(f'Función de transferencia del normotenso (control): {sysnormo}')
print(f"Polos del sistema: L1= {L[0]:.3E}, L2= {L[1]:.3E}\n")

# Función de transferencia: Hipertenso
Z,L,R,C = 0.010,0.001,1.00,1.000
syshiper,L = cardio(Z,L,R,C)
print(f'Función de transferencia del hipertenso (caso 2): {syshiper}')
print(f"Polos del sistema: L1= {L[0]:.3E}, L2= {L[1]:.3E}\n")

# Controlador PID 
def controlador(kP,kI,kD,sys):
    Cr=1E-6
    Re=1/(Cr*kI)
    Rr=kP*Re
    Ce=kD/Rr
    numPID=[Re*Rr*Ce*Cr,(Re*Ce+Rr*Cr),1]
    denPID=[Re*Cr,0]
    PID=ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign = -1)
    return sysPID

hipoPID = controlador(458.184,1110647.276,0.00627,syshipo)
print(f'Función de transferencia del hipotenso en lazo cerrado: {hipoPID}')
hiperPID = controlador(129.978,312762.858,0.00174,syshiper)
print(f'Función de transferencia del hipertenso en lazo cerrado: {hiperPID}')

# Funciones de sistema en lazo abierto  
_,Pp0 = ctrl.forced_response(sysnormo,t,u,x0)
_,Pp1 = ctrl.forced_response(syshipo,t,u,x0)
_,Pp2 = ctrl.forced_response(syshiper,t,u,x0)

# Funciones de sistema en lazo cerrado
_,PIDHipo = ctrl.forced_response(hipoPID,t,Pp0,x0)
_,PIDHiper = ctrl.forced_response(hiperPID,t,Pp0,x0)

def plotsignals(caso):
    # Colores
    clr1 = np.array([139, 30, 45]) / 255
    clr2 = np.array([51, 104, 160]) / 255
    clr3 = np.array([18, 84, 79]) / 255
    clr4 = np.array([0.5, 0.5, 0.5])

    fg = plt.figure()
    fg.patch.set_facecolor('w')
    fg.set_size_inches(w,h) 

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 11
    plt.rcParams['mathtext.fontset'] = 'stix' 

    if caso == "individuos":
        plt.plot(t,Pp0,'-',linewidth=0.5,color=clr1) # Normotenso
        plt.plot(t,Pp1,'-',linewidth=0.5,color=clr2) # Hipotenso
        plt.plot(t,Pp2,'-',linewidth=0.5,color=clr3) # Hipertenso
        L = plt.legend(['$P_p(t):Normotenso$','$P_p(t):Hipotenso$','$P_p(t):Hipertenso$'],loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=3, frameon=False, fontsize=13)
    elif caso == "hipotenso":
        plt.plot(t,Pp0,'-',linewidth=0.5,color=clr1) # Normotenso
        plt.plot(t,Pp1,'-',linewidth=0.5,color=clr2) # Hipotenso
        plt.plot(t,PIDHipo,':',linewidth=1,color=clr4) # Controlador hipotenso
        L = plt.legend(['$P_p(t):Normotenso$','$P_p(t):Hipotenso$','$PID(t):Hipotenso$'],loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=3, frameon=False, fontsize=13)
    elif caso == "hipertenso":
        plt.plot(t,Pp0,'-',linewidth=0.5,color=clr1) # Normotenso
        plt.plot(t,Pp2,'-',linewidth=0.5,color=clr3) # Hipertenso
        plt.plot(t,PIDHiper,':',linewidth=1,color=clr4) # Controlador hipertenso
        L = plt.legend(['$P_p(t):Normotenso$','$P_p(t):Hipertenso$','$PID(t):Hipertenso$'], loc='upper center', bbox_to_anchor=(0.5, 1.18),ncol=3, frameon=False, fontsize=13)

    plt.xlabel('$t$ [s]', fontsize=11, fontname='Times New Roman')
    plt.ylabel('$V_i(t)$ [V]', fontsize=11, fontname='Times New Roman')
    plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
    plt.ylim(-0.6,1.28); plt.yticks(np.arange(-0.6,1.3,0.2))
    plt.tight_layout()
    plt.subplots_adjust(top=0.80) 
    plt.show()
    fg.savefig(caso+'_python.pdf', bbox_inches='tight', format='pdf')
    return fg

# Graficas
plotsignals("individuos")
plotsignals("hipotenso")
plotsignals("hipertenso")