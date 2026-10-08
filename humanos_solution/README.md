# HumanOS Intelligence Engine — solución didáctica

Solución para el take-home challenge: obligatorias A–D, pregunta interpretativa y **opcional A (Predictive modelling)**. Datos totalmente sintéticos. Revisar, comprender y adaptar antes de entregar.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest -q
uvicorn humanos.api:app --reload
```

Abrir http://127.0.0.1:8000/docs para probar GET `/signals`, `/moments`, `/cohorts` y `/cohorts/{dimension}/{value}`. Ejecutar el reto predictivo con `python -m humanos.predictive`. Los resultados se guardan en `outputs/`.

En Colab: subir o descomprimir la carpeta en Drive; añadir `src` a `sys.path` y cargar los CSV desde Drive. El notebook incluido proporciona las celdas correspondientes. **Colab no es necesario para servir la API**; para probarla de forma sencilla, usar el terminal local.

## Arquitectura y decisiones (resumen)

**A. Procesamiento.** `core.validate` comprueba columnas, valores nulos, duplicados, tipo de pesos, flags y Likert enteros 1–5. `calculate_signals` usa `item_config.csv` dinámicamente, invierte los ítems configurados (`6-x`), convierte Likert a 0–100 (`25*(x-1)`) y calcula medias ponderadas por señal. No se codifican reglas individuales por ítem. El resultado es determinista. Los pesos son configurables y no tienen por qué sumar 1.

**B. Moments.** Se proponen cuatro *afinidades exploratorias*, no diagnósticos ni etiquetas exclusivas. `Learning / Exploration = 0.60 Appetite + 0.40 Capacity`; `Mastery / Contribution = 0.55 Knowledge Exchange + 0.45 Agency`; `Consolidation / Stability = 0.50 Visibility + 0.30 Agency + 0.20 Capacity`; `Transition / Reinvention = 0.45 Appetite + 0.35 Capacity + 0.20*(100-Visibility)`. Los pesos son **hipótesis de diseño** y requieren validación. Las preguntas no miden directamente preferencia por estabilidad ni intención de transición: estas dos afinidades son proxies débiles y **no deben presentarse como momentos observados**. Un score alto en más de una afinidad es posible; la edad nunca determina un momento.

**C. Cohortes.** Se agregan señales por `age_group`, `role`, `work_mode`. Se calculan `n`, `score`, `organization_score`, `delta = score - organization_score` y `reportable = (n >= 10)`. Cuando `n < 10`, `score` y `delta` se devuelven como `null` para impedir interpretaciones accidentales. La edad, rol y modalidad son lentes descriptivas, no explicaciones causales.

**D. API.** FastAPI ofrece los cuatro endpoints pedidos; usa `lru_cache` para evitar recálculos en cada petición. Para datos mutables, eliminar caché o establecer una política de invalidación. Se devuelven HTTP 400 para dimensiones no válidas y 404 para cohortes inexistentes. Sin autenticación ni despliegue, por alcance del ejercicio.

**Opcional A.** Target `future_visibility_w2` (regresión). Las features son las seis puntuaciones W1 y tres cohortes. `participant_id` no se usa. `future_visibility_change` no se usa como feature porque contiene el target. División aleatoria 80/20 con semilla 42; 5-fold CV **solo en entrenamiento**; `ColumnTransformer` dentro del `Pipeline` para impedir leakage. Baseline media vs Ridge, Random Forest y Gradient Boosting. Métricas MAE, RMSE y R². Ridge se preselecciona por simplicidad y regularización; el test se reserva para evaluación. El cambio estimado se obtiene como `predicted_w2 - future_visibility_w1`. La etiqueta `estimated_decline` es solo el signo del cambio estimado; no equivale a una clasificación validada de caídas significativas. Los modelos predicen una media condicional, no la probabilidad individual de caída. Permutation importance se calcula en test como análisis exploratorio y **no demuestra causalidad**.

**Trade-offs y limitaciones.** La muestra predictiva tiene 360 observaciones, es sintética, solo tiene dos waves y contiene subgrupos pequeños. Un split aleatorio supone que los participantes son independientes; en datos reales sería necesario considerar estructura por organización y validación temporal. Los scores de momentos no están validados psicométricamente. En cohortes pequeñas, no sacar conclusiones. Para producción: schemas estrictos, persistencia, versionado de configuración, monitorización, controles de privacidad, tests de integración y validación externa. El modelo de ML no debería utilizarse para decisiones individuales sobre empleados sin auditoría y garantías adicionales.

## Pregunta de interpretación (apartado 9)

El ejemplo del enunciado indica que la cohorte **50–59** tiene 82 en Mastery / Contribution y 81 en Learning / Exploration, mientras **29–35** tiene 63 y 76 respectivamente. Podemos concluir que **en el ejemplo**, la cohorte 50–59 presenta puntuaciones agregadas superiores en ambas afinidades (19 y 5 puntos). También que Mastery y Exploration pueden coexistir. **No** podemos afirmar que la edad cause esos resultados, que todas las personas de un grupo sean iguales, que los mayores sean siempre expertos o que el grupo 29–35 tenga menos capacidad; tampoco podemos inferir significación estadística ni representatividad sin conocer tamaño, dispersión y calidad de medición de las cohortes. Si n<10, no se interpreta.

## Uso de herramientas de IA

Se utilizó ChatGPT para proponer arquitectura, generar un primer borrador de código, tests, notebook y explicaciones. **Antes de entregar, el candidato debe documentar qué revisó, ejecutó, corrigió y modificó personalmente**, y asegurarse de poder explicar las decisiones y resultados. No declarar revisiones o modificaciones no realizadas.
