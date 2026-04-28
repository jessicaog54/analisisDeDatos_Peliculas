### Practica_3_Publicacion_Aplicaciones_Web
 
| Integrantes |
|---|
| Jessica Johanna Obando García |
| Mateo González Escudero |
| Lukas Jiménez Bueno |
| David Ramirez Velez |


# Industria del cine — Proyecto de Análisis de Datos y BI

## Descripción general

Este proyecto analiza información histórica de películas a partir del dataset inicial `movies_metadata.csv`. A partir de este archivo se realizó un proceso de limpieza, transformación y modelado para construir archivos CSV transformados, entre ellos `fact_peliculas.csv`, `dim_fecha.csv` y tablas puente como `bridge_pelicula_productora.csv`.

El enfoque del análisis no está centrado en categorías temáticas como miedo, terror, comedia o acción, sino principalmente en variables relacionadas con la industria cinematográfica desde la perspectiva de inversión, producción, recaudo y rentabilidad. Por esta razón, el dashboard y los KPIs se orientan a responder preguntas sobre presupuesto, ingresos, ganancias, producción por año, pertenencia a colecciones y disponibilidad de datos financieros.

---

# Fase 1: Comprensión del problema

## 1.1 Contexto del dataset

El dataset `movies_metadata.csv` contiene información descriptiva y financiera de películas, incluyendo variables como:

- Título de la película.
- Fecha de estreno.
- Presupuesto.
- Recaudo.
- Duración.
- Popularidad.
- Promedio de votos.
- Cantidad de votos.
- Idioma original.
- Estado de la película.
- Productoras.
- Países de producción.
- Pertenencia o no a una colección/saga.

Después del proceso ETL, el dataset fue organizado en un modelo tipo Data Warehouse, donde la tabla principal es `fact_peliculas`. Esta tabla concentra las métricas de negocio más importantes, como presupuesto, recaudo, ganancia, ROI, rentabilidad, categoría de presupuesto y pertenencia a colección.

## 1.2 Identificación del problema de análisis o negocio

La industria del cine requiere tomar decisiones de inversión con alto nivel de incertidumbre. Producir una película implica costos elevados y no siempre garantiza retorno económico. Por esta razón, el problema de análisis se enfoca en comprender cómo se comportan las películas desde el punto de vista financiero y productivo.

El problema central puede formularse así:

> ¿Qué patrones de inversión, producción y recaudo permiten entender la rentabilidad de las películas dentro del dataset analizado?

Desde una perspectiva de negocio, el análisis busca apoyar decisiones relacionadas con:

- Identificar si mayores presupuestos se asocian con mayores recaudos.
- Evaluar si pertenecer a una colección o saga mejora la probabilidad de rentabilidad.
- Comprender cómo ha evolucionado la producción de películas a través del tiempo.
- Analizar qué tan completa es la información financiera del dataset.
- Construir indicadores que permitan resumir el comportamiento general de la industria.

## 1.3 Preguntas clave de análisis

1. **¿Cómo ha evolucionado la cantidad de películas producidas por año y por década?**  
   Esta pregunta permite identificar tendencias de crecimiento o caída en la producción cinematográfica.

2. **¿Existe relación entre el presupuesto de una película y su recaudo?**  
   Esta pregunta busca determinar si invertir más dinero en producción se asocia con mayores ingresos.

3. **¿Las películas que pertenecen a una colección o saga tienen mayor probabilidad de ser rentables?**  
   Esta pregunta permite analizar si las franquicias o colecciones representan una ventaja económica.

4. **¿Qué categorías de presupuesto presentan mejores niveles de rentabilidad?**  
   Esta pregunta ayuda a comparar películas de bajo, medio, alto presupuesto y tipo blockbuster.

5. **¿Qué porcentaje de películas cuenta con información financiera suficiente para analizar presupuesto y recaudo?**  
   Esta pregunta es importante porque muchos registros no tienen presupuesto o recaudo disponible, lo cual afecta la interpretación de los resultados.

---

# Fase 2: Formulación de hipótesis

Para la validación estadística se trabajó con un nivel de significancia de `α = 0.05`. Esto significa que si el valor p es menor a 0.05, se rechaza la hipótesis nula y se considera que existe evidencia estadística suficiente para apoyar la hipótesis alternativa.

