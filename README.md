# 🚘 Escape en Coordenadas

Programa en Python que genera un tablero tipo grilla de ciudad y busca la ruta más corta entre dos puntos usando el algoritmo **A\* (A-Star)**, teniendo en cuenta obstáculos y zonas de mayor costo.

## 📋 Descripción

El programa arma un tablero de calles (una cuadrícula donde hay caminos cada 3 filas y columnas, simulando manzanas de edificios) y le permite al usuario:

1. Agregar **zonas bloqueadas** manualmente en las coordenadas que elija.
2. Ver cómo se agrega **agua** de forma aleatoria en un 15% de los caminos disponibles (representa zonas más costosas de atravesar).
3. Ingresar una coordenada de **inicio** y una de **fin**.
4. Calcular la ruta más corta entre ambos puntos con A*, considerando que:
   - Los caminos normales cuestan `1`.
   - El agua cuesta `5` (es transitable, pero se evita si hay una alternativa más corta).
   - Los edificios y zonas bloqueadas son intransitables (costo infinito).
5. La búsqueda se ejecuta dos veces seguidas, para poder agregar una nueva zona bloqueada después de encontrar el primer camino y ver cómo se recalcula la ruta.

### Simbología

| Símbolo | Significado |
|---------|-------------|
| 🚘 | Punto de inicio |
| ❎ | Punto final |
| ⬜ | Camino libre |
| 🏠 | Edificio (obstáculo fijo) |
| 💧 | Agua (transitable, mayor costo) |
| 🚧 | Zona bloqueada (agregada por el usuario) |
| 🔸 | Camino encontrado por A* |

## ⚙️ Requisitos

- Python 3
- No requiere librerías externas (usa solo `random` y `heapq`, incluidas en la instalación estándar de Python)

## 🚀 Cómo ejecutar

```bash
python escapeencoords.py
```

Durante la ejecución, el programa va a pedir:

- Cantidad de filas y columnas del tablero.
- Si querés agregar zonas bloqueadas (respondiendo `si` o `no`, y luego la coordenada `fila,columna`).
- Coordenada de inicio y de fin (en formato `fila,columna`).

## 🧠 Detalles técnicos

- El tablero se representa como una matriz de enteros, donde cada valor corresponde a un tipo de celda (`CAMINO`, `EDIFICIO`, `AGUA`, `ZONAS_BLOQ`).
- La heurística usada en A* es la **distancia Manhattan** entre el nodo actual y el destino.
- El camino final se reconstruye siguiendo un diccionario de "padres" desde el nodo final hasta el de inicio, y luego se invierte para mostrarlo en el orden correcto.
- La validación de coordenadas se reutiliza tanto para el inicio y fin como para las zonas bloqueadas ingresadas por el usuario, evitando que se pisen con edificios o queden fuera del mapa.
