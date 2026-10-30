# Guía rápida

Este repositorio reproduce resultados numéricos del artículo Frontiers 1877314.
El README principal está en inglés para lectores y producción editorial.

## Ejecutar

Con Python 3.12:

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py --verify
```

Se regeneran las tablas descriptivas, Wilcoxon con ajuste de Holm, la Figura 13
y un registro de verificación. Los archivos públicos contienen identificadores
P01–P15 y salidas numéricas o agregadas; no se incluyen documentos personales,
nombres, correos, respuestas libres ni enlaces privados de Drive.

La comprobación de las distancias originales permitió corregir la etiqueta de
la Tabla 6 y ajustar Holm con precisión completa. Véase `docs/proof_corrections.md`.
La conclusión de significancia no cambia.

El repositorio todavía no contiene el video, el listado completo de las 105
noticias ni el cuestionario anonimizado completo. Esos archivos deben añadirse
antes de afirmar que todos los suplementos anunciados están disponibles aquí.

Un DOI de Zenodo permitiría citar una versión archivada e identificable del
repositorio. Es adicional al DOI del artículo y no es necesario para crear GitHub.