---

## Hipótesis 1: Relación entre presupuesto y recaudo

### Planteamiento

Las películas con mayor presupuesto tienden a tener mayor recaudo, ya que cuentan con más recursos para producción, efectos, talento, distribución y mercadeo.

### Variables relacionadas

- `budget`: presupuesto de la película.
- `revenue`: recaudo de la película.
- `profit`: ganancia calculada como `revenue - budget`.
- `roi`: retorno sobre la inversión.

### Hipótesis estadística

- **H0:** No existe relación estadísticamente significativa entre el presupuesto y el recaudo de las películas.
- **H1:** Sí existe relación estadísticamente significativa entre el presupuesto y el recaudo de las películas.

### Prueba estadística aplicada

Se utilizó la prueba de correlación de Spearman, ya que las variables financieras no siguen necesariamente una distribución normal y pueden contener valores extremos.

La prueba se aplicó sobre películas con presupuesto y recaudo mayores que cero.

### Resultado

- Muestra analizada: 5.171 películas con presupuesto y recaudo disponibles.
- Correlación de Spearman entre presupuesto y recaudo: `ρ = 0.704`.
- Valor p: `< 0.001`.

### Decisión

Como el valor p es menor que 0.05, se rechaza H0.

### Interpretación

Existe evidencia estadística de una relación positiva fuerte entre presupuesto y recaudo. En términos de negocio, esto indica que las películas con mayores inversiones tienden a generar mayores ingresos. Sin embargo, esto no significa que siempre sean más rentables, porque una película puede recaudar mucho, pero también tener costos muy altos.

---

## Hipótesis 2: Relación entre pertenecer a colección y rentabilidad

### Planteamiento

Las películas que pertenecen a una colección, saga o franquicia podrían tener ventaja comercial porque ya cuentan con reconocimiento de marca, audiencia previa y mayor expectativa del público.

### Variables relacionadas

- `pertenece_a_coleccion`: indica si la película pertenece o no a una colección.
- `es_rentable`: indica si la película generó ganancia positiva.
- `profit`: ganancia de la película.

### Hipótesis estadística

- **H0:** La rentabilidad de una película es independiente de si pertenece o no a una colección.
- **H1:** La rentabilidad de una película está asociada con pertenecer o no a una colección.

### Prueba estadística aplicada

Se utilizó una prueba Chi-cuadrado de independencia, ya que ambas variables son categóricas.

### Resultado

- Películas que pertenecen a colección: 4.318.
- Películas que no pertenecen a colección: 39.095.
- Porcentaje rentable en películas de colección: `24.90%`.
- Porcentaje rentable en películas que no pertenecen a colección: `6.53%`.
- Chi-cuadrado: `χ² = 1709.25`.
- Valor p: `< 0.001`.
- Odds ratio aproximado: `4.74`.

### Decisión

Como el valor p es menor que 0.05, se rechaza H0.

### Interpretación

Existe evidencia estadística de que pertenecer a una colección está asociado con una mayor probabilidad de rentabilidad. En el dataset, las películas de colección presentan una proporción de rentabilidad notablemente superior frente a las películas independientes o no pertenecientes a sagas.

---

## Hipótesis 3: Relación entre categoría de presupuesto y rentabilidad

### Planteamiento

Las películas con mayor categoría de presupuesto pueden tener una mayor probabilidad de ser rentables, debido a que suelen contar con mejores recursos de producción, distribución y promoción.

### Variables relacionadas

- `categoria_presupuesto`: clasifica las películas como bajo, medio, alto o blockbuster.
- `es_rentable`: indica si la película fue rentable.
- `budget`, `revenue`, `profit`.

### Hipótesis estadística

- **H0:** La categoría de presupuesto y la rentabilidad son independientes.
- **H1:** La categoría de presupuesto y la rentabilidad están asociadas.

### Prueba estadística aplicada

Se utilizó una prueba Chi-cuadrado de independencia. Para esta prueba se excluyó la categoría `Sin dato`, ya que cuando no existe presupuesto no es posible interpretar correctamente la rentabilidad financiera.

### Resultado

Porcentaje de películas rentables por categoría de presupuesto:

| Categoría de presupuesto | Películas | Películas rentables | % rentables |
|---|---:|---:|---:|
| Bajo (<5M) | 3.070 | 810 | 26.38% |
| Medio (5-30M) | 3.351 | 1.454 | 43.39% |
| Alto (30-100M) | 1.599 | 1.036 | 64.79% |
| Blockbuster (>100M) | 372 | 329 | 88.44% |

Resultado estadístico:

- Chi-cuadrado: `χ² = 967.65`.
- Valor p: `< 0.001`.

### Decisión

Como el valor p es menor que 0.05, se rechaza H0.

### Interpretación

Existe evidencia estadística de asociación entre la categoría de presupuesto y la rentabilidad. En el dataset, a medida que aumenta la categoría de presupuesto, también aumenta la proporción de películas rentables. Sin embargo, esta conclusión debe analizarse con cuidado, porque los grandes presupuestos suelen estar acompañados de estrategias de distribución más amplias y mayor exposición comercial.

---

# Fase 3: Preparación y modelado de datos

Aunque el foco de este documento está en las fases 1, 2, 4 y 6, se incluye un resumen de la Fase 3 porque es la base del análisis y del dashboard.

## 3.1 Archivo inicial

El archivo inicial utilizado fue:

```text
movies_metadata.csv
```

Este archivo contenía la información original de las películas. A partir de este dataset se realizó el proceso de extracción, limpieza, transformación y carga.

## 3.2 Limpieza aplicada

Durante la preparación de datos se realizaron las siguientes acciones:

- Eliminación de registros duplicados.
- Eliminación de registros con identificadores no numéricos.
- Eliminación o corrección de fechas inválidas.
- Conversión de variables numéricas como presupuesto, recaudo, duración, popularidad y votación.
- Normalización de presupuestos y recaudos menores a 1.000 como valores no válidos.
- Clasificación de estados inválidos como `Unknown`.
- Creación de banderas para identificar si una película tiene presupuesto, tiene recaudo, es rentable y pertenece a una colección.

## 3.3 Métricas derivadas

Se crearon las siguientes métricas para el análisis:

| Métrica | Fórmula / descripción |
|---|---|
| `profit` | `revenue - budget` |
| `roi` | `(profit / budget) * 100` |
| `es_rentable` | 1 si la ganancia es positiva y existe presupuesto |
| `tiene_presupuesto` | 1 si el presupuesto es mayor que cero |
| `tiene_recaudacion` | 1 si el recaudo es mayor que cero |
| `pertenece_a_coleccion` | 1 si la película pertenece a una colección |
| `categoria_presupuesto` | Sin dato, Bajo, Medio, Alto o Blockbuster |
| `decada` | Agrupación del año de estreno por década |

## 3.4 Modelo estrella

El modelo resultante se estructuró como un Data Warehouse tipo estrella:

- Tabla de hechos:
  - `fact_peliculas`

- Dimensiones:
  - `dim_fecha`
  - `dim_idioma`
  - `dim_estado`
  - `dim_genero`
  - `dim_pais_produccion`
  - `dim_productora`

- Tablas puente:
  - `bridge_pelicula_genero`
  - `bridge_pelicula_pais`
  - `bridge_pelicula_productora`

Este modelo permite conectar las métricas financieras y de producción con dimensiones de tiempo, idioma, estado, país, género y productora.

---

# Fase 4: Definición de KPIs

Los KPIs se definieron con base en el enfoque de negocio del proyecto: inversión, producción, recaudo y rentabilidad.

## KPI 1: Ingresos totales

### Fórmula

```text
Ingresos totales = SUM(revenue)
```

### Resultado

```text
498.800.868.299
```

Aproximadamente `498,8 mil millones`.

### Justificación de negocio

Permite medir el volumen total de recaudo generado por las películas del dataset. Es un indicador clave para entender el tamaño económico de la muestra analizada.

### Relación con hipótesis

Se relaciona con la Hipótesis 1, porque permite analizar el comportamiento del recaudo frente al presupuesto.

### Interpretación

El dataset muestra un volumen de ingresos acumulados alto, pero concentrado principalmente en películas que sí cuentan con datos de recaudo. Por eso debe interpretarse junto con el porcentaje de películas con información financiera disponible.

---

## KPI 2: Presupuesto total

### Fórmula

