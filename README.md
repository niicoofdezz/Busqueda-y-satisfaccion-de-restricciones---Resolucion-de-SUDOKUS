<div align="center">

<br/>

```
███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
```

### _Resolución automática de Sudokus con Backtracking, AC3 y Forward Checking_

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![CSP](https://img.shields.io/badge/Técnica-CSP-8A2BE2?style=for-the-badge)](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)
[![IA](https://img.shields.io/badge/Campo-Inteligencia_Artificial-00CED1?style=for-the-badge)]()

<br/>

> **Proyecto Académico** · Sistemas Inteligentes · Ingeniería Robótica · 2024

</div>

---

## 🧩 ¿Qué es este proyecto?

Un resolvedor automático de Sudokus que implementa y compara **tres algoritmos de inteligencia artificial** distintos, con interfaz gráfica interactiva. El usuario carga un tablero, elige el algoritmo y observa la solución junto con métricas de rendimiento.

El proyecto no solo resuelve Sudokus — analiza y compara la eficiencia de cada enfoque, midiendo **tiempo de ejecución** y **número de saltos hacia atrás** en 8 tableros de prueba distintos.

---

## 🗂️ Estructura

```
Sudoku-CSP/
├── main.py              # Interfaz gráfica (Tkinter) y punto de entrada
├── solver.py            # Implementación de los 3 algoritmos
├── tablero.py           # Clase Tablero: lógica de restricciones
└── sudokus/
    ├── sudoku1.txt      # 8 tableros de prueba con dificultad variada
    └── ...sudoku8.txt
```

---

## 🧠 Los Tres Algoritmos

### 🔁 Backtracking

Exploración recursiva del árbol de soluciones: prueba un valor, avanza, y si llega a un conflicto **retrocede** y prueba el siguiente.

**Mejora implementada:** en lugar de probar los 9 dígitos a ciegas, se calculan los **dominios** de cada casilla (valores posibles según las restricciones actuales), reduciendo drásticamente el espacio de búsqueda.

```python
# Caso base: tablero completo
if tablero.esTableroCompleto():
    return True

# Prueba valores del dominio de la casilla vacía
for valor in self.matriz_variables[fila][col].dominio:
    if not infringe_restricciones(fila, col, valor):
        tablero.setCasilla(fila, col, valor)
        if self.backtracking(tablero, siguiente_fila, siguiente_col):
            return True
        tablero.setCasilla(fila, col, 0)  # Backjump
```

---

### 🔗 AC3 — Consistencia de Arco

Antes de buscar, AC3 **reduce los dominios** de todas las casillas eliminando valores inconsistentes entre celdas relacionadas (misma fila, columna o mini-tablero).

Cada par de casillas con restricción entre ellas forma una **arista**. El algoritmo procesa la cola de aristas hasta que todos los dominios son consistentes entre sí — dejando al Backtracking un espacio de búsqueda muchísimo menor.

```
81 casillas × 20 restricciones = 1.620 aristas totales procesadas
```

**Reto resuelto:** al combinar AC3 con Backtracking, los dominios modificados por AC3 se sobreescribían. Se introdujo una variable booleana `calcularDominios` para evitar recalcularlos si ya habían sido procesados por el otro algoritmo.

---

### ⚡ Forward Checking

En cada asignación, **comprueba hacia delante**: elimina temporalmente de los dominios vecinos el valor recién asignado. Si algún dominio queda vacío, retrocede sin necesidad de explorar esa rama.

Incluye una función `restaurar()` que recupera los valores podados cuando se deshace una asignación, garantizando que los dominios vuelven al estado correcto.

**Reto resuelto:** la función `restaurar()` recorría el tablero entero, lo que era incorrecto — Forward Checking solo debe mirar hacia delante. Se añadieron filtros para recorrer únicamente desde la casilla actual en adelante.

---

## 📊 Comparativa de Rendimiento

Los 3 algoritmos se evaluaron sobre **8 Sudokus** distintos midiendo tiempo de ejecución y saltos dados:

| Algoritmo | Velocidad | Saltos | Observaciones |
|-----------|:---------:|:------:|---------------|
| Backtracking | 🐢 Lento | Muchos | Explora más ramas del árbol |
| AC3 + Backtracking | ⚡ Rápido | Pocos | AC3 reduce dominios antes de buscar |
| Forward Checking | ⚡⚡ Más rápido | Mínimos | Detecta conflictos con anticipación |

> Forward Checking fue el más rápido en todos los tableros. La combinación AC3 + Backtracking redujo considerablemente los saltos respecto a Backtracking puro.

---

## 🖥️ Interfaz Gráfica

Desarrollada con **Tkinter**, permite:

- **Cargar** cualquier Sudoku desde archivo `.txt`
- **Limpiar** el tablero
- **Ejecutar** cualquiera de los 3 algoritmos con un clic
- Ver el **estado de la solución** (correcta / incorrecta / incompleta)
- Ver el **tiempo de ejecución** en consola

---

## 🚀 Cómo ejecutarlo

```bash
# Instalar dependencias (Tkinter viene incluido con Python)
# No requiere instalación adicional

# Ejecutar
python main.py
```

1. Pulsa **"Cargar SuDoKu"** y selecciona uno de los archivos de `sudokus/`
2. Elige el algoritmo: **Back Tracking**, **AC3** o **Forward Checking**
3. Observa la solución en el tablero y el tiempo en consola

**Formato de los archivos `.txt`:**
```
3 1 2 4 0 0 0 0 8
7 4 0 0 9 3 6 0 0
...
```
`0` representa una casilla vacía.

---

## 📚 Contexto Académico

**Asignatura:** Sistemas Inteligentes — Búsqueda y Satisfacción de Restricciones  
**Autor:** Nicolás Fernández Blánquez  
**Fecha:** Marzo 2024

---

<div align="center">

**Stack:** Python 3.8 · Tkinter · CSP · Backtracking · AC3 · Forward Checking

_Tres algoritmos, un mismo tablero, resultados muy distintos._

</div>
