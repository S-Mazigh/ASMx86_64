# My_Atou

## Vue d'ensemble des implémentations

### 1. Implémentation naïve
```nasm
my_atou_naive:
    push %rbp
    movq %rsp, %rbp
    xorq %rax,%rax
    xorq %rsi,%rsi 
    movl $10, %ecx

loop:
    movb (%rdi), %sil
    cmpb $0, %sil
    je end
    subb $48, %sil
    mul %ecx
    addl %esi, %eax
    inc %rdi
    jmp loop
end:
    movq %rbp,%rsp
    popq %rbp
    ret
```

> - Ceci est la version réalisée durant la remédiation. Petite mais importante modification : j'ai utilisé %sil au lieu de %dl, car %rdx (et donc %dl) est modifié par l'instruction `mul` !
> - `mull` n'existe pas, même en AT&T, la taille est déduite par le nom du registre.

### 2. Implémentation avec une meilleure boucle
```nasm
my_atou_better_loop:
    push %rbp
    movq %rsp, %rbp
    xorq %rax,%rax
    xorq %rsi,%rsi
    movl $10, %ecx 

    movb (%rdi), %sil  # Amorçage 

loopp:
    subb $48, %sil
    mul %ecx
    addl %esi, %eax
    inc %rdi
    movb (%rdi), %sil
    cmpb $0, %sil
    jne loopp
    movq %rbp,%rsp
    popq %rbp
    ret
```
- La boucle peut être écrite avec un seul branchement, il suffit de précharger le premier caractère pour que le fonctionnement soit correct.

### 3. Implémentation sans multiplication
```nasm
my_atou_no_mul:
    push %rbp
    movq %rsp, %rbp
    xorq %rax,%rax
    xorq %rsi,%rsi

    movb (%rdi), %sil

loopppp:
    subb $48, %sil
    movl %eax, %ecx
    sal $3, %eax    # eax = eax * 8
    sal $1, %ecx    # ecx = ecx * 2
    addl %ecx ,%eax # eax = (eax * 8) + (eax * 2) = eax * 10
    addl %esi, %eax  
    inc %rdi
    movb (%rdi), %sil
    cmpb $0, %sil
    jne loopppp
    movq %rbp,%rsp
    popq %rbp
    ret
```

- On peut éviter d'utiliser `mul` et rester avec nos bons vieux décalages à gauche (left shift) et additions.
- `x * 10 = (x * 8) + (x * 2)`
- On a plus d'opérations, mais elles sont bien plus simples que mul, et `%rdx` n'est plus utilisé, on peut donc l'utiliser au lieu de `%rsi` si on le souhaite !

### 4. Implémentation avec LEA (Load Effective Address)

> Attention ! lea est l'incarnation même de la confusion. À utiliser avec précaution, et seulement après avoir débloqué le statut "Génie de la confusion".

```nasm
my_atou_lea:
    push %rbp
    movq %rsp, %rbp
    xorq %rax,%rax
    xorq %rsi,%rsi

    movb (%rdi), %sil

looppp:
    subb $48, %sil
    lea (%eax,%eax,4), %eax    # eax = eax + eax * 4
    lea (%esi,%eax,2), %eax    # eax = esi + (eax * 2)
    inc %rdi
    movb (%rdi), %sil
    cmpb $0, %sil
    jne looppp
    movq %rbp,%rsp
    popq %rbp
    ret
```

- Le fameux `lea` ! Pour rappel, les parenthèses ne font pas de déréférencement ! Le processeur ne fait que le calcul d'adresse et écrit le résultat dans le registre de destination. Autrement dit, `lea (%r2,%r3,i), %r1` permet de faire des opérations de type : `r1 = r2 + r3*i`, où `i` ne peut être égal qu'à 1, 2, 4 ou 8.

## Résultats de performance

### Grands nombres (>1 000 000)
```
❯ ./my_atou 10000000 1
Starting stress test with 10000000 iterations...


Test completed successfully! All implementations gave matching results.

Timing results:
glibc:       1.620747 seconds (avg: 0.000000162)
naive:       1.519484 seconds (avg: 0.000000152)
better_loop: 1.510028 seconds (avg: 0.000000151)
no_mul:      1.500172 seconds (avg: 0.000000150)
lea:         1.498446 seconds (avg: 0.000000150)
```

### Tous les nombres
```
❯ ./my_atou 10000000 0
Starting stress test with 10000000 iterations...


Test completed successfully! All implementations gave matching results.

Timing results:
glibc:       1.622808 seconds (avg: 0.000000162)
naive:       1.527342 seconds (avg: 0.000000153)
better_loop: 1.516223 seconds (avg: 0.000000152)
no_mul:      1.506818 seconds (avg: 0.000000151)
lea:         1.506587 seconds (avg: 0.000000151)
```