```text
Presupuesto total = SUM(budget)
```

### Resultado

```text
187.457.668.200
```

Aproximadamente `187,46 mil millones`.

### Justificación de negocio

Mide el nivel de inversión registrada en las películas del dataset.

### Relación con hipótesis

Se relaciona con la Hipótesis 1 y la Hipótesis 3, ya que permite estudiar si mayores niveles de inversión se asocian con mayor recaudo o mayor rentabilidad.

### Interpretación

El presupuesto total permite dimensionar el esfuerzo económico de producción. Sin embargo, muchas películas no tienen presupuesto registrado, por lo que este KPI representa únicamente la inversión conocida en el dataset.

---

## KPI 3: Ganancia total

### Fórmula

```text
Ganancia total = SUM(revenue) - SUM(budget)
```

### Resultado

```text
311.343.200.099
```

Aproximadamente `311,34 mil millones`.

### Justificación de negocio

Permite evaluar el resultado financiero agregado del conjunto de películas.

### Relación con hipótesis

Se relaciona con todas las hipótesis, especialmente con el análisis de rentabilidad por presupuesto y colección.

### Interpretación

El resultado agregado es positivo. Esto indica que, en conjunto, las películas con información financiera generan más ingresos que costos. Aun así, este resultado puede estar influenciado por películas de alto recaudo y por registros sin información completa.

---

## KPI 4: ROI global

### Fórmula

```text
ROI global = (Ganancia total / Presupuesto total) * 100
```

### Resultado

```text
166,09%
```

### Justificación de negocio

El ROI permite medir qué tanto retorno se obtiene por cada unidad monetaria invertida.

### Relación con hipótesis

Se relaciona con la Hipótesis 1 y la Hipótesis 3.

### Interpretación

Un ROI global positivo indica que, de forma agregada, los ingresos superan ampliamente el presupuesto registrado. Sin embargo, el ROI individual de cada película puede variar mucho, por lo que se recomienda analizarlo por categorías de presupuesto y no solo de forma global.

---

## KPI 5: Cantidad total de películas

### Fórmula

```text
Cantidad de películas = COUNT(pelicula_id)
```

### Resultado

```text
43.413 películas
```

### Justificación de negocio

Permite conocer el tamaño de la base limpia usada en el análisis y en el dashboard.

### Relación con hipótesis

Se relaciona con el análisis temporal y de producción, especialmente con la evolución de películas por año.

### Interpretación

La base limpia contiene un volumen amplio de películas, suficiente para analizar tendencias generales de producción. Sin embargo, no todas las películas tienen información completa de presupuesto o recaudo.

---

## KPI 6: Porcentaje de películas rentables

### Fórmula

```text
% películas rentables = SUM(es_rentable) / COUNT(pelicula_id) * 100
```

### Resultado

```text
8,36% sobre el total de películas
43,24% sobre películas con presupuesto registrado
```

### Justificación de negocio

Permite identificar qué proporción de películas logra recuperar su inversión y generar ganancia.

### Relación con hipótesis

Se relaciona con la Hipótesis 2 y la Hipótesis 3.

### Interpretación

Sobre el total de películas, el porcentaje rentable es bajo porque una gran parte del dataset no tiene presupuesto registrado. Cuando se analiza únicamente el grupo con presupuesto disponible, la proporción de películas rentables aumenta considerablemente.

---

## KPI 7: Porcentaje de películas con presupuesto y recaudo

### Fórmula

```text
% con presupuesto = SUM(tiene_presupuesto) / COUNT(pelicula_id) * 100
% con recaudo = SUM(tiene_recaudacion) / COUNT(pelicula_id) * 100
```

### Resultado

```text
Películas con presupuesto: 19,33%
Películas con recaudo: 16,20%
```

### Justificación de negocio

Este KPI evalúa la calidad y completitud de los datos financieros.

### Relación con hipótesis

Se relaciona con todas las hipótesis, porque la falta de datos financieros puede limitar la validez del análisis.

### Interpretación

La mayoría de películas no tiene información de presupuesto o recaudo. Por esta razón, los análisis financieros deben interpretarse como conclusiones sobre la muestra con datos disponibles, no necesariamente sobre toda la industria cinematográfica.

---

