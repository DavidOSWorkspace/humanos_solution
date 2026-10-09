# Práctica Silverce
Solución al problema propuesto por Silverce.

## 1. Introducción

Para realizar este proyecto he intentado aprovechar los conocimientos y la experiencia que he adquirido en asignaturas y proyectos anteriores, especialmente en programación con Python, análisis de datos, Machine Learning y desarrollo de APIs.

Mi objetivo ha sido desarrollar una solución que cumpla con los requisitos del reto de HumanOS, pero intentando entender cómo funciona cada parte y reutilizando herramientas y metodologías con las que ya había trabajado anteriormente.

También he utilizado ChatGPT como herramienta de apoyo durante el desarrollo, principalmente para adaptar código de proyectos anteriores, resolver errores y organizar algunas partes de la implementación.

## 2. Arquitectura y organización del proyecto

He decidido organizar el proyecto en diferentes módulos para separar las responsabilidades de cada parte y facilitar tanto su comprensión como su mantenimiento.

La solución está dividida en varias funcionalidades:

- **Procesamiento de datos:** lectura de los archivos CSV, validación de los datos y transformación de las respuestas.
- **Cálculo de señales:** obtención de las seis señales de HumanOS mediante las respuestas y los pesos definidos en la configuración.
- **Career & Life Moments:** cálculo de las puntuaciones asociadas a los diferentes momentos profesionales.
- **Análisis de cohortes:** agrupación de resultados por edad, rol y modalidad de trabajo, respetando las restricciones de privacidad.
- **API:** exposición de los resultados mediante endpoints para que puedan consultarse desde otras aplicaciones.
- **Machine Learning:** desarrollo de modelos predictivos para estimar Future Visibility en Wave 2.

He intentado mantener una estructura modular porque es una forma de trabajar que ya había utilizado en otros proyectos y considero que facilita localizar errores, modificar funcionalidades y ampliar la aplicación.

## 3. Procesamiento de datos y cálculo de señales

Para esta parte he utilizado principalmente Python, Pandas y NumPy, ya que son librerías con las que estoy familiarizado por trabajos anteriores.

Primero he realizado la lectura y validación de los datasets, comprobando que las respuestas tengan valores válidos y que la configuración de los ítems sea correcta.

Después he aplicado las transformaciones necesarias para calcular las señales, teniendo en cuenta las preguntas invertidas y los pesos de cada ítem. Las puntuaciones se normalizan a una escala de 0 a 100 para facilitar su interpretación.

Para los Career & Life Moments he utilizado combinaciones de las señales obtenidas, intentando que las puntuaciones representen diferentes situaciones profesionales sin asignar a cada persona una única categoría.

En el análisis de cohortes he agrupado los resultados por edad, rol y modalidad de trabajo. También he tenido en cuenta el tamaño mínimo de las cohortes para evitar mostrar información de grupos demasiado pequeños.

## 4. Desarrollo de la API

Para desarrollar la API he partido de una aplicación que había realizado anteriormente en un proyecto de Computación, en el que desarrollamos una aplicación de predicción del tráfico mediante modelos de Machine Learning.

En aquel proyecto ya habíamos trabajado con una API para conectar las diferentes partes de la aplicación y permitir la consulta de los resultados de las predicciones.

Como ya estaba familiarizado con esa estructura, decidí reutilizarla como referencia en lugar de empezar completamente desde cero.

En esta parte utilicé **ChatGPT para que me ayudara a adaptar el modelo de API que ya tenía desarrollado a las necesidades específicas de HumanOS**.

Principalmente, lo utilicé para reorganizar los endpoints, adaptar las respuestas al formato JSON requerido y conectar las diferentes funcionalidades del proyecto.

Finalmente, la API se ha desarrollado utilizando FastAPI y permite consultar las señales, los Career & Life Moments y los resultados de las diferentes cohortes.

Durante la implementación también utilicé ChatGPT para solucionar algunos problemas relacionados con la instalación de dependencias, los entornos virtuales y la ejecución del servidor con Uvicorn.

## 5. Reto opcional A – Machine Learning

Para el reto opcional he elegido la **Opción A: Predictive Modelling**, ya que es la parte con la que me siento más familiarizado debido a mi experiencia en proyectos anteriores.

Anteriormente había trabajado en un proyecto de predicción de criptomonedas, donde utilicé técnicas de Machine Learning para analizar datos históricos e intentar predecir su comportamiento.

También participé en un proyecto de Computación en el que desarrollamos una aplicación que utilizaba modelos predictivos para estimar el tráfico en diferentes carreteras.

Por eso, para esta práctica decidí utilizar modelos y metodologías similares a los que ya conocía, adaptándolos al problema planteado por HumanOS.

El objetivo ha sido utilizar las variables disponibles en Wave 1 para intentar predecir el valor de Future Visibility en Wave 2.

### Preparación de los datos

Primero he realizado un análisis exploratorio del dataset para comprobar los tipos de variables, los valores nulos y la distribución de los datos.

