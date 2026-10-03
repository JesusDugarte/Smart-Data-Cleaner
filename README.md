# Smart Data Cleaner

## Estado actual

**Versión: V2-09 --- Validada**

Smart Data Cleaner es una herramienta desarrollada en Python para
analizar, consolidar y controlar la calidad de múltiples archivos CSV.

El sistema determina si los archivos pueden consolidarse, analiza la
calidad cuando corresponde, aplica correcciones permitidas, valida el
resultado y genera un informe Excel.

## Objetivo

``` text
Archivos CSV
    ↓
Análisis estructural
    ↓
Diagnóstico
    ↓
Compatibilidad de tipos
    ↓
Decisión
    ├── LISTO
    ├── REVISAR
    └── BLOQUEADO
             ↓
       si corresponde
             ↓
      Análisis de calidad
             ↓
    Correcciones permitidas
             ↓
         Validación
             ↓
       Resultado final
             ↓
       Informe Excel
```

## Evolución

### V2-06 --- Decisión de consolidación

Determina si los archivos pueden consolidarse.

-   `LISTO`: no existen conflictos que impidan la consolidación.
-   `REVISAR`: existen diferencias compatibles que requieren atención.
-   `BLOQUEADO`: existe una incompatibilidad que impide continuar.

Reglas principales:

1.  Mismo tipo en todos los archivos → `LISTO`.
2.  Tipos diferentes pero valores analizables convertibles → `REVISAR`.
3.  Al menos un valor no convertible → `BLOQUEADO`.
4.  Sin datos analizables → `REVISAR`.
5.  Faltantes con datos analizables convertibles → `REVISAR`.
6.  Faltantes y valores no convertibles → `BLOQUEADO`.

`REVISAR` no impide la consolidación; `BLOQUEADO` sí.

### V2-07 --- Calidad de datos

Analiza:

-   faltantes;
-   duplicados;
-   espacios;
-   consistencia de texto.

Los espacios pueden corregirse automáticamente.

La capitalización puede corregirse cuando existe una forma dominante
suficiente.

Los duplicados no se eliminan automáticamente y quedan como pendientes.

### V2-08 --- Modelo y validación

El resultado se organiza en:

``` text
resultado_proceso
├── diagnostico
├── decision
├── ejecucion
├── validacion
└── resultado
    ├── estado_final
    ├── datos
    ├── resumen
    ├── correcciones
    └── pendientes
```

La columna `Archivo_Origen` conserva la procedencia de cada registro.

Se validan:

-   estructura;
-   cantidad de registros;
-   procedencia.

### V2-09 --- Informe Excel

Genera:

``` text
informe_proceso.xlsx
├── Resumen
├── Calidad
├── Correcciones
├── Pendientes
└── Datos_Limpios
```

No se utilizan gráficos en esta versión.

`Resumen` presenta el estado, ejecución y validaciones.

`Calidad` presenta faltantes, duplicados, espacios y consistencia de
texto.

`Correcciones` registra únicamente las correcciones realizadas.

`Pendientes` registra acciones que requieren revisión.

`Datos_Limpios` contiene el resultado final y conserva `Archivo_Origen`.

## Arquitectura

``` text
Smart Data Cleaner
│
├── detectores/
├── reglas/
├── limpieza/
├── validacion/
├── analisis/
├── modelo/
├── presentacion/
├── exportacion/
└── inicio_v2_06.py
```

La separación permite distinguir detección, reglas, transformación,
validación, análisis, modelo y presentación.

## Flujo

``` text
1. Entrada
2. Análisis estructural
3. Diagnóstico estructural
4. Construcción de estructura objetivo
5. Homogeneización
6. Validación estructural
7. Análisis de tipos
8. Compatibilidad
9. Determinación del estado
10. Consolidación
11. Calidad
12. Correcciones permitidas
13. Validación
14. Resultado
15. Exportación TXT
16. Exportación Excel
```

En `BLOQUEADO`, no se ejecutan las etapas que dependen de una
consolidación válida.

## Casos de prueba V2-09

### LISTO

Archivos:

``` text
archivo_X.csv
archivo_W.csv
```

Resultado:

``` text
ESTRUCTURA_EQUIVALENTE
LISTO
6 registros
```

Comprobado en consola y Excel.

### REVISAR

Archivos:

``` text
archivo_calidad_integral.csv
archivo_capitalizacion_corregible.csv
```

Resultado:

``` text
REVISAR
8 registros
```

Hallazgos:

-   1 faltante en `Precio`;
-   1 fila duplicada;
-   3 valores con espacios;
-   1 variación de capitalización.

Correcciones:

-   3 espacios;
-   1 capitalización.

Pendiente:

-   revisar filas duplicadas.

Comprobado en consola y Excel.

### BLOQUEADO

Archivos:

``` text
archivo_X.csv
archivo_Z.csv
```

Problema:

``` text
Precio
1 valor no convertible
```

Resultado:

``` text
BLOQUEADO
```

No se realiza consolidación, análisis de calidad ni validación de
consolidación.

Comprobado en consola y Excel.

## Estado de la versión

**V2-09 --- VALIDADA**

``` text
LISTO       ✓
REVISAR     ✓
BLOQUEADO   ✓
```

## Tecnologías

-   Python
-   pandas
-   openpyxl
-   CSV
-   Excel

## Instalación

Requisitos:

- Python 3.11 o superior.
- pandas.
- openpyxl.

Instalar las dependencias con:

```powershell
pip install pandas openpyxl
```

## Ejecución

Desde la carpeta raíz del proyecto ejecutar:

```powershell
python inicio_v2_06.py
```

La versión actual utiliza archivos CSV de prueba configurados
directamente en `inicio_v2_06.py`. Actualmente se utilizan:

```text
pruebas_v2_06/
├── archivo_X.csv
└── archivo_W.csv
```

Para procesar otros archivos en esta versión, es necesario modificar la
lista `archivos_csv` del archivo `inicio_v2_06.py`.

## Entrada de datos

Smart Data Cleaner recibe archivos CSV para analizarlos, determinar su
compatibilidad estructural y de tipos y, cuando corresponde,
consolidarlos.

En V2-09, la entrada está configurada de forma explícita en el archivo
principal. El descubrimiento automático de archivos en una carpeta no
forma parte de esta versión.

## Resultados

Después de una ejecución válida, los resultados se generan en la carpeta
`salida/`:

```text
salida/
├── datos_limpios.csv
├── informe_proceso.txt
└── informe_proceso.xlsx
```

- `datos_limpios.csv`: contiene los datos finales procesados.
- `informe_proceso.txt`: contiene un resumen textual del proceso.
- `informe_proceso.xlsx`: contiene el informe estructurado en Excel.

La carpeta `salida/` contiene resultados generados localmente y está
excluida del control de versiones mediante `.gitignore`.

## Principios de diseño

-   No modificar datos sin una regla definida.
-   No eliminar información automáticamente.
-   Separar diagnóstico de decisión.
-   Separar lógica de presentación.
-   Validar el resultado producido.
-   Diferenciar "sin problemas" de "no analizado".

## Próximos pasos

V2-09 se considera una versión estable.

Las futuras versiones podrán ampliar las reglas de calidad, soportar
configuraciones adicionales, incorporar pruebas automatizadas, mejorar
el procesamiento de múltiples archivos o añadir una interfaz de usuario.

Estas funcionalidades no forman parte de V2-09.
