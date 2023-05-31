# TP Programación Concurrente: Listas Sincronizadas

## Integrantes

* F. Galileo Cappella Lewi, 653/20
* Leo Mansini, 318/19

## Ejecución del programa
Se necesita `java 17`
```bash
javac -d build $(find ./src -name "*.java")
java -cp build ThreadPool
```

## Ejecución del testing
Se necesita `java`
```bash
javac -d build $(find ./src -name "*.java")
java -cp build Test.RunTests
```

## Ejecución del análisis
Se necesita `python 3.11` con `Pipenv` (y si no se tiene la versión correcta de python se puede usar `pyenv` para instalarla).

* Opción 1: Descargar y correr [udo](dev.galileocap.me/udo)
* Opción 2: 
```bash
PIPENV_PIPFILE=./analyze/Pipfile pipenv install
PIPENV_PIPFILE=./analyze/Pipfile pipenv run python ./analyze/main.py
```

### Extra
Se puede ejecutar el archivo `analyze/convert_csv.py` para convertir los pickle guardados en csv.
```bash
PIPENV_PIPFILE=./analyze/Pipfile pipenv install
PIPENV_PIPFILE=./analyze/Pipfile pipenv run python ./analyze/convert_csv.py
```