Después he separado las variables predictoras de la variable objetivo y he dividido los datos en entrenamiento y prueba, utilizando un 80 % para entrenar y un 20 % para evaluar.

También he aplicado las transformaciones necesarias para trabajar con variables categóricas y numéricas.

### Modelos utilizados

He comparado varios modelos de regresión:

- **Dummy Regressor:** como modelo de referencia para comprobar si los demás modelos realmente aportaban una mejora.
- **Ridge Regression:** un modelo de regresión lineal regularizada.
- **Random Forest Regressor:** un modelo basado en la combinación de varios árboles de decisión.
- **Gradient Boosting Regressor:** un modelo que combina árboles de forma secuencial para mejorar las predicciones.

La elección de estos modelos se debe principalmente a que ya había trabajado con técnicas de regresión y modelos basados en árboles en proyectos anteriores.

Para comparar los resultados he utilizado MAE, RMSE y R². También he aplicado validación cruzada para comprobar que el rendimiento no dependiera únicamente de una división concreta de los datos.

Finalmente, he seleccionado **Ridge Regression**, ya que obtuvo un buen equilibrio entre precisión, estabilidad e interpretabilidad.

Una vez obtenidas las predicciones de Wave 2, he calculado la diferencia respecto a Wave 1 para estimar si Future Visibility podría aumentar o disminuir.

### Interpretación de los resultados

Una de las cosas que he tenido en cuenta es que el modelo permite identificar relaciones predictivas, pero no demostrar relaciones de causa y efecto.

Por ejemplo, aunque una variable tenga bastante importancia en la predicción, eso no significa necesariamente que sea la responsable de que Future Visibility aumente o disminuya.

También he considerado las limitaciones del dataset, especialmente su tamaño y el hecho de que los datos sean sintéticos.

## 6. Uso de Inteligencia Artificial

Durante el desarrollo he utilizado **ChatGPT como herramienta de apoyo**, pero intentando partir de conocimientos, código y experiencias que ya tenía de proyectos anteriores.

Los principales usos que le he dado han sido:

- Adaptar la estructura de la API de mi anterior aplicación de predicción del tráfico a los requisitos de HumanOS.
- Ayudarme a organizar el código en diferentes módulos.
- Revisar algunas funciones y comprobar que se ajustaran a lo solicitado.
- Resolver errores relacionados con librerías, importaciones y ejecución del proyecto.
- Apoyarme en la comparación de modelos de Machine Learning y en la interpretación de los resultados.
- Ayudarme a estructurar la documentación del proyecto.

He intentado utilizar la IA como una herramienta que me permitiera avanzar más rápido y adaptar soluciones que ya conocía, en lugar de limitarme a generar código sin entender su funcionamiento.

## 7. Decisiones técnicas y limitaciones

Una de las principales decisiones ha sido utilizar Python para todo el proyecto, ya que me permitía trabajar con los datos, desarrollar los modelos predictivos y crear la API dentro de un mismo entorno.

También he priorizado una arquitectura modular para facilitar el mantenimiento y la reutilización del código.

En cuanto al Machine Learning, he preferido utilizar modelos que pudiera interpretar y comparar correctamente, en lugar de buscar únicamente el modelo más complejo.

Entre las principales limitaciones destacaría que los datos son sintéticos y que el número de participantes es relativamente reducido, especialmente para analizar determinados grupos.

Además, las fórmulas utilizadas para calcular los Career & Life Moments son una propuesta exploratoria y necesitarían validarse antes de utilizarlas en un entorno real.

Por último, aunque la API permite consultar los resultados, considero que en una aplicación real sería necesario añadir autenticación, controles de acceso y una gestión más completa de los errores.

## 8. Posibles mejoras

Si continuara desarrollando el proyecto, algunas mejoras que me gustaría incorporar serían:

- Crear una interfaz gráfica para visualizar las señales y los resultados de las cohortes.
- Añadir una base de datos para almacenar los resultados.
- Incorporar autenticación y diferentes permisos de acceso a la API.
- Ampliar las pruebas automatizadas.
- Probar los modelos predictivos con un conjunto de datos más grande y representativo.
- Incorporar nuevas mediciones temporales para analizar cómo evolucionan las señales.

## 9. Conclusión personal

Este reto me ha parecido una buena oportunidad para aplicar conocimientos de diferentes asignaturas y proyectos en un mismo desarrollo.

La parte de Machine Learning ha sido la que me ha resultado más familiar, porque ya había trabajado anteriormente con modelos predictivos tanto en el proyecto de criptomonedas o en la aplicación de predicción del tráfico que comentamos en la entrevista.

En cambio, la parte de procesamiento de señales y Career & Life Moments me ha permitido trabajar con un problema diferente, en el que no se trata solamente de obtener resultados numéricos, sino también de interpretarlos correctamente.

Para la API me ha resultado útil poder partir de una estructura que ya conocía y utilizar ChatGPT para adaptarla a este nuevo contexto.

En general, he intentado combinar mis conocimientos previos con el uso de herramientas de IA para desarrollar una solución organizada, comprensible y que pudiera seguir mejorando en el futuro.
