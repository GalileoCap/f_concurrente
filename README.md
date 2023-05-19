# TP Programación Concurrente

## Integrantes

* F. Galileo Cappella Lewi, 653/20
* Leo Mansini

## Ejecución del programa
Se necesita `java`
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
cd ./analyze && pipenv run python main.py
```
