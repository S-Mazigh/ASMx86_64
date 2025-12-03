# L'alignement de la pile en x86_64

## Rappel sur l'adressage de la RAM

La mémoire vive (RAM) est adressable par octet, ce qui signifie qu'une adresse correspond à un octet unique. À titre de comparaison, les SSD, bien que très rapides, sont utilisés comme mémoire secondaire car leur gestion interne se fait par blocs, et non par octet. Cependant, au *niveau logiciel*, il est possible d'accéder à des données de taille *inférieure* à un bloc, mais les transactions coûtent aussi chers vu qu'en vrai on travaille avec un bloc.

Lorsque l'on souhaite récupérer plusieurs octets consécutifs en RAM, deux méthodes principales existent :  
1. Effectuer plusieurs déréférencements successifs (peu efficace).  
2. Utiliser un accès aligné, permettant de récupérer plusieurs octets en une seule opération.

Considérons une mémoire de $2^{16}$ octets (64 Ko), avec des adresses sur 16-bits.

```{figure} ./_static/images/ExampleRam-1.svg
:align: center
:alt: Un schéma de RAM avec des adresses en 4-bits.
Un schéma de RAM avec des adresses en 4-bits.
```

 Si l’on veut lire l'octet à l'adresse `0x210F` (figure de gauche), une seule requête est nécessaire. Cependant, pour accéder à deux octets à partir de cette adresse (`0x210F` et `0x2110`), il faudra effectuer deux requêtes (figure de droite), car les deux octets ne se trouvent pas sur une adresse alignée.

````{subfigure} AB
:layout-sm: A|B
:name: ram-example-1
:align: center
:subcaptions: above
```{image} ./_static/images/ExampleRam-2.svg
:alt: Récupérer un octet depuis la RAM.
```

```{image} ./_static/images/ExampleRam-3.svg
:alt: Récupérer deux octets non-alignés depuis la RAM.
```

La lecture en RAM peut se faire en plusieurs fois.
````

Si les **2** octets commencent à une adresse alignée sur **2**, comme `0x210E`, et que le controlleur mémoire supporte les accés dit alignés, il est possible de les lire en une seule fois. Une adresse alignée pour des données de **2** octets est un multiple de $2^1$ :  
- `0x210E = 0b0010 0001 0000 1110` (le dernier bit est 0, indiquant un multiple de $2^1$).

Ainsi, les processeurs (et leurs contrôleurs mémoire) peuvent optimiser les accès alignés, en réduisant les requêtes nécessaires.

Une donnée de taille $N$ doit généralement être adressée par une adresse multiple de $N$. Par exemple, pour un entier (`int`) de **4** octets, l’adresse doit être un multiple de **4**. Cette règle permet aux processeurs de maximiser l’efficacité des accès mémoire. Par exemple, parmis les adresses dans notres schémas, une données de **16** octets (`long double`) devrait être stocké soit à partir de `0x0000`,`0x2100` ou `0x2110` (on a besoin que les 4 derniers bits soit à 0, i.e multiple de **16**).

```{figure} ./_static/images/ExampleRam-6.svg
:alt: Lire 16 octets en une requête
:align: center

Lire 16 octets en une requête.
```

Cependant, l'alignement strict dépend des architectures :
- **x86 (Intel/AMD)** : Tolère les accès non alignés, mais avec une légère pénalité de performance. Le processeur peut gérer les accès en plusieurs cycles mémoire si nécessaire.
- **M68k (premiers processeurs)** : Génère une exception en cas d’accès non aligné. Cela imposait des contraintes strictes sur le placement des données en mémoire.
- **ARM**: Les anciennes versions de l'architecture ne supportaient pas les accès non alignés. Mais depuis ARMv6, ces accès sont "*possibles*" ([arm-doc](https://developer.arm.com/documentation/ddi0290/g/unaligned-and-mixed-endian-data-access-support/unaligned-access-support/armv6-extensions?lang=en)) avec pas mal de restrictions ([stackoverflow](https://stackoverflow.com/questions/18269181/unaligned-access-causes-error-on-arm-cortex-m4)).

```{admonition} Impact des accès non alignés
:class: warning
Même sur des processeurs comme le x86, les accès non alignés restent plus lents qu’un accès aligné, car ils peuvent nécessiter des lectures multiples et des opérations supplémentaires pour assembler les données.
```

