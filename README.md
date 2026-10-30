[![Open in MATLAB Online](https://www.mathworks.com/images/responsive/global/open-in-matlab-online.svg)](https://matlab.mathworks.com/open/github/v1?repo=YasditContreras/MSFP2)
# Práctica 2 — Modelado y control del sistema cardiovascular mediante el modelo Windkessel

Repositorio académico de la asignatura **Modelado de Sistemas Fisiológicos**, correspondiente al programa de **Ingeniería Biomédica** del Tecnológico Nacional de México / Instituto Tecnológico de Tijuana.

Esta práctica estudia el **modelo Windkessel de cuatro elementos** para representar la dinámica del sistema cardiovascular. Se comparan tres condiciones simuladas —**hipotensa, normotensa e hipertensa**— y se diseñan estrategias de control *in silico* para reducir la diferencia entre los casos hipotenso/hipertenso y la respuesta de referencia normotensa.

> **Importante:** las estrategias de control desarrolladas en esta práctica tienen fines exclusivamente académicos y de simulación.

## Datos de la práctica

**Docente:** Dr. Paul Antonio Valle Trujillo  
**Institución:** Tecnológico Nacional de México / Instituto Tecnológico de Tijuana  
**Estudiante:** Kenia Yasdit Contreras Jiménez · 23212188 · l23212188@tectijuana.edu.mx

## Contenido
1. Resumen
2. Competencia y objetivos
3. Introducción al modelo Windkessel
4. Variables y analogía eléctrica
5. Parámetros de los tres casos
6. Modelo mediante ecuaciones diferenciales
7. Funciones de transferencia
8. Error y estabilidad

---

## 1. Resumen
El objetivo es **modelar, analizar y controlar el comportamiento dinámico del sistema cardiovascular** utilizando el modelo Windkessel de cuatro elementos: **Z, C, R, L**.

## 4. Variables y analogía eléctrica

Las variables de estado seleccionadas son:

$$ x_1(t) = F_L(t) $$

$$ x_2(t) = P_p(t) $$

$$ u(t) = P_a(t) $$

$$ y(t) = P_p(t) $$

### Relaciones constitutivas

$$ P_a(t) - P_p(t) = L \frac{dF_L(t)}{dt} $$

$$ F_Z(t) = \frac{P_a(t) - P_p(t)}{Z} $$

$$ F_R(t) = \frac{P_p(t)}{R} $$

$$ F_C(t) = C \frac{dP_p(t)}{dt} $$

$$ F_Z(t) + F_L(t) = F_R(t) + F_C(t) $$

## 5. Parámetros de los tres casos

| Parámetro | Hipotenso | Normotenso | Hipertenso |
|---|---:|---:|---:|
| `Z` | 0.010 | 0.010 | 0.010 |
| `L` | 0.001 | 0.001 | 0.001 |
| `R` | 1.000 | 1.000 | 1.000 |
| `C` | 3.500 | 1.500 | 1.000 |

## 6. Modelo mediante ecuaciones diferenciales

$$ \dot{F}_L(t) = \frac{1}{L}P_a(t) - \frac{1}{L}P_p(t) $$

$$ \dot{P}_p(t) = \frac{1}{ZC}P_a(t) + \frac{1}{C}F_L(t) - \left(\frac{1}{ZC} + \frac{1}{RC}\right)P_p(t) $$

$$ x(t) = \begin{bmatrix} F_L(t) \\ P_p(t) \end{bmatrix} $$

$$ \dot{x}(t) = A x(t) + B u(t) $$

$$ A = \begin{bmatrix} 0 & -\frac{1}{L} \\ \frac{1}{C} & -\left(\frac{1}{ZC} + \frac{1}{RC}\right) \end{bmatrix} $$

$$ B = \begin{bmatrix} \frac{1}{L} \\ \frac{1}{ZC} \end{bmatrix} $$

$$ y(t) = C x(t) $$

$$ C = \begin{bmatrix} 0 & 1 \end{bmatrix}, \quad D = 0 $$

## 7. Funciones de transferencia

### 7.1 Desarrollo algebraico

Partiendo de:

$$ F_Z(t) + F_L(t) = F_C(t) + F_R(t) $$

con:

$$ F_Z(t) = \frac{P_a(t) - P_p(t)}{Z} $$

$$ F_L(t) = \frac{1}{L} \int [P_a(t) - P_p(t)] \, dt $$

$$ F_C(t) = C \frac{dP_p(t)}{dt} $$

$$ F_R(t) = \frac{P_p(t)}{R} $$

se obtiene:

$$ \frac{P_a(t) - P_p(t)}{Z} + \frac{1}{L} \int [P_a(t) - P_p(t)] dt = C \frac{dP_p(t)}{dt} + \frac{P_p(t)}{R} $$

Laplace con condiciones iniciales nulas:

$$ \frac{P_a(s) - P_p(s)}{Z} + \frac{P_a(s) - P_p(s)}{Ls} = C s P_p(s) + \frac{P_p(s)}{R} $$

$$ \left(\frac{1}{Z} + \frac{1}{Ls}\right) P_a(s) = \left( C s + \frac{1}{R} + \frac{1}{Z} + \frac{1}{Ls} \right) P_p(s) $$

$$ \frac{P_p(s)}{P_a(s)} = \frac{LRs + RZ}{CLRZ s^2 + L(R+Z)s + RZ} $$

Forma general:

$$ G(s) = \frac{R(Ls + Z)}{CLRZ s^2 + L(R+Z)s + RZ} $$

### Funciones de transferencia calculadas

| Caso | C | Función |
|---|---:|---|
| Hipotenso | 3.500 | $G_{hipo}(s) = \frac{0.001s+0.01}{3.5\times10^{-5}s^2+0.00101s+0.01}$ |
| Normotenso | 1.500 | $G_{normo}(s) = \frac{0.001s+0.01}{1.5\times10^{-5}s^2+0.00101s+0.01}$ |
| Hipertenso | 1.000 | $G_{hiper}(s) = \frac{0.001s+0.01}{1.0\times10^{-5}s^2+0.00101s+0.01}$ |

### Error en estado estacionario

$$ e_{ss} = \lim_{s \to 0} s P_a(s) \left[1 - \frac{P_p(s)}{P_a(s)}\right] $$

$$ e_{ss} = 0 $$

### Cálculo de los polos

$$ CLRZ s^2 + L(R+Z)s + RZ = 0 $$

$$ \lambda_{1,2} = \frac{-L(R+Z) \pm \sqrt{L^2(R+Z)^2 - 4CLRZ^2}}{2CLRZ} $$

## 8. Error y estabilidad

### 8.2 Polos

| Caso | Polo 1 | Polo 2 | Interpretación |
|---|---:|---:|---|
| Hipotenso | -14.429 + 8.805j | -14.429 - 8.805j | Estable y subamortiguado |
| Normotenso | -12.062 | -55.272 | Estable y sobreamortiguado |
| Hipertenso | -10.000 | -10.000 | Estable y críticamente amortiguado |

## 9. Señal de excitación

| Parámetro | Valor |
|---|---:|
| Minimum | -0.2 |
| Maximum | 1 |
| Seed | 106 |
| Sample time | 0.1 s |
| Intervalo | 0 a 15 s |

## 10. Implementación en MATLAB

$$ \dot{x} = A x + B u $$

$$ y = C x + D u $$

$$ G(s) = \frac{R(Ls+Z)}{CLRZ s^2 + L(R+Z)s + RZ} $$

## 12. Diseño de control

$$ e_{hipo}(t) = P_{p,normo}(t) - P_{p,hipo}(t) $$

$$ e_{hiper}(t) = P_{p,normo}(t) - P_{p,hiper}(t) $$

## 13. Sintonización PID

### Controlador hipotenso

$$ K_{P,hipo} = 458.18412862009 $$
$$ K_{I,hipo} = 1110647.27603615 $$
$$ K_{D,hipo} = 0.00626708429767374 $$

### Controlador hipertenso

$$ K_{P,hiper} = 129.978567122813 $$
$$ K_{I,hiper} = 312762.858715908 $$
$$ K_{D,hiper} = 0.00174611348908487 $$

| Controlador | Kp | Ki | Kd | Observaciones |
|---|---:|---:|---:|---|
| Hipotenso | 458.1841 | 1110647.2760 | 0.006267 | Ki alto por C=3.5, polos complejos -14.429±8.805j, respuesta oscilatoria |
| Hipertenso | 129.9785 | 312762.8587 | 0.001746 | Ki menor por C=1.0, polos críticos -10.000, sistema más rígido |
Ambos controladores usan estructura PID con filtro: $C_{PID}(s)=K_P + \frac{K_I}{s} + \frac{K_D N s}{s+N}$

## 14. Análisis en lazo cerrado

Comparar $P_{p,normo}(t)$, $P_{p,hipo}(t)$ y $P_{p,hipo,PID}(t)$ para cada caso.

## 15. Implementación en Python

Implementar $G_{hipo}(s)$, $G_{normo}(s)$, $G_{hiper}(s)$ con las mismas condiciones que MATLAB.

## 16. Verificación cruzada

| Modelo | Hipotenso | Normotenso | Hipertenso |
|---|:---:|:---:|:---:|
| Ecuaciones de estado | ✓ | ✓ | ✓ |
| Función de transferencia | ✓ | ✓ | ✓ |
| Simscape Electrical | ✓ | ✓ | ✓ |
| MATLAB (Live Script) | ✓ | ✓ | ✓ |
| Python | ✓ | ✓ | ✓ |

✓ = Respuesta coincidente / Verificado

## 17. Diagrama biológico

## 18. Resultados y discusión
Incluir matrices A, B, C, D, funciones de transferencia, polos, error, ganancias PID.

## 19. Conclusiones

## 19. Conclusiones

> **Conclusión de la estudiante:**
> Kenia Yasdit Contreras Jiménez - 23212188

El modelo Windkessel de cuatro elementos permitió representar el sistema arterial con un circuito eléctrico, donde `Z` es la impedancia, `C` la distensibilidad, `R` la resistencia periférica y `L` la inertancia. Aunque tiene cuatro elementos, solo `C` y `L` guardan energía, por eso el sistema es de segundo orden.

Al cambiar solo `C` se vio el efecto en la dinámica:
- **Hipotenso (C=3.5):** polos complejos $-14.429 \pm 8.805j$, respuesta subamortiguada y oscilatoria, más elástico.
- **Normotenso (C=1.5):** polos reales $-12.062$ y $-55.272$, sobreamortiguado, usado como referencia.
- **Hipertenso (C=1.0):** polos en $-10.000$, críticamente amortiguado, más rígido.

Los tres casos son estables (polos con parte real negativa) y con error cero ante escalón $e_{ss}=0$.

En lazo abierto, con la misma señal aleatoria (min=-0.2, max=1, seed=106, 0-15s), el hipotenso tuvo mayor amplitud y oscilación, y el hipertenso una respuesta más lenta y atenuada.

Con el normotenso como referencia se diseñaron dos controles con error $e(t)=P_{p,normo}(t)-P_{p,caso}(t)$. El PID se sintonizó con Tune:
- Hipotenso: Kp=458.18, Ki=1110647.27, Kd=0.00626
- Hipertenso: Kp=129.97, Ki=312762.85, Kd=0.00174

El hipotenso necesitó ganancias más altas por ser más elástico. Ambos controles en lazo cerrado redujeron el error y mejoraron el seguimiento de la referencia.

Los resultados coincidieron entre ecuaciones de estado, función de transferencia, Simscape, MATLAB y Python al usar los mismos parámetros y la misma señal.

Como limitación, el modelo no considera propagación de onda ni regulación autonómica, pero para la práctica permitió entender la relación entre distensibilidad y presión y aplicar control clásico.

**Nota:** Simulación con fines académicos, no es recomendación clínica.

## 24. Referencias
1. M. C. Khoo, Physiological Control Systems, 2nd ed.
2. F. C. Hoppensteadt and C. S. Peskin, Modeling and Simulation in Medicine and the Life Sciences
3. J. E. Hall, Guyton and Hall Textbook of Medical Physiology, 14th ed.
4. K. Ogata, Ingeniería de Control Moderna
5. N. S. Nise, Control Systems Engineering
6. P. A. Valle, Syllabus MSF

## Uso académico
Práctica de Modelado y control del sistema cardiovascular mediante el modelo Windkessel. Fines exclusivamente académicos.
