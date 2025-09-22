# L'alignement de la pile en amd64

## Rappel sur l'adressage de la RAM

La mémoire vive (RAM) est adressable par octet, ce qui signifie qu'une adresse correspond à un octet unique. À titre de comparaison, les SSD, bien que très rapides, sont utilisés comme mémoire secondaire car leur gestion interne se fait par blocs, et non par octet. Cependant, au *niveau logiciel*, il est possible d'accéder à des données de taille *inférieure* à un bloc, mais les transactions coûtent aussi chers vu qu'en vrai on travaille un bloc.

Lorsque l'on souhaite récupérer plusieurs octets consécutifs en RAM, deux méthodes principales existent :  
1. Effectuer plusieurs déréférencements successifs (peu efficace).  
2. Utiliser un accès aligné, permettant de récupérer plusieurs octets en une seule opération.

Considérons une mémoire de \(2^{16}\) octets (64 Ko), avec des adresses sur 16 bits.

<center><div  class="figure-container-small">
<figure>
    <img src="./_static/images/ExampleRam-1.svg" alt="A schema for 64KB RAM" class="figure">
</figure>
</div></center>

 Si l’on veut lire l'octet à l'adresse `0x210F`, une seule requête est nécessaire. Cependant, pour accéder à deux octets à partir de cette adresse (`0x210F` et `0x2110`), il faudra effectuer deux requêtes, car les deux octets ne se trouvent pas sur une adresse alignée pour une lecture de 2 octets.

 <center><div  class="figure-container-small">
<figure>
    <img src="./_static/images/ExampleRam-2.svg" alt="A schema for 64KB RAM" class="figure">
    <img src="./_static/images/ExampleRam-3.svg" alt="A schema for 64KB RAM" class="figure">
</figure>
</div>
</center>

Si les deux octets commencent à une adresse alignée, comme `0x210E`, et que le controlleur mémoire supporte les accés dit alignés, il est possible de les lire en une seule fois. Une adresse alignée pour des données de 2 octets est un multiple de \(2^1\) :  
`0x210E = 0b0010 0001 0000 1110` (le dernier bit est 0, indiquant un multiple de \(2^1\)).

Ainsi, les processeurs (et leurs contrôleurs mémoire) peuvent optimiser les accès alignés, en réduisant les requêtes nécessaires.

Une donnée de taille \(N\) doit généralement être adressée par une adresse multiple de \(N\). Par exemple, pour un entier (`int`) de 4 octets, l’adresse doit être un multiple de 4. Cette règle permet aux processeurs de maximiser l’efficacité des accès mémoire. Par exemple, parmis les adresses dans notres schémas, une données de 16 octets (`long double`) devrait être stocké soit à partir de `0x0000`,`0x2100` ou `0x2110` (on a besoin que les 4 derniers bits soit à 0).

<center><div  class="figure-container-small">
<figure>
    <img src="./_static/images/ExampleRam-6.svg" alt="A schema for 64KB RAM" class="figure">
</figure>
</div></center>

Cependant, l'alignement strict dépend des architectures :
- **x86 (Intel/AMD)** : Tolère les accès non alignés, mais avec une légère pénalité de performance. Le processeur peut gérer les accès en plusieurs cycles mémoire si nécessaire.
- **M68k (premiers processeurs)** : Génère une exception en cas d’accès non aligné. Cela imposait des contraintes strictes sur le placement des données en mémoire.
- **Systèmes embarqués simples** : Certains processeurs n'imposent pas d’alignement strict mais subissent des ralentissements en conséquence.

**Impact des accès non alignés :** Même sur des processeurs comme le x86, les accès non alignés restent plus lents qu’un accès aligné, car ils peuvent nécessiter des lectures multiples et des opérations supplémentaires pour assembler les données.

Les processeurs lisent souvent des blocs de mémoire plus larges que la taille exacte des données demandées. Par exemple :
- Si un processeur charge toujours 4 octets à la fois, une adresse `0x210F` sera interprétée comme `0b0010 0001 0000 11XX` (en ignorant les deux derniers bits), où X peut être 1 ou 0. Ainsi, les octets chargés seront : `0x210C`, `0x210D`, `0x210E`, et `0x210F`.
- Si un entier (`int`: 4 octets) commence à l'adresse `0x2103`, deux lectures de 4 octets seront nécessaires :
  1. `0x2100` à `0x2103`.
  2. `0x2104` à `0x2107`.  
  Ensuite, le processeur assemblera les octets nécessaires (il a chargé 4 octets inutiles!).
- Si l'entier commence à une adresse alignée comme `0x2104`, une seule lecture suffira.

<center><div  class="figure-container-small">
<figure>
    <img src="./_static/images/ExampleRam-4.svg" alt="A schema for 64KB RAM" class="figure">
    <img src="./_static/images/ExampleRam-5.svg" alt="A schema for 64KB RAM" class="figure">
</figure>
</div></center>

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

Une fois tous les arguments empilés (du 7ème au n-ème), l'adresse mémoire dans %rsp (le sommet de la pile) doit être alignée sur 16 (32 ou 64) dependant des types de données empilé. Dans notre cas on ne va pas utilisé les types `__m256` et `__m512` qui sont utilisés pour les instructions SIMD (Single Instruction Multiple Data).