Les processeurs lisent souvent des blocs de mémoire plus larges que la taille exacte des données demandées. Par exemple :
- Si un processeur charge toujours 4 octets à la fois, une adresse `0x210F` sera interprétée comme `0b0010 0001 0000 11XX` (en ignorant les deux derniers bits), où X peut être 1 ou 0. Ainsi, les octets chargés seront : `0x210C`, `0x210D`, `0x210E`, et `0x210F`.
- Si un entier (`int`: 4 octets) commence à l'adresse `0x2103`, deux lectures de 4 octets seront nécessaires :
  1. `0x2100` à `0x2103`.
  2. `0x2104` à `0x2107`.  
  Ensuite, le processeur assemblera les octets nécessaires (il aura chargé 4 octets inutiles!).
- Si l'entier commence à une adresse alignée comme `0x2104`, une seule lecture suffira.

````{subfigure} AB
:layout-sm: A|B
:name: ram-example-2
:align: center
:subcaptions: above
```{image} ./_static/images/ExampleRam-4.svg
:alt: Deux blocs de 4 octets sont lus.
```

```{image} ./_static/images/ExampleRam-5.svg
:alt: Un seul bloc de 4 octet est lu.
```

Lecture 4 octets alignée vs non alignée.
````

Les processeurs modernes ont pratiquement tous de la mémoire cache. Et Ils utilisent des techniques comme le préchargement (pré-fetching) pour anticiper les besoins en données. Cela consiste à charger plusieurs octets d’un coup pour remplir une ligne de cache, typiquement de 64 octets. Si une donnée de 16 octets est mal alignée, le processeur devra :
1. Charger une première ligne de cache de 64 octets contenant une partie des données.
2. Charger une seconde ligne de cache de 64 octets contenant le reste des données.
Ainsi une donnée qui aurait pu tenir dans une seule ligne de cache génère deux requêtes mémoire, augmentant le temps d’accès et diminuant les performances.


<blockquote class="small-text">
Références:
<ul>
<li><a href="https://developer.ibm.com/articles/pa-dalign/" target="_blank">https://developer.ibm.com/articles/pa-dalign/</a></li>
</blockquote>


## Comprendre l'alignement de la pile en Linux AMD64

Sur les architectures x86_64 (AMD64), la norme ABI (Application Binary Interface) System V impose que la pile soit alignée sur **16 octets** avant l'exécution d'une fonction.

Dans l'abi on a: 
> In addition to registers, each function has a frame on the run-time stack. This stack grows downwards from high addresses. Figure 3.3 shows the stack organization. The end of the input argument area shall be aligned on a 16 (32 or 64, if __m256 or __m512 is passed on stack) byte boundary. In other words, the value (%rsp + 8) is always a multiple of 16 (32 or 64) when control is transferred to the function entry point. The stack pointer, %rsp, always points to the end of the latest allocated stack frame.

Je vais vous expliquer le paragraphe, petit à petit avec de meilleurs schémas:

> In addition to registers, each function has a frame on the run-time stack. This stack
grows downwards from high addresses.

Chaque fonction à une stack frame (une section de la pile du processus) qui commence à une adresse haute qui est decrementée à chaque allocation (sauvegarde de registes ou allocations de variables locales).

> The end of the input argument area shall be aligned on a 16 (32 or 64, if __m256 or __m512 is passed on stack) byte boundary.

Une fois tous les arguments empilés (du 7ème au n-ème), l'adresse mémoire dans `%rsp` (le sommet de la pile) doit être alignée sur 16 (32 ou 64) dependant des types de données empilé. Dans notre cas on ne va pas utilisé les types `__m256` et `__m512` qui sont utilisés par les instructions SIMD (Single Instruction Multiple Data).

> In other words, the value `(%rsp + 8)` is always a multiple of 16 (32 or 64) when control is transferred to the function entry point. The stack pointer, `%rsp`, always points to the end of the latest allocated stack frame.

Ici le paragraphe parle de la valeur d'`%rsp` directement après que l'adresse de retour fu empilée. La valeur de `%rsp + 8` represente ainsi l'**adresse** où *l'adresse de retour* est stockée. Ainsi la conclusion est: 

<center> <blockquote class="conclusion">Avant un <code>call</code> la pile doit être alignée sur 16! </blockquote></center>

Prennant le programme Hello World comme exemple:

```nasm
    .global main

    .text
main:
    sub     $8, %rsp
    movq    $message, %rdi
    call    puts
    mov     $0, %rax
    add     $8, %rsp
    ret

message:
    .asciz "Hello, world!"
```

:::{important}
- Les figures suivantes utilisent des adresses sur 32-bits à la place de 64-bits pour une lecture plus facile.
- Rappelez-vous, pour vérifier si une adresse est alignée sur 16, il suffit de voir si les 4 derniers bits (le dernier hex) sont à 0.
:::

Pour commencer, il faut savoir qu'il existe une hypothèse forte sur l'état initiale. On suppose que le bootstrapper qui appel `main` a respecté l'ABI, et ainsi avant `call main` le sommet de la pile `%rsp` était alignée sur 16.

```{figure} ./_static/images/StackAlignment-1.svg
:alt: L'alignment de la pile à l'entrée dans main.
:align: center
L'alignment de la pile à l'entrée dans main.
```

Vu que le `call` **push** la valeur de `%rip` dans la pile (une adresse de 8 octets), le sommet de la pile `%rsp` perd son alignement sur 16 pour un alignement sur 8.

```{figure} ./_static/images/StackAlignment-2.svg
:alt: L'adresse de retour fu empilée
:align: center

L'adresse de retour fu empilée
```

Du coup, pour avoir un alignement sur 16 avant de faire `call puts` il faut décrementer le `%rsp` de 8 pour avoir une decrementation de 16 au total (le **push** de `call main` + notre décrementation). On peut faire cela rapidement par:
- un **push** d'un registre de 8 octets.
- ou une soustraction de 8 sur `%rsp`.

```{figure} ./_static/images/StackAlignment-3.svg
:alt: On s'assure que le sommet de la pile est aligné sur 16 via une soustraction de 8.
:align: center

On s'assure que le sommet de la pile est aligné sur 16 via une soustraction de 8.
```

L'histoire se répète pour le `call puts`, le sommet de pile perd son alignement sur 16 aprés le `call` et le retrouve au `ret` de `puts`. Le `%rsp` pointera sur les données rouges au retour de `puts`.

Maintenant, pour que le `ret` de `main` puisse **pop** la bonne adresse de retour, on doit placer `%rsp` sur le debut de l'adresse de retour. Sinon on lira d'autres données binaires comme l'adresse de retour, et le `%rip` peut se retrouver de l'autre côté de la galaxy.

## Pourquoi faire compliqué quand on peut faire simple ?

<!-- La pile (stack) est une zone mémoire utilisée par les programmes pour gérer les appels de fonction, les variables locales, et les adresses de retour. Sur x86_64, la pile croît **vers les adresses basses** : chaque allocation réduit la valeur du pointeur de pile `%rsp`. L'ABI stipule que juste avant qu'une fonction ne commence son exécution, la valeur `%rsp + 8` (c'est-à-dire le sommet effectif de la pile, où est stockée l'adresse de retour) doit être un multiple de 16. -->

Des fois, on n'a pas le choix. L'idée derrière cet alignement de 16 octets est directement liée à la gestion des données SIMD (Single Instruction, Multiple Data), en particulier les instructions SSE (Streaming SIMD Extensions) et AVX. Ces instructions, utilisées pour des calculs vectoriels, manipulent des blocs de données de 16 ou 32 octets. En pratique, les opérations sur les flottants sont faites avec ces instructions. Si ces blocs ne sont pas alignés correctement en mémoire, cela peut entraîner une dégradation des performances ou même des erreurs sur des architectures anciennes.

```{admonition} L'importance de l'alignement
:class: important
Imaginez que le processeur doit charger un bloc de 16 octets pour une instruction SIMD. Si ce bloc commence à une adresse non alignée, plusieurs requêtes mémoire sont nécessaires pour rassembler les données, ce qui ralentit l'exécution. L'alignement garantit que ces blocs peuvent être chargés en une seule opération, optimisant ainsi les performances. 
```

```{admonition} Encore plus important
:class: warning
Sur certaines architectures plus anciennes ou strictes, comme avec les versions SSE1 et SSE2 de x86, un accès mal aligné provoque une exception fatale. 
```


Dans l'ABI System V, l'alignement de 16 octets garantit que les instructions SSE, qui utilisent les registres XMM pour des blocs de 128-bits (16 octets), fonctionnent sans problème (pas de segfault). De plus, les extensions AVX, qui opèrent sur des blocs encore plus grands (256-bits ou 512-bits), renforcent cette nécessité avec un alignement de 32 ou 64 octets dans des cas spécifiques.

Si vous vous demandez pourquoi une fonction semble fonctionner dans certains cas et planter dans d'autres, pensez à vérifier l'alignement de la pile. Des posts comme [why 16B alignment](https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment) ou [ce cas spécifique](https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r) sur `scanf` montrent bien que des erreurs subtiles peuvent survenir à cause de ce détail souvent négligé.

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment" target="_blank">https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment</a></li>
<li><a href="https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r" target="_blank">https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r</a></li>
</blockquote>