## KPI 8: Porcentaje de películas que pertenecen a colección

### Fórmula

```text
% en colección = SUM(pertenece_a_coleccion) / COUNT(pelicula_id) * 100
```

### Resultado

```text
9,95%
```

### Justificación de negocio

Permite identificar qué proporción del catálogo corresponde a películas asociadas a sagas, franquicias o colecciones.

### Relación con hipótesis

Se relaciona directamente con la Hipótesis 2.

### Interpretación

Aunque las películas de colección son una minoría, muestran una mayor proporción de rentabilidad frente a las películas que no pertenecen a colección.

---

# Fase 6: Análisis, validación y storytelling

## 6.1 Interpretación general de resultados

El dashboard de la industria del cine muestra que el dataset contiene un volumen amplio de películas, con más de 43 mil registros limpios. A nivel financiero, los ingresos acumulados superan el presupuesto total registrado, generando una ganancia global positiva.

La visualización de producción por año muestra un crecimiento importante en la cantidad de películas registradas, especialmente desde finales del siglo XX y durante las décadas de 2000 y 2010. Esto puede interpretarse como una mayor disponibilidad de información cinematográfica reciente y un crecimiento en la producción registrada dentro del dataset.

Sin embargo, uno de los hallazgos más importantes es que existe una alta cantidad de películas sin presupuesto y sin recaudo registrado. Esto significa que el análisis financiero no debe interpretarse sobre todo el universo de películas, sino principalmente sobre aquellas que tienen información económica disponible.

---

## 6.2 Validación de hipótesis mediante pruebas estadísticas

### Validación de la Hipótesis 1

La prueba de Spearman mostró una correlación positiva fuerte entre presupuesto y recaudo:

```text
ρ = 0.704
p < 0.001
```

Por lo tanto, se rechaza H0 y se concluye que existe relación significativa entre presupuesto y recaudo.

Desde el punto de vista de negocio, esto indica que una mayor inversión suele estar asociada con mayor capacidad de recaudo. No obstante, el recaudo no debe confundirse con rentabilidad, porque la ganancia depende también del costo de producción.

---

### Validación de la Hipótesis 2

La prueba Chi-cuadrado mostró asociación significativa entre pertenecer a una colección y ser rentable:

```text
χ² = 1709.25
p < 0.001
```

Además, las películas de colección presentaron una rentabilidad del `24,90%`, mientras que las películas no pertenecientes a colección presentaron una rentabilidad del `6,53%`.

Por lo tanto, se rechaza H0 y se concluye que pertenecer a una colección está asociado con una mayor probabilidad de rentabilidad.

---

### Validación de la Hipótesis 3

La prueba Chi-cuadrado mostró asociación significativa entre categoría de presupuesto y rentabilidad:

```text
χ² = 967.65
p < 0.001
```

La proporción de películas rentables aumenta según la categoría de presupuesto:

- Bajo: 26,38%.
- Medio: 43,39%.
- Alto: 64,79%.
- Blockbuster: 88,44%.

Por lo tanto, se rechaza H0 y se concluye que la categoría de presupuesto está asociada con la rentabilidad.

---

## 6.3 Uso del valor p para la toma de decisiones

En las tres hipótesis evaluadas, el valor p fue menor que 0.05. Esto significa que los resultados observados tienen baja probabilidad de explicarse únicamente por azar.

En términos prácticos:

- El presupuesto sí se relaciona con el recaudo.
- Pertenecer a una colección sí se asocia con mayor rentabilidad.
- La categoría de presupuesto sí se relaciona con la probabilidad de ser rentable.

Estas conclusiones apoyan el uso de los KPIs financieros y de producción para tomar decisiones basadas en evidencia.

---

## 6.4 Storytelling con los datos

La historia que cuentan los datos es la siguiente:

> La industria cinematográfica analizada muestra un crecimiento importante en la producción de películas a lo largo del tiempo. Aunque el dataset contiene más de 43 mil películas, no todas tienen información financiera completa. Por eso, al analizar inversión y recaudo, es necesario concentrarse en las películas con presupuesto y recaudo registrados.

> Los resultados muestran que las películas con mayor presupuesto tienden a generar mayores ingresos. Además, las películas que hacen parte de colecciones o sagas presentan una ventaja clara en términos de rentabilidad. Esto sugiere que el reconocimiento de marca y la continuidad de una franquicia pueden influir positivamente en los resultados económicos.

