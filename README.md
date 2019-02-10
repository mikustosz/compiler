# Kompilator języka LATTE
napisany w języku Python 3.7

### Uruchamianie
Żeby uruchomić kompilator należy wcześniej uruchomić:
```
make
source venv/bin/activate
```
Kompilator uruchamiamy wpisując lub `./lattc_llvm` podając ścieżkę do pliku w formacie _.lat_.


### Struktura projektu
W katalogu `lib/` znajdziemy bibliotekę jasmin. Poza tym w katalogu `gen/` znajdują się pliki wygenerowane przez parser/lekser ANTLR. Biblioteka ta jest także używana podczas uruchamiania kompilatora, dlatego ważne jest żeby mieć zainstalowaną bibliotekę pip: _antlr4-python3-runtime_.

W katalogu `src/` znajdziemy kod źródłowy programów.


### Implementacja
Zaimplementowany frontend oraz backend w llvm w postaci SSA