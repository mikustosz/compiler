# compiler

## Running ANTLR
Wykonaj w terminalu:
```
export CLASSPATH=".:/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH"
alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java org.antlr.v4.gui.TestRig'
```

### Generowanie gramatyki
```
cd src/
antlr4 -Dlanguage=Python3 -visitor Latte.g4 -o gen/
```
### How to run gui:
https://github.com/antlr/antlr4/blob/master/doc/getting-started.md
grun <NAME> r -gui


****************************************************** 
*Żeby uzyskać kod jvm należy:*
```
javac Hello.java
java -jar lib/classfileanalyzer.jar Hello.class > Hello.j
```

*Żeby z kodu Hello.j otrzymać znowu plik class:*
```
java -jar lib/jasmin.jar Hello.j
```


### Full skrypt do testowania
```
python -m src.main > experiments/Siemanko.j && java -jar lib/jasmin.jar experiments/Siemanko.j && mv Siemanko.class experiments/ && cd experiments/ && java Siemanko && cd ..
```

## Frontend rules
OK There should be at leas one main function in the code
OK If a function is used it must be declared anywhere
OK If a function is used it must have arguments of the same type as declared
 * If a var is used it must be declared BEFORE usage
OK A var must not be assigned value of a wrong type
OK A var must not be declared twice
OK Var type shouldn't be void
OK if a function is declared as a type it must always return this type
OK if a function returnes void it musn't return anything
OK number of arguments in function must always be as declared
OK return function must be reachable
OK any function with type other than void must have at least one return function with correct type
OK return must be of the same type
OK expressions: you cannot mix types! 
OK you cannot pass wrong types to functions