> El análisis por categorías de presupuesto también muestra que las películas tipo blockbuster tienen mayor proporción de rentabilidad, aunque requieren inversiones mucho más altas. Por lo tanto, el presupuesto puede ser una palanca importante para aumentar el recaudo, pero debe analizarse junto con el riesgo, el ROI y la disponibilidad real de datos.

---

## 6.5 Propuestas de decisiones basadas en evidencia

1. **Priorizar análisis financieros sobre películas con datos completos.**  
   Para tomar decisiones de inversión, se recomienda filtrar películas con presupuesto y recaudo disponibles.

2. **Evaluar con mayor detalle las películas de colección o franquicia.**  
   Los datos muestran que pertenecer a una colección está asociado con mayor rentabilidad. Esto puede apoyar decisiones sobre secuelas, sagas o explotación de marcas existentes.

3. **Usar categorías de presupuesto para segmentar estrategias.**  
   Las películas de bajo, medio, alto presupuesto y blockbuster no se comportan igual. Cada grupo debe analizarse con expectativas financieras diferentes.

4. **No tomar decisiones únicamente con el recaudo.**  
   Una película puede tener altos ingresos, pero si su presupuesto también es muy alto, la rentabilidad puede no ser tan favorable. Por eso se deben analizar juntos presupuesto, ganancia y ROI.

5. **Mejorar la calidad de los datos financieros.**  
   El porcentaje de películas con presupuesto y recaudo disponible es bajo. Para análisis futuros se recomienda enriquecer la base con fuentes adicionales o validar datos faltantes.

6. **Revisar el KPI de rating en el dashboard.**  
   Si el objetivo es mostrar `rating promedio`, se recomienda usar una medida de promedio real, como `AVERAGE(vote_average)`, y no una suma acumulada. El promedio simple del dataset limpio es cercano a `5,62`, mientras que el promedio ponderado por cantidad de votos es cercano a `6,69`.

---

## 6.6 Limitaciones del análisis

1. **Datos financieros incompletos.**  
   Muchas películas no tienen presupuesto o recaudo registrado, lo cual limita el alcance de las conclusiones financieras.

2. **Valores en cero pueden representar datos faltantes.**  
   En el dataset, un presupuesto o recaudo igual a cero no necesariamente significa que la película no tuvo inversión o ingresos; puede significar que el dato no estaba disponible.

3. **No se ajustó por inflación.**  
   Comparar presupuestos y recaudos de películas de diferentes décadas puede ser impreciso si no se ajustan los valores monetarios.

4. **El dataset no incluye todos los costos reales.**  
   Variables como mercadeo, distribución, impuestos o acuerdos comerciales no están presentes, pero pueden afectar la rentabilidad real.

5. **La información reciente puede estar incompleta.**  
   Los años más cercanos al final del dataset pueden mostrar caídas no necesariamente por menor producción, sino por falta de actualización de datos.

6. **El rating puede estar sesgado.**  
   El promedio de votos puede depender de la cantidad de votantes. Por eso, para análisis más precisos, se recomienda usar rating ponderado por `vote_count`.

---

# Conclusiones

El proyecto permitió analizar la industria del cine desde una perspectiva de producción, inversión y rentabilidad. A partir del dataset inicial `movies_metadata.csv`, se construyó un modelo transformado que facilitó la creación de KPIs y visualizaciones en el dashboard.

Los principales hallazgos son:

- El dataset limpio contiene 43.413 películas.
- Los ingresos totales superan el presupuesto total registrado.
- Existe una relación significativa entre presupuesto y recaudo.
- Las películas que pertenecen a colecciones tienen mayor probabilidad de ser rentables.
- Las categorías de mayor presupuesto presentan mayores proporciones de rentabilidad.
- La calidad de los datos financieros es una limitación importante, ya que muchas películas no tienen presupuesto o recaudo registrado.

En conclusión, el análisis muestra que la inversión, la pertenencia a colecciones y la segmentación por presupuesto son variables importantes para comprender la rentabilidad de las películas. Sin embargo, las decisiones deben tomarse considerando la disponibilidad y calidad de los datos.

---
