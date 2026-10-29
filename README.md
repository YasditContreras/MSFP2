[![Open in MATLAB Online](https://www.mathworks.com/images/responsive/global/open-in-matlab-online.svg)](https://matlab.mathworks.com/)

# Práctica 5.4 — Modelado y control del sistema cardiovascular mediante el modelo Windkessel

Repositorio académico de la asignatura **Modelado de Sistemas Fisiológicos**, correspondiente al programa de **Ingeniería Biomédica** del Tecnológico Nacional de México / Instituto Tecnológico de Tijuana.

Esta práctica estudia el **modelo Windkessel de cuatro elementos** para representar la dinámica del sistema cardiovascular. Se comparan tres condiciones simuladas —**hipotensa, normotensa e hipertensa**— y se diseñan estrategias de control *in silico* para reducir la diferencia entre los casos hipotenso/hipertenso y la respuesta de referencia normotensa.

> **Importante:** las estrategias de control desarrolladas en esta práctica tienen fines exclusivamente académicos y de simulación. No constituyen una estrategia terapéutica ni una recomendación para el tratamiento de alteraciones de la presión arterial.

---

## Datos de la práctica

**Docente:** Dr. Paul Antonio Valle Trujillo  
**Departamento:** Ingeniería Eléctrica y Electrónica  
**Institución:** Tecnológico Nacional de México / Instituto Tecnológico de Tijuana  
**Asignatura:** Modelado de Sistemas Fisiológicos  
**Programa:** Ingeniería Biomédica  
**Estudiante:** Nombre completo · Número de control · correo institucional

**Repositorio de la asignatura:** https://github.com/DrPaulValle/MSF-IBF1020  
**Sede:** Tijuana, Baja California, México

---

<a id="contenido"></a>
## Contenido

1. [Resumen](#resumen)
2. [Competencia y objetivos](#objetivos)
3. [Introducción al modelo Windkessel](#introduccion)
4. [Variables y analogía eléctrica](#analogia)
5. [Parámetros de los tres casos](#parametros)
6. [Modelo mediante ecuaciones diferenciales](#ecuaciones)
7. [Funciones de transferencia](#transferencia)
8. [Error en estado estacionario y estabilidad](#estabilidad)
9. [Señal de excitación y condiciones de simulación](#senal)
10. [Implementación en MATLAB, Simulink y Simscape Electrical](#matlab)
11. [Análisis en lazo abierto](#lazo-abierto)
12. [Diseño de los sistemas de control](#control)
13. [Sintonización de los controladores PID](#pid)
14. [Análisis en lazo cerrado](#lazo-cerrado)
15. [Implementación en Python](#python)
16. [Verificación cruzada](#verificacion)
17. [Diagrama biológico](#diagrama)
18. [Resultados y discusión](#resultados)
19. [Conclusiones](#conclusiones)
20. [Actividades y lista de comprobación](#actividades)
21. [Estructura del repositorio](#estructura)
22. [Requisitos](#requisitos)
23. [Reproducibilidad y entregables](#entregables)
24. [Referencias](#referencias)

---

<a id="resumen"></a>
## 1. Resumen

El objetivo de esta práctica es **modelar, analizar y controlar el comportamiento dinámico del sistema cardiovascular** utilizando el modelo Windkessel de cuatro elementos. Este modelo representa propiedades hemodinámicas del sistema arterial mediante cuatro elementos equivalentes: **impedancia característica `Z`**, **distensibilidad arterial `C`**, **resistencia periférica `R`** e **inertancia arterial `L`**.

Aunque el modelo contiene cuatro elementos, solamente `C` y `L` almacenan energía de manera independiente, por lo que su dinámica puede representarse mediante **dos variables de estado** y corresponde a un sistema de segundo orden.

Durante la práctica se estudian tres conjuntos de parámetros:

- **Hipotenso:** `C = 3.500`
- **Normotenso:** `C = 1.500`
- **Hipertenso:** `C = 1.000`

Los parámetros `Z`, `L` y `R` se mantienen constantes. El modelo **normotenso** se utiliza como referencia, mientras que los modelos **hipotenso** e **hipertenso** se consideran los casos a controlar.

La práctica se desarrolla exclusivamente mediante **experimentación in silico**, utilizando MATLAB/Simulink, Simscape Electrical y Python/Visual Studio Code. Finalmente, se comparan las diferentes representaciones del modelo y se verifica la consistencia de sus resultados.

---

<a id="objetivos"></a>
## 2. Competencia y objetivos

### Competencia a desarrollar

Modelizar sistemas fisiológicos mediante circuitos eléctricos equivalentes, ecuaciones diferenciales y funciones de transferencia para analizar su comportamiento dinámico y diseñar estrategias de control mediante técnicas de control clásico.

### Objetivo general

Analizar el modelo Windkessel de cuatro elementos como representación del sistema cardiovascular, comparar las respuestas de los casos hipotenso, normotenso e hipertenso y diseñar controladores PID que reduzcan la diferencia entre cada caso y la respuesta de referencia normotensa.

### Objetivos específicos

- Identificar las variables y parámetros del modelo Windkessel.
- Relacionar `Z`, `C`, `R` y `L` con sus propiedades hemodinámicas.
- Formular el modelo mediante ecuaciones diferenciales ordinarias.
- Obtener la representación en espacio de estados.
- Obtener las funciones de transferencia de los casos hipotenso, normotenso e hipertenso.
- Analizar el error en estado estacionario ante una entrada escalón.
- Calcular y analizar los polos de los tres modelos.
- Implementar los modelos mediante ecuaciones de estado, funciones de transferencia y Simscape Electrical.
- Aplicar exactamente la misma señal aleatoria a los tres casos.
- Comparar las respuestas en lazo abierto.
- Utilizar el modelo normotenso como referencia para construir dos sistemas de control.
- Diseñar y sintonizar dos controladores PID mediante la herramienta **Tune** de Simulink.
- Comparar las respuestas en lazo cerrado.
- Reproducir los resultados mediante MATLAB y Python.
- Elaborar un diagrama biológico que relacione el modelo con las estructuras cardiovasculares.
- Verificar la consistencia entre las diferentes plataformas de simulación.
- Documentar los resultados y evidencias en GitHub.

---

<a id="introduccion"></a>
## 3. Introducción al modelo Windkessel

El sistema arterial presenta propiedades dinámicas relacionadas con la resistencia periférica, la distensibilidad arterial, la impedancia característica de la región proximal y la inercia asociada al movimiento de la sangre.

El modelo Windkessel permite representar estas propiedades mediante un circuito equivalente. Su desarrollo parte de modelos más simples, como el Windkessel de dos elementos, y se amplía hasta el modelo de cuatro elementos utilizado en esta práctica.

La correspondencia entre las variables fisiológicas y eléctricas es:

| Variable o elemento | Equivalente eléctrico | Interpretación fisiológica |
|---|---|---|
| Presión arterial | Voltaje | Diferencia de presión del sistema cardiovascular |
| Flujo sanguíneo | Corriente | Movimiento de sangre |
| `Z` | Impedancia/resistencia característica | Impedancia característica de la región proximal |
| `C` | Capacitancia | Distensibilidad arterial y almacenamiento de volumen |
| `R` | Resistencia | Resistencia periférica |
| `L` | Inductancia | Inertancia asociada al movimiento de la sangre |

El modelo permite estudiar cómo los cambios en la **distensibilidad arterial `C`** modifican la respuesta dinámica. En esta práctica, un valor mayor de `C` representa el caso hipotenso y un valor menor representa el caso hipertenso.

---

<a id="analogia"></a>
## 4. Variables y analogía eléctrica

Las variables utilizadas son:

- `P_a(t)`: presión arterial de entrada.
- `P_p(t)`: presión sobre la distensibilidad arterial.
- `F_L(t)`: flujo a través de la inertancia arterial.
- `F_Z(t)`: flujo a través de la impedancia característica.
- `F_R(t)`: flujo asociado con la resistencia periférica.
- `F_C(t)`: flujo asociado con la distensibilidad.

Las variables de estado seleccionadas son:

$$
x_1(t)=F_L(t)
$$

$$
x_2(t)=P_p(t)
$$

y la entrada es:

$$
u(t)=P_a(t)
$$

La salida considerada es:

$$
y(t)=P_p(t)
$$

### Relaciones constitutivas

Para la inertancia:

$$
P_a(t)-P_p(t)=L\frac{dF_L(t)}{dt}
$$

Para la impedancia característica:

$$
F_Z(t)=\frac{P_a(t)-P_p(t)}{Z}
$$

Para la resistencia periférica:

$$
F_R(t)=\frac{P_p(t)}{R}
$$

Para la distensibilidad:

$$
F_C(t)=C\frac{dP_p(t)}{dt}
$$

La conservación del flujo en el nodo correspondiente a `P_p(t)` es:

$$
F_Z(t)+F_L(t)=F_R(t)+F_C(t)
$$

---

<a id="parametros"></a>
## 5. Parámetros de los tres casos

Los valores indicados en la práctica son:

| Parámetro | Hipotenso | Normotenso | Hipertenso | Unidades |
|---|---:|---:|---:|---|
| `Z` | 0.010 | 0.010 | 0.010 | mmHg·s·ml⁻¹ |
| `L` | 0.001 | 0.001 | 0.001 | mmHg·s²·ml⁻¹ |
| `R` | 1.000 | 1.000 | 1.000 | mmHg·s·ml⁻¹ |
| `C` | 3.500 | 1.500 | 1.000 | ml·mmHg⁻¹ |

La diferencia entre los tres conjuntos de parámetros se establece **modificando únicamente `C`**.

- El caso **hipotenso** presenta mayor distensibilidad.
- El caso **normotenso** funciona como referencia.
- El caso **hipertenso** presenta menor distensibilidad y mayor rigidez arterial.

---

<a id="ecuaciones"></a>
## 6. Modelo mediante ecuaciones diferenciales

A partir de las relaciones anteriores:

$$
\boxed{
\dot F_L(t)=
\frac{1}{L}P_a(t)-\frac{1}{L}P_p(t)
}
$$

y:

$$
\boxed{
\dot P_p(t)=
\frac{1}{ZC}P_a(t)
+\frac{1}{C}F_L(t)
-\left(\frac{1}{ZC}+\frac{1}{RC}\right)P_p(t)
}
$$

Por lo tanto:

$$
x(t)=
\begin{bmatrix}
F_L(t)\\
P_p(t)
\end{bmatrix}
$$

y el modelo queda expresado como:

$$
\boxed{\dot{x}(t)=Ax(t)+Bu(t)}
$$

donde:

$$
A=
\begin{bmatrix}
0 & -\frac{1}{L}\\
\frac{1}{C} &
-\left(\frac{1}{ZC}+\frac{1}{RC}\right)
\end{bmatrix}
$$

$$
B=
\begin{bmatrix}
\frac{1}{L}\\
\frac{1}{ZC}
\end{bmatrix}
$$

La ecuación de salida es:

$$
\boxed{y(t)=Cx(t)}
$$

con:

$$
C=
\begin{bmatrix}
0 & 1
\end{bmatrix},
\qquad
D=0
$$

> En MATLAB se recomienda utilizar variables con nombres diferentes para la matriz de salida `C` y el parámetro fisiológico `C` de distensibilidad, para evitar confusiones.

---

<a id="transferencia"></a>
## 7. Funciones de transferencia

## 7.1 Desarrollo algebraico de los cálculos realizados

Los cálculos entregados complementan el desarrollo anterior y muestran la obtención de la función de transferencia a partir de la ecuación de conservación de flujo del circuito equivalente.

Partiendo de:

$$
F_Z(t)+F_L(t)=F_C(t)+F_R(t)
$$

con:

$$
F_Z(t)=\frac{P_a(t)-P_p(t)}{Z}
$$

$$
F_L(t)=\frac{1}{L}\int [P_a(t)-P_p(t)]\,dt
$$

$$
F_C(t)=C\frac{dP_p(t)}{dt}
$$

$$
F_R(t)=\frac{P_p(t)}{R}
$$

se obtiene el modelo integro-diferencial:

$$
\boxed{
\frac{P_a(t)-P_p(t)}{Z}
+\frac{1}{L}\int[P_a(t)-P_p(t)]dt
=
C\frac{dP_p(t)}{dt}+\frac{P_p(t)}{R}
}
$$

Aplicando la transformada de Laplace con condiciones iniciales nulas:

$$
\frac{P_a(s)-P_p(s)}{Z}
+
\frac{P_a(s)-P_p(s)}{Ls}
=
CsP_p(s)+\frac{P_p(s)}{R}
$$

Al realizar el procedimiento algebraico:

$$
\left(\frac{1}{Z}+\frac{1}{Ls}\right)P_a(s)
=
\left(
Cs+\frac{1}{R}+\frac{1}{Z}+\frac{1}{Ls}
\right)P_p(s)
$$

y, finalmente:

$$
\boxed{
\frac{P_p(s)}{P_a(s)}
=
\frac{LRs+RZ}
{CLRZs^2+L(R+Z)s+RZ}
}
$$

Esta expresión coincide con la función de transferencia utilizada para los tres casos de la práctica.

### Error en estado estacionario

Para una entrada escalón unitario:

$$
P_a(s)=\frac{1}{s}
$$

el error se define como:

$$
e(s)=P_a(s)-P_p(s)
$$

y, utilizando el teorema del valor final:

$$
e_{ss}
=
\lim_{s\rightarrow0}
sP_a(s)
\left[
1-\frac{P_p(s)}{P_a(s)}
\right]
$$

Con la función de transferencia obtenida:

$$
\boxed{e_{ss}=0}
$$

Por lo tanto, para una entrada escalón unitario, el error en estado estacionario es de **0 V** en la representación eléctrica utilizada en los cálculos.

### Cálculo de los polos

Los polos se obtienen a partir del denominador:

$$
CLRZs^2+L(R+Z)s+RZ=0
$$

Definiendo:

$$
a=CLRZ,\qquad b=L(R+Z),\qquad c=RZ
$$

la solución general es:

$$
\boxed{
\lambda_{1,2}
=
\frac{-L(R+Z)\pm
\sqrt{L^2(R+Z)^2-4CLRZ^2}}
{2CLRZ}
}
$$


Aplicando la transformada de Laplace con condiciones iniciales nulas y considerando:

$$
G(s)=\frac{P_p(s)}{P_a(s)}
$$

se obtiene:

$$
\boxed{
G(s)=
\frac{R(Ls+Z)}
{CLRZs^2+L(R+Z)s+RZ}
}
$$

A partir de esta expresión deben obtenerse:

$$
G_{hipo}(s)
$$

$$
G_{normo}(s)
$$

$$
G_{hiper}(s)
$$

sustituyendo los respectivos valores de `C`.

### Funciones de transferencia calculadas

Utilizando:

$$
Z=0.010,\qquad L=0.001,\qquad R=1
$$

y modificando únicamente `C`, se obtienen:

| Caso | `C` | Función de transferencia |
|---|---:|---|
| Hipotenso | `3.500` | $\displaystyle G_{hipo}(s)=\frac{0.001s+0.01}{3.5\times10^{-5}s^2+0.00101s+0.01}$ |
| Normotenso | `1.500` | $\displaystyle G_{normo}(s)=\frac{0.001s+0.01}{1.5\times10^{-5}s^2+0.00101s+0.01}$ |
| Hipertenso | `1.000` | $\displaystyle G_{hiper}(s)=\frac{0.001s+0.01}{1.0\times10^{-5}s^2+0.00101s+0.01}$ |


### Orden del sistema

El denominador contiene un término en `s²`, por lo que las tres funciones de transferencia corresponden a sistemas de **segundo orden**.

Esto concuerda con la presencia de dos elementos independientes de almacenamiento de energía:

- `L`: inertancia.
- `C`: distensibilidad.

---

<a id="estabilidad"></a>
## 8. Error en estado estacionario y estabilidad

### 8.1 Error en estado estacionario

Para cada modelo se debe aplicar una entrada escalón y determinar:

1. La respuesta final.
2. El valor final de la entrada.
3. El error en estado estacionario.

Registrar los resultados:

| Caso | Valor final de la salida | Error en estado estacionario |
|---|---:|---:|
| Hipotenso | `[completar]` | `[completar]` |
| Normotenso | `[completar]` | `[completar]` |
| Hipertenso | `[completar]` | `[completar]` |

### 8.2 Polos

Los polos se obtienen de:

$$
CLRZs^2+L(R+Z)s+RZ=0
$$

Los cálculos entregados proporcionan los siguientes polos:

| Caso | Polo 1 | Polo 2 | Interpretación |
|---|---:|---:|---|
| Hipotenso | `-14.429 + 8.805j` | `-14.429 - 8.805j` | Estable y subamortiguado |
| Normotenso | `-12.062` | `-55.272` | Estable y sobreamortiguado |
| Hipertenso | `-10.000` | `-10.000` | Estable y críticamente amortiguado |

En los tres casos, los polos tienen parte real negativa, por lo que el sistema es estable en lazo abierto.

La clasificación observada en los cálculos muestra que el cambio de `C` modifica de forma importante la naturaleza de la respuesta:

- **Hipotenso:** aparecen polos complejos conjugados, por lo que se espera una respuesta oscilatoria amortiguada.
- **Normotenso:** aparecen dos polos reales distintos, por lo que se espera una respuesta sobreamortiguada.
- **Hipertenso:** aparecen dos polos reales coincidentes, correspondiente al caso críticamente amortiguado.

Agregar posteriormente el gráfico del plano complejo como evidencia de estos resultados.

---

<a id="senal"></a>
## 9. Señal de excitación y condiciones de simulación

La práctica solicita utilizar el bloque **Uniform Random Number** de Simulink con:

| Parámetro | Valor |
|---|---:|
| Minimum | `-0.2` |
| Maximum | `1` |
| Seed | `106` |
| Sample time | `0.1 s` |
| Intervalo de simulación | `0 ≤ t ≤ 15 s` |

Es indispensable utilizar **exactamente la misma realización de la señal aleatoria** para los modelos hipotenso, normotenso e hipertenso.

De esta manera, las diferencias observadas entre las respuestas deberán atribuirse a los parámetros de cada modelo y no a excitaciones diferentes.

---

<a id="matlab"></a>
## 10. Implementación en MATLAB, Simulink y Simscape Electrical

Para cada una de las tres condiciones cardiovasculares se deben construir tres representaciones:

### a) Modelo mediante ecuaciones de estado

Implementar:

$$
\dot{x}=Ax+Bu
$$

y:

$$
y=Cx+Du
$$

### b) Modelo mediante función de transferencia

Implementar:

$$
G(s)=
\frac{R(Ls+Z)}
{CLRZs^2+L(R+Z)s+RZ}
$$

### c) Circuito equivalente mediante Simscape Electrical

Construir el circuito Windkessel utilizando los elementos equivalentes `Z`, `C`, `R` y `L`.

### Verificación

Las tres representaciones deben producir respuestas consistentes cuando se utilicen:

- Los mismos parámetros.
- Las mismas condiciones iniciales.
- La misma señal de entrada.
- El mismo intervalo de simulación.

---

<a id="lazo-abierto"></a>
## 11. Análisis en lazo abierto

Aplicar la misma señal de excitación a los tres modelos y registrar la presión:

$$
P_{p,hipo}(t)
$$

$$
P_{p,normo}(t)
$$

$$
P_{p,hiper}(t)
$$

### Aspectos a analizar

- Diferencia de amplitud entre las respuestas.
- Diferencias en el comportamiento transitorio.
- Influencia de la distensibilidad `C`.
- Relación entre los resultados y la interpretación fisiológica del modelo.
- Consistencia entre ecuaciones de estado, función de transferencia y Simscape Electrical.

### Evidencia

Agregar aquí las figuras correspondientes:

```text
resultados/
├── lazo_abierto_hipotenso.pdf
├── lazo_abierto_normotenso.pdf
└── lazo_abierto_hipertenso.pdf
```

---

<a id="control"></a>
## 12. Diseño de los sistemas de control

El modelo **normotenso** se utiliza como referencia.

Se construyen dos sistemas de control independientes:

1. **Normotenso → Hipotenso**
2. **Normotenso → Hipertenso**

### Caso hipotenso

La señal de error es:

$$
\boxed{
e_{hipo}(t)=P_{p,normo}(t)-P_{p,hipo}(t)
}
$$

### Caso hipertenso

La señal de error es:

$$
\boxed{
e_{hiper}(t)=P_{p,normo}(t)-P_{p,hiper}(t)
}
$$

Cada sistema deberá incorporar un bloque **PID Controller**.

El objetivo del control es reducir la diferencia entre la respuesta del caso correspondiente y la respuesta del modelo normotenso.

---

<a id="pid"></a>
## 13. Sintonización de los controladores PID

Utilizar la herramienta **Tune** del bloque `PID Controller` de Simulink.

Se deben obtener de manera independiente:

### Controlador hipotenso

$$
K_{P,hipo}=[\text{completar}]
$$

$$
K_{I,hipo}=[\text{completar}]
$$

$$
K_{D,hipo}=[\text{completar}]
$$

### Controlador hipertenso

$$
K_{P,hiper}=[\text{completar}]
$$

$$
K_{I,hiper}=[\text{completar}]
$$

$$
K_{D,hiper}=[\text{completar}]
$$

### Evidencia de sintonización

Agregar capturas de la herramienta **Tune** y registrar:

| Controlador | `Kp` | `Ki` | `Kd` | Observaciones |
|---|---:|---:|---:|---|
| Hipotenso | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| Hipertenso | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

La sintonización debe buscar una respuesta estable y una reducción del error entre el caso correspondiente y la respuesta normotensa.

---

<a id="lazo-cerrado"></a>
## 14. Análisis en lazo cerrado

Repetir las simulaciones utilizando los controladores obtenidos.

### Caso hipotenso

Comparar:

$$
P_{p,normo}(t)
$$

$$
P_{p,hipo}(t)
$$

$$
P_{p,hipo,PID}(t)
$$

### Caso hipertenso

Comparar:

$$
P_{p,normo}(t)
$$

$$
P_{p,hiper}(t)
$$

$$
P_{p,hiper,PID}(t)
$$

### Discusión

Analizar:

- Reducción del error.
- Seguimiento de la referencia.
- Comportamiento transitorio.
- Sobreimpulso u oscilaciones, si aparecen.
- Tiempo necesario para acercarse a la respuesta de referencia.
- Diferencias entre el controlador hipotenso y el hipertenso.
- Efecto de las ganancias `Kp`, `Ki` y `Kd`.

---

<a id="python"></a>
## 15. Implementación en Python

Utilizar **Python mediante Visual Studio Code** para implementar las funciones de transferencia:

```text
G_hipo(s)
G_normo(s)
G_hiper(s)
```

El programa debe:

1. Definir los parámetros de los tres casos.
2. Construir las funciones de transferencia.
3. Utilizar la misma señal de entrada empleada en MATLAB/Simulink.
4. Obtener las respuestas en lazo abierto.
5. Incorporar las ganancias PID obtenidas mediante `Tune`.
6. Construir los sistemas de lazo cerrado.
7. Generar las figuras correspondientes.
8. Guardar los resultados.

### Comparación MATLAB–Python

Las condiciones deben ser equivalentes:

| Condición | MATLAB/Simulink | Python |
|---|---|---|
| Parámetros | Iguales | Iguales |
| Entrada | Misma realización | Misma realización |
| Condiciones iniciales | Iguales | Iguales |
| PID | Ganancias obtenidas con Tune | Mismas ganancias |
| Tiempo de simulación | 0–15 s | 0–15 s |

---

<a id="verificacion"></a>
## 16. Verificación cruzada

Comparar los resultados obtenidos mediante:

1. Ecuaciones de estado en Simulink.
2. Funciones de transferencia en Simulink.
3. Circuito Windkessel en Simscape Electrical.
4. Cuaderno computacional de MATLAB.
5. Código desarrollado en Python.

### Matriz de verificación

| Modelo | Hipotenso | Normotenso | Hipertenso |
|---|---|---|---|
| Ecuaciones de estado | `[ ]` | `[ ]` | `[ ]` |
| Función de transferencia | `[ ]` | `[ ]` | `[ ]` |
| Simscape Electrical | `[ ]` | `[ ]` | `[ ]` |
| MATLAB | `[ ]` | `[ ]` | `[ ]` |
| Python | `[ ]` | `[ ]` | `[ ]` |

Si existen diferencias, discutir si pueden deberse a:

- Método numérico.
- Discretización.
- Configuración de la señal aleatoria.
- Condiciones iniciales.
- Implementación del modelo.
- Parámetros utilizados.

---

<a id="diagrama"></a>
## 17. Diagrama biológico

Elaborar mediante **BioRender** o una herramienta equivalente un diagrama que relacione el modelo Windkessel con las estructuras y propiedades fisiológicas representadas.

El diagrama debe identificar como mínimo:

- Corazón.
- Aorta.
- Grandes arterias.
- Vasos periféricos.
- Flujo sanguíneo.
- Presión arterial.
- Distensibilidad arterial.
- Resistencia periférica.

También debe establecer la relación entre las estructuras fisiológicas y:

```text
Z → impedancia característica
C → distensibilidad arterial
R → resistencia periférica
L → inertancia arterial
```

Agregar el archivo, por ejemplo:

```text
figuras/
└── diagrama_biologico_windkessel.png
```

---

<a id="resultados"></a>
## 18. Resultados y discusión

Esta sección debe contener **resultados propios de la ejecución de la práctica**, no valores inventados.

### 18.1 Resultados matemáticos

Incluir:

- Ecuaciones diferenciales.
- Matrices `A`, `B`, `C` y `D`.
- Funciones de transferencia.
- Polos.
- Error en estado estacionario.

### 18.2 Resultados en lazo abierto

Comparar los tres casos:

- Hipotenso.
- Normotenso.
- Hipertenso.

Explicar cómo la modificación de `C` afecta la respuesta.

### 18.3 Resultados de los controladores

Incluir las ganancias:

| Controlador | `Kp` | `Ki` | `Kd` |
|---|---:|---:|---:|
| Normotenso–Hipotenso | `[ ]` | `[ ]` | `[ ]` |
| Normotenso–Hipertenso | `[ ]` | `[ ]` | `[ ]` |

### 18.4 Resultados en lazo cerrado

Mostrar y comparar:

- Referencia normotensa.
- Caso sin controlar.
- Caso controlado.

### 18.5 Comparación entre plataformas

Explicar si MATLAB/Simulink, Simscape Electrical y Python presentan respuestas equivalentes y, en caso de existir diferencias, justificar su posible origen.

---

<a id="conclusiones"></a>
## 19. Conclusiones

La conclusión debe redactarse después de completar las simulaciones y debe responder, como mínimo:

- ¿Qué permitió comprender el modelo Windkessel?
- ¿Cómo afectó el cambio de `C` a la dinámica cardiovascular simulada?
- ¿Qué diferencias se observaron entre los casos hipotenso, normotenso e hipertenso?
- ¿Qué efecto tuvieron los controladores PID?
- ¿Los resultados fueron consistentes entre MATLAB, Simulink, Simscape Electrical y Python?
- ¿Qué limitaciones presentó el modelo y la simulación?

> **Conclusión del estudiante:**  
> `[Redactar aquí la conclusión final a partir de los resultados obtenidos.]`

---

<a id="actividades"></a>
## 20. Actividades y lista de comprobación

### Formulación y análisis

- [ ] Identificar `Z`, `C`, `R`, `L`, `P_a(t)`, `P_p(t)` y `F_L(t)`.
- [ ] Relacionar cada elemento con su propiedad hemodinámica.
- [ ] Formular las ecuaciones diferenciales.
- [ ] Obtener las matrices de espacio de estados.
- [ ] Obtener `G_hipo(s)`, `G_normo(s)` y `G_hiper(s)`.
- [ ] Determinar el error en estado estacionario.
- [ ] Calcular los polos.
- [ ] Representar los polos en el plano complejo.
- [ ] Analizar la estabilidad.

### MATLAB / Simulink / Simscape

- [ ] Implementar las ecuaciones de estado.
- [ ] Implementar las funciones de transferencia.
- [ ] Implementar los circuitos mediante Simscape Electrical.
- [ ] Configurar Uniform Random Number con `min=-0.2`, `max=1`, `seed=106`, `Ts=0.1 s`.
- [ ] Simular de `0` a `15 s`.
- [ ] Utilizar la misma señal para los tres modelos.
- [ ] Comparar las respuestas en lazo abierto.

### Control

- [ ] Utilizar el modelo normotenso como referencia.
- [ ] Construir el sistema normotenso–hipotenso.
- [ ] Construir el sistema normotenso–hipertenso.
- [ ] Incorporar un PID en cada sistema.
- [ ] Utilizar `Tune`.
- [ ] Registrar `Kp`, `Ki` y `Kd`.
- [ ] Comparar las respuestas en lazo cerrado.
- [ ] Analizar el error y la respuesta transitoria.

### Python

- [ ] Implementar las tres funciones de transferencia.
- [ ] Reproducir la misma entrada.
- [ ] Obtener las respuestas en lazo abierto.
- [ ] Incorporar las ganancias PID.
- [ ] Simular los dos sistemas de lazo cerrado.
- [ ] Generar las figuras.
- [ ] Comparar Python con MATLAB/Simulink.

### Documentación

- [ ] Elaborar el diagrama biológico.
- [ ] Incorporar capturas de las simulaciones.
- [ ] Incorporar figuras de resultados.
- [ ] Documentar las ganancias de los controladores.
- [ ] Redactar la discusión.
- [ ] Redactar las conclusiones.
- [ ] Completar `README.md`.
- [ ] Completar `CITATION.cff`.

---

<a id="estructura"></a>
## 21. Estructura del repositorio

Se recomienda organizar el repositorio de la siguiente manera:

```text
.
├── README.md
├── CITATION.cff
│
├── matlab/
│   ├── practica_windkessel.mlx
│   └── funciones/
│
├── simulink/
│   ├── windkessel_hipotenso.slx
│   ├── windkessel_normotenso.slx
│   ├── windkessel_hipertenso.slx
│   ├── control_hipotenso.slx
│   └── control_hipertenso.slx
│
├── python/
│   └── windkessel.py
│
├── simscape/
│   └── modelo_windkessel/
│
├── figuras/
│   ├── polos.png
│   ├── lazo_abierto.png
│   ├── lazo_cerrado_hipotenso.png
│   ├── lazo_cerrado_hipertenso.png
│   └── diagrama_biologico_windkessel.png
│
├── resultados/
│   ├── matlab/
│   ├── python/
│   └── capturas_simulink/
│
└── evidencias/
    └── capturas/
```

Los nombres pueden modificarse, pero las rutas del `README.md` deben mantenerse actualizadas.

---

<a id="requisitos"></a>
## 22. Requisitos

### Software

- MATLAB.
- Simulink.
- Simscape Electrical.
- Herramientas para utilizar el bloque `PID Controller` y la herramienta `Tune`.
- Python.
- Visual Studio Code.
- Git y GitHub.
- BioRender o herramienta equivalente para el diagrama biológico.

### Archivos y recursos

El repositorio final debe contener los archivos necesarios para reproducir:

- Modelo mediante ecuaciones de estado.
- Modelo mediante función de transferencia.
- Circuito Windkessel.
- Sistemas de control.
- Código MATLAB.
- Código Python.
- Señal de excitación.
- Figuras y capturas.
- Diagrama biológico.
- `README.md`.
- `CITATION.cff`.

---

<a id="entregables"></a>
## 23. Reproducibilidad y entregables

### Secuencia de reproducción

1. Identificar las variables y parámetros del modelo.
2. Formular las ecuaciones diferenciales.
3. Obtener el modelo en espacio de estados.
4. Obtener las tres funciones de transferencia.
5. Calcular el error en estado estacionario.
6. Calcular y graficar los polos.
7. Implementar los tres modelos en Simulink/Simscape.
8. Configurar la señal `Uniform Random Number`.
9. Ejecutar las simulaciones de `0` a `15 s`.
10. Comparar los tres casos en lazo abierto.
11. Construir los sistemas normotenso–hipotenso y normotenso–hipertenso.
12. Sintonizar ambos PID mediante `Tune`.
13. Ejecutar las simulaciones en lazo cerrado.
14. Reproducir los resultados en MATLAB.
15. Reproducir los resultados en Python.
16. Comparar todas las plataformas.
17. Elaborar el diagrama biológico.
18. Documentar resultados, discusión y conclusiones.
19. Organizar el repositorio y completar `CITATION.cff`.

### Entregables mínimos

| Entregable | Evidencia |
|---|---|
| Desarrollo matemático | Ecuaciones y procedimiento |
| Espacio de estados | Matrices `A`, `B`, `C`, `D` |
| Funciones de transferencia | `G_hipo`, `G_normo`, `G_hiper` |
| Parámetros | Tabla de los tres casos |
| Análisis de estabilidad | Polos y plano complejo |
| Simulink | Modelos de los tres casos |
| Simscape Electrical | Circuito Windkessel |
| Lazo abierto | Figuras comparativas |
| Controladores | Dos PID y ganancias |
| Lazo cerrado | Figuras comparativas |
| MATLAB | Cuaderno y figuras |
| Python | Código y figuras |
| Diagrama biológico | Figura con relaciones fisiológicas |
| Verificación | Comparación entre plataformas |
| Documentación | `README.md` |
| Citación | `CITATION.cff` |

---

<a id="referencias"></a>
## 24. Referencias

1. M. C. Khoo, *Physiological Control Systems: Analysis, Simulation, and Estimation*, 2nd ed., IEEE Press, 2018.

2. F. C. Hoppensteadt and C. S. Peskin, *Modeling and Simulation in Medicine and the Life Sciences*, Springer.

3. J. E. Hall, *Guyton and Hall Textbook of Medical Physiology*, 14th ed., Elsevier, 2021.

4. K. Ogata, *Ingeniería de Control Moderna*, 5.ª ed., Pearson Educación, 2010.

5. N. S. Nise, *Control Systems Engineering*, 8th ed., John Wiley & Sons, 2020.

6. P. A. Valle, *Syllabus para Modelado de Sistemas Fisiológicos*, Tecnológico Nacional de México / Instituto Tecnológico de Tijuana.

---

### Nota sobre los cálculos proporcionados

Los resultados numéricos de esta versión del README se incorporaron a partir del documento **Cálculos.pdf** proporcionado para la práctica. En particular, se conservaron el procedimiento algebraico, la expresión de la función de transferencia, el resultado de error estacionario y los polos calculados para los casos hipotenso, normotenso e hipertenso. fileciteturn3file0L1-L1

## Uso académico

Este repositorio documenta una práctica de **Modelado y control del sistema cardiovascular mediante el modelo Windkessel**. Los resultados deben distinguirse entre desarrollo matemático, simulaciones, resultados obtenidos mediante MATLAB/Python y análisis propio del estudiante.

Las estrategias de control incluidas tienen únicamente finalidad académica y de simulación.
