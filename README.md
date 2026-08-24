# Algoritmos de Búsqueda y Heurísticas en Redes Viales - Heurística y Optimización

Práctica 2 de la asignatura **Heurística y Optimización (UC3M)**.

---

## 📌 Descripción del Proyecto

Estudio, implementación y comparación empírica de diferentes algoritmos de búsqueda de caminos óptimos sobre redes de transporte y grafos a gran escala (dataset de la red de carreteras de New York City).

### Algoritmos Implementados:
* **Algoritmo A*:** Búsqueda informada utilizando heurísticas admisibles (distancia Euclídea y distancia Manhattan).
* **Algoritmo de Dial:** Búsqueda basada en colas por distancia (cubos de Dial con coste unitario/entero) logrando complejidad O(1) por inserción/extracción en distancias cortas.
* **Dial Lineal:** Optimización con listas abiertas circulares.
* **Búsqueda con Colas de Prioridad (Min-Heap):** Implementación estándar para comparación de tiempos de ejecución y consumo de memoria.

---

## 🛠️ Tecnologías

* **Lenguaje:** Python 3.
* **Estructuras de Datos:** Grafos, Tablas Hash, Min-Heaps y Listas Enlazadas.

---

## 🚀 Ejecución

```bash
# Ejecutar los algoritmos y pruebas comparativas
python main.py
```
