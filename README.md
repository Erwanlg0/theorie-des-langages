# Projet interpreteur mini langage - groupe 2

Interpreteur realise avec PLY. L'analyse syntaxique construit un AST, l'affiche, puis execute le programme a partir de cet arbre.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

Lancer les exemples integres :

```bash
python parser.py
```

## Version minimale

```txt
x=4;
x=x+3;
print(x);

if(x>3){print(x);}else{print(0);};

while(x<10){
    x=x+1;
    print(x);
};

for(i=0;i<4;i=i+1){
    print(i*i);
};
```

Fonctionnalites minimales couvertes :

- variables avec noms a plusieurs caracteres ;
- affectation ;
- affichage d'expressions numeriques ;
- `if` / `if else` ;
- `while` et `for` ;
- affichage de l'AST en console.

## Correspondance exacte avec le sujet

### Spécifications de la version minimale (8/20)

- FAIT : Votre interpréteur devra gérer les noms de variables à plusieurs caractères.
- FAIT : affectation
- FAIT : affichage d’expressions numériques (pouvant contenir des variables numériques)
- FAIT : instructions conditionnelles : implémenter le si-alors-sinon/si-alors
- FAIT : structures itératives : implémenter le while et le for
- FAIT : Affichage de l’arbre de syntaxe (sur la console ou avec graphViz)

### Améliorations majeures  (entre autre)

- FAIT : Gérer les fonctions avec/ sans paramètre avec/sans valeur de retour
- FAIT : Gérer le scope des variables
- FAIT : Gérer les fonctions récursives terminales
- NON FAIT : Les tableaux
- NON FAIT : la POO
- NON FAIT : Gérer le passage des paramètres par référence (cf id() en python)

### Améliorations mineures  (entre autre)

- FAIT : Gestion des erreurs (variable non initialisée, …)
- FAIT : Gérer la déclaration explicite des variables
- FAIT : Gestion du type chaine de caractères (et extension d’autant de l’instruction d’affichage)
- FAIT : Gestion des variables globales
- FAIT : affectations multiples à la python : a, b = 2, 3
- NON FAIT : comparaison multiples à la python : 1<2<3
- FAIT : print multiples : print(x+2, « toto ») ;
- FAIT : incrémentation et affectation élargie : x++, x+=1
- FAIT EN PARTIE : possibilités de mettre des commentaires dans le code (et génération automatique d’une docString)

Pour le dernier point, les commentaires sont gérés, mais la génération automatique d’une docString n’est pas implémentée.

## Inputs de demonstration

```python
# affectation, print
s1 = 'x=4;x=x+3;print(x);'

# affectation elargie, incrementation
s2 = 'x=0;while(x<3){print(x);x++;};'

# while, for
s3 = 'for(i=0;i<4;i=i+1){print(i*i);};'

# chaine de caracteres et print multiple
s4 = 'var nom="mini langage";print("Projet", nom, 13);'

# affectation multiple
s5 = 'a,b=2,3;print(a,b);a+=10;print(a);'

# fonction avec parametre et valeur de retour
s6 = 'function carre(x){return x*x;}print(carre(5));'

# fonction sans parametre et sans valeur de retour utile
s7 = 'function bonjour(){print("bonjour");}bonjour();'

# return coupe-circuit
s8 = 'function test(){return 7;print(666);}print(test());'

# recursion terminale
s9 = 'function fact(n,acc){if(n==0){return acc;}else{return fact(n-1,acc*n);}}print(fact(5,1));'
```

### Fonctions et scope local

```txt
function carre(x){
    return x*x;
}

function bonjour(){
    print("bonjour");
}

print(carre(5));
bonjour();
```

Les appels de fonctions creent un scope local pour leurs parametres. Les fonctions avec et sans parametres sont acceptees, avec ou sans `return`.

### Recursion terminale

```txt
function fact(n, acc){
    if(n==0){
        return acc;
    }else{
        return fact(n-1, acc*n);
    }
}

print(fact(5, 1));
```

### Declarations explicites

```txt
var nom="mini langage";
var x=2, y=3;
```

### Chaines et print multiple

```txt
print("Projet", nom, x+y);
```

### Affectations multiples et elargies

```txt
a,b=2,3;
a+=10;
b*=2;
x++;
```

### Commentaires

```txt
# commentaire ligne
// commentaire ligne
/* commentaire
   sur plusieurs lignes */
```

### Gestion d'erreurs

L'interpreteur signale notamment :

- variable non initialisee ;
- division par zero ;
- mauvais nombre de parametres ;
- fonction non definie ;
- erreur de syntaxe avec annulation de l'execution.
