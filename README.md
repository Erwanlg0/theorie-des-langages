# Projet Interpréteur mini langage groupe 2 

```
# affectation, print
s1 = 'x=4;x=x+3;print(x);'

# opérations arithmétiques
s2 = 'a=10;b=3;c=a*b;print(c);d=a/b;print(d);'

# if / if-else
s3 = 'x=5;if(x>3){print(x);};'
s4 = 'x=2;if(x>3){print(x);}else{y=99;print(y);};'

# while
s5 = 'x=4;while(x<30){x=x+3;print(x);};'

# for
s6 = 'for(i=0;i<4;i=i+1;){print(i*i);};'

# combiné while + for
s7 = 'x=4;while(x<30){x=x+3;print(x);};for(i=0;i<4;i=i+1;){print(i*i);};'

# gestion d'erreur : variable non initialisée
s8 = 'print(z);'

# gestion d'erreur : division par zéro
s9 = 'x=5;y=0;print(x/y);'
```

---

- `lexer.py` — Analyse lexicale avec PLY
- `parser.py` — Analyse syntaxique, construction de l'AST et évaluation