## Conclusions

1. La différence est très petite (< 6%). Au moins, nous sommes plus rapides que `atoi()` qui est bien plus complexe, ce qui montre que notre approche est valide.
2. L'implémentation avec `lea` semble être la meilleure, mais en réalité j'ai eu un test plus court où elle ne l'était pas, exemple :

```
❯ ./my_atoi 10000 0
Démarrage du test de stress avec 10000 itérations...

Test complété avec succès ! Toutes les implémentations ont donné des résultats identiques.

Résultats temporels :
glibc :       0,002512 secondes (moy : 0,000000251)
naive :       0,002374 secondes (moy : 0,000000237)
better_loop : 0,002405 secondes (moy : 0,000000240)
no_mul :      0,002294 secondes (moy : 0,000000229)
lea :         0,002327 secondes (moy : 0,000000233)
```

- Nos processeurs modernes ont de nombreuses optimisations :
  - Prédiction de branchement
  - Pipeline d'instructions
  - Préchargement du cache
   
Toutes ces optimisations rendent même la gestion de plusieurs caractères à la fois équivalente en performance. En fait, on peut faire ce qu'on appelle du déroulage de boucle où on récupère 8 octets depuis la mémoire et on teste 8 caractères à la fois. Cela complexifie énormément le programme et on ne gagne pas grand-chose, puisque de toute façon les prochains caractères sont préchargés en cache.

> "Premature optimization is the root of all evil" - Donald Knuth

Parfois, la solution la plus simple ou naïve est suffisante, pas la peine de chercher à faire passer votre programme en ludicrous speed. 

<center>
<img src=./_static/images/gifs/spaceballs-ludicrous.gif alt="Ludicrous Speed"/>
</center>

Mais j'admets que c'est plus amusant ainsi, donc amusez-vous bien.

<center>
<img src="./_static/images/gifs/malcom-hal.gif" alt="Boule de neige effect"/>
</center>

## Appendix

- Les sources sont par [ici](../resources/my_atou.zip). Il suffit de `make`.
    - Dans le fichier `my_atou.s` vous verrez que j'ai utilisé souvent `1:` ou `2:` comme label. Ce sont des labels un peu spéciaux où il faut spécifier dans quelle direction le `jmp` doit chercher le label (b pour backward et f pour forward). D'où les `jne 1b` pour revenir au label `1:` de la boucle (le plus proche) \[<a href="https://docs.oracle.com/cd/E19120-01/open.solaris/817-5477/esqaq/index.html" target="_blank">ref</a>\].
    - Vous trouverez un my_atou qui vérifie si les caractères sont des chiffres, pour rappel `ja 3f` veut dire saute au label `3:` présent dans ce code si la valeur non signée est supérieur:

```nasm
    my_atou:

    push %rbp
    movq %rsp, %rbp
    xorq %rax,%rax
    xorq %rsi,%rsi

    movb (%rdi), %sil

    1:
    cmpb $0x30, %sil
    jb 3f
    cmpb $0x39, %sil
    ja 3f

    subb $0x30, %sil
    movl %eax, %ecx
    sal $3, %eax    
    sal $1, %ecx
    addl %ecx ,%eax
    addl %esi, %eax  

    inc %rdi
    movb (%rdi), %sil
    testb %sil,%sil
    jnz 1b

    2:
    movq %rbp,%rsp
    popq %rbp
    ret

    3:
    xorq %rax, %rax
    jmp 2b
```

- On peut remplacer `subb $48, %sil` par `andb $0x0F, %sil`. Cette technique fonctionne comme un modulo pour les caractères ASCII des chiffres décimaux (0-9) car leur valeur hexadécimale suit le pattern `0x3n`.
    - 0x30 == '0'
    - 0x31 == '1'
    - ...
    - 0x39 == '9'
- Ainsi on poura s'amuser à faire entrer des chaines de caractères du type "abcf" qui donnera le nombre 1236. Cependant, pour les caractères ayant A,B,C,D,E,F comme dernier hexadécimal, l'opération les conservera et ils correspondent à des valeurs non décimales (10-15), ce qui produira des résultats incorrects lors de l'addition avec `%eax`.

```nasm
my_atou_better_loop:
push %rbp
movq %rsp, %rbp
xorq %rax,%rax
xorq %rsi,%rsi 
movl $10, %ecx 

movb (%rdi), %sil 

1:
andb $0x0F, %sil
mul %ecx
addl %esi, %eax
inc %rdi
movb (%rdi), %sil
cmpb $0, %sil
jne 1b

movq %rbp,%rsp
popq %rbp
ret
```