> In other words, the value (%rsp + 8) is always a multiple of 16 (32 or 64) when control is transferred to the function entry point. The stack pointer, %rsp, always points to the end of the latest allocated stack frame.

Ici le paragraphe parle de la valeur de %rsp directement après que l'adresse de retour fu empilée. La valeur de %rsp + 8 represente ainsi l'adresse ou l'adresse de retour est stockée. Ainsi la conclusion est: 

<center> <blockquote class="conclusion">Avant un <code>call</code> la pile doit être aligné sur 16! </blockquote></center>

En revenant à l'exemple:

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

Alors, il existe une hypothèse forte sur l'état initiale. On suppose que le bootstrapper qui appel `main` a respecté l'ABI, et ainsi avant `call main` le sommet de la pile `%rsp` était alignée sur 16. Vu que le `call` push la valeur de `%rip` dans la pile (une adresse de 8 octets), le sommet de la pile `%rsp` perd son alignement sur 16 pour un alignement sur 8.

Du coup, pour avoir un alignement sur 16 avant de faire `call puts` il faut soit push un registre de 8 octets, ou soustraire 8 de `%rsp`.

Maintenant, pour que `ret` puisse pop la bonne adresse de retour, on doit replace `%rsp` sur le debut de l'adresse de retour.

### Mais pourquoi faire simple quand on peut faire compliqué ?

<!-- La pile (stack) est une zone mémoire utilisée par les programmes pour gérer les appels de fonction, les variables locales, et les adresses de retour. Sur x86_64, la pile croît **vers les adresses basses** : chaque allocation réduit la valeur du pointeur de pile `%rsp`. L'ABI stipule que juste avant qu'une fonction ne commence son exécution, la valeur `%rsp + 8` (c'est-à-dire le sommet effectif de la pile, où est stockée l'adresse de retour) doit être un multiple de 16. -->

Des fois, on n'a pas le choix. L'idée derrière cet alignement de 16 octets est directement liée à la gestion des données SIMD (Single Instruction, Multiple Data), en particulier les instructions SSE (Streaming SIMD Extensions) et AVX. Ces instructions, utilisées pour des calculs vectoriels, manipulent des blocs de données de 16 ou 32 octets. Si ces blocs ne sont pas alignés correctement en mémoire, cela peut entraîner une dégradation des performances ou même des erreurs sur des architectures anciennes.

**L'importance de l'alignement:**
> Imaginez que le processeur doit charger un bloc de 16 octets pour une instruction SIMD. Si ce bloc commence à une adresse non alignée, plusieurs requêtes mémoire sont nécessaires pour rassembler les données, ce qui ralentit l'exécution. L'alignement garantit que ces blocs peuvent être chargés en une seule opération, optimisant ainsi les performances. 

**Encore plus important:**
> Sur certaines architectures plus anciennes ou strictes, comme avec les verions SSE1 et SSE2 de x86, un accès mal aligné pouvait provoquer une exception fatale. 

Dans l'ABI System V, l'alignement de 16 octets garantit que les instructions SSE, qui utilisent les registres XMM pour des blocs de 128 bits (16 octets), fonctionnent sans problème (pas de segfault). De plus, les extensions AVX, qui opèrent sur des blocs encore plus grands (256 bits ou 512 bits), renforcent cette nécessité avec un alignement de 32 ou 64 octets dans des cas spécifiques.

Si vous vous demandez pourquoi une fonction semble fonctionner dans certains cas et planter dans d'autres, pensez à vérifier l'alignement de la pile. Des forums comme [Stack Overflow](https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment) ou [ce cas spécifique](https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r) sur `scanf` montrent bien que des erreurs subtiles peuvent survenir à cause de ce détail souvent négligé.

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment" target="_blank">https://stackoverflow.com/questions/49391001/why-does-the-x86-64-amd64-system-v-abi-mandate-a-16-byte-stack-alignment</a></li>
<li><a href="https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r" target="_blank">https://stackoverflow.com/questions/51070716/glibc-scanf-segmentation-faults-when-called-from-a-function-that-doesnt-align-r</a></li>
</blockquote>


<!-- ## Une responsabilité partagée

L'alignement de la pile n'est pas magique, il est géré par le programme lui-même. Lorsqu'une fonction est appelée, l'**appelant** (caller) doit s'assurer que la pile est correctement alignée avant de transférer le contrôle à la fonction. Cela signifie que si l'alignement est rompu à un moment donné, il appartient au programmeur ou au compilateur de corriger la situation. Ce point est particulièrement important dans les fonctions utilisant des bibliothèques comme glibc : une pile mal alignée peut provoquer des comportements imprévisibles, comme des erreurs de segmentation dans des appels à des fonctions simples telles que `scanf`.

## L'histoire derrière cet alignement -->

<!-- L'alignement strict trouve ses origines dans les instructions SIMD, introduites avec les processeurs SSE. Initialement, SSE exigeait un alignement de 16 octets pour fonctionner. Avec les extensions ultérieures comme SSE3 et AVX, des accès non alignés sont devenus possibles, mais au prix de performances moindres. Pour maintenir une compatibilité optimale et des performances maximales, l'ABI System V a standardisé l'alignement à 16 octets. -->

