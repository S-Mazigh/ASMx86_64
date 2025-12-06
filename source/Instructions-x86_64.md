# Instructions Basiques

| Catégorie             | Opérations                | Opcodes                                                                                                                                                                                                                                        | Description                                                                                                  |
| --------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Mouvement de données  | Copie de registre/mémoire | [`mov`](https://www.felixcloutier.com/x86/mov)                                                                                                                                                                                                 | Transfère des données entre des registres, dans la mémoire ou charge des valeurs immédiates                  |
|                       | Copie Conditionnelle      | [`cmovcc`](https://www.felixcloutier.com/x86/cmovcc)                                                                                                                                                                                           | Déplace les données uniquement si le code de condition (cc) est rempli (par exemple, `cmove`, `cmovg`)       |
|                       | Copie avec extension      | [`movsx`](https://www.felixcloutier.com/x86/movsx:movsxd), [`movzx`](https://www.felixcloutier.com/x86/movzx)                                                                                                                                  | Étend le signe (`movsx`) ou étend avec zéro (`movzx`) les valeurs plus petites vers des tailles plus grandes |
| La Pile               | Push                      | [`push`](https://www.felixcloutier.com/x86/push)                                                                                                                                                                                               | Décrémente RSP et stocke l'opérande dans la pile                                                             |
|                       | Pop                       | [`pop`](https://www.felixcloutier.com/x86/pop)                                                                                                                                                                                                 | Charge la valeur depuis la pile et incrémente RSP                                                            |
|                       | Enter/Leave               | [`enter`](https://www.felixcloutier.com/x86/enter), [`leave`](https://www.felixcloutier.com/x86/leave)                                                                                                                                         | Crée/supprime une stack frame                                                                                |
| Arithmetique          | Math Basique              | [`add`](https://www.felixcloutier.com/x86/add), [`sub`](https://www.felixcloutier.com/x86/sub)                                                                                                                                                 | Addition et soustraction                                                                                     |
|                       | Multiplication            | [`mul`](https://www.felixcloutier.com/x86/mul), [`imul`](https://www.felixcloutier.com/x86/imul)                                                                                                                                               | Multiplication non signée (`mul`) et signée (`imul`)                                                         |
|                       | Division                  | [`div`](https://www.felixcloutier.com/x86/div), [`idiv`](https://www.felixcloutier.com/x86/idiv)                                                                                                                                               | Division non signée (`div`) et signée (`idiv`)                                                               |
|                       | Math Rapide               | [`inc`](https://www.felixcloutier.com/x86/inc), [`dec`](https://www.felixcloutier.com/x86/dec)                                                                                                                                                 | Incrémente ou décrémente de 1                                                                                |
|                       | Math Complexe             | [`lea`](https://www.felixcloutier.com/x86/lea)                                                                                                                                                                                                 | Load Effective Address, calcule l'adresse pointée, et la charge dans le registre                             |
| Bitwise               | Logique                   | [`and`](https://www.felixcloutier.com/x86/and), [`or`](https://www.felixcloutier.com/x86/or), [`xor`](https://www.felixcloutier.com/x86/xor)                                                                                                   | Opérations booléennes de base                                                                                |
|                       | Shifts                    | [`shl`](https://www.felixcloutier.com/x86/sal:sar:shl:shr), [`shr`](https://www.felixcloutier.com/x86/sal:sar:shl:shr)                                                                                                                         | Décalage logique à gauche/à droite                                                                           |
|                       | Arithmetic Shifts         | [`sal`](https://www.felixcloutier.com/x86/sal:sar:shl:shr), [`sar`](https://www.felixcloutier.com/x86/sal:sar:shl:shr)                                                                                                                         | Décalage arithmétique à gauche/à droite                                                                      |
|                       | Rotatation                | [`rol`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`ror`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`rcl`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`rcr`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror) | Rotation des bits                                                                                            |
| Comparaison           | Compare                   | [`cmp`](https://www.felixcloutier.com/x86/cmp)                                                                                                                                                                                                 | Soustrait les opérandes et définit les indicateurs                                                           |
|                       | Test                      | [`test`](https://www.felixcloutier.com/x86/test)                                                                                                                                                                                               | Fait un bitwise ANDs, met à jour les flags sans charger le résultat dans le registre destination             |
| Structure de contrôle | Jump Unconditionnel       | [`jmp`](https://www.felixcloutier.com/x86/jmp)                                                                                                                                                                                                 | Jump direct (unconditionnel)                                                                                 |
|                       | Jump Conditionnel         | [`jcc`](https://www.felixcloutier.com/x86/jcc)                                                                                                                                                                                                 | Jump si (condition)                                                                                          |
|                       | Call/Return               | [`call`](https://www.felixcloutier.com/x86/call), [`ret`](https://www.felixcloutier.com/x86/ret)                                                                                                                                               | Appel et retour de fonction                                                                                  |
| Contrôle des Flags    | Carry Flag                | [`clc`](https://www.felixcloutier.com/x86/clc), [`stc`](https://www.felixcloutier.com/x86/stc)                                                                                                                                                 | Clear/Set CF                                                                                                 |
|                       | Direction Flag            | [`cld`](https://www.felixcloutier.com/x86/cld), [`std`](https://www.felixcloutier.com/x86/std)                                                                                                                                                 | Clear/Set DF                                                                                                 |
|                       | Interrupt Flag            | [`cli`](https://www.felixcloutier.com/x86/cli), [`sti`](https://www.felixcloutier.com/x86/sti)                                                                                                                                                 | Clear/Set IF                                                                                                 |
| Système               | Appel Système             | [`syscall`](https://www.felixcloutier.com/x86/syscall)                                                                                                                                                                                         | Appel système                                                                                                |
|                       | Interruption              | [`int`](https://www.felixcloutier.com/x86/int)                                                                                                                                                                                                 | Interruption logicielle                                                                                      |

**Exemple avec lea:**

```nasm
; Récupérer l'adresse d'un élément dans un tableau contigue (array)
leal (%ebx, %ecx, 4), %eax    # eax = ebx + ecx*4 (tableau de dwords, i.e. 4 octets)
leaq (%rbx, %rcx, 8), %rax    # rax = rbx + rcx*8 (tableau de qwords, i.e. 8 octets)

; Addition de valeurs multiples
leal 5(%rax, %rbx), %eax      # eax = rax + rbx + 5 (addition à trois opérands)

; Multiplication et addition combinées
leal 5(%rax, %rax, 2), %eax   # eax = rax * 3 + 5
```

<!-- <center>
<img src="./_static/images/gifs/pulp-fiction-john-travolta-text.gif" alt="Pourquoi cette page est en anglais ?"/>
</center> -->


:::{admonition} Optimisations courantes
:class: tip
- `xor %rax, %rax` est plus efficace que `mov $0, %rax` pour mettre à zéro un registre.
- `test %rax, %rax` est plus efficace que `cmp $0, %rax` pour tester si un registre est à zéro.
- Le compilateur peut ajouter des instructions `nop` (qui font rien) pour optimiser l'alignement en mémoire et l'utilisation du cache d'instructions.
:::

:::{admonition} Notes pour le mode 64 bits
:class: important
- Les opérations 32 bits sur les registres étends implicitement leur valeur à 64 bits avec des zéros. Par exemple, charger une valeur de 32-bits dans `%rax` va forcer les 32 bits de poids fort à zéro même si la valeur est négative.
- `movslq`/`movsxd` sont nécessaire pour l'extension de signe 32→64 bits.
- Vous pouvez écrire `movq` pour charger une valeur immédiate de 8 octets (64 bits) dans un registre. Par contre, si vous dumpez le binaire obtenu via `objdump` vous verez que l'instruction s'est changée en `movabs`. C'est une particularité de la syntaxe AT&T, `movabs` est utilisée lors du chargement d'immédiats de 8 octets à la place de `movq`. C'est pour faire la différence entre le `mov` qui va charger des immédiats de 4 octets ou moins dans un register 8 octets en rajoutant des zéros, du `mov` qui charge réellement un immédiat de 8 octets.
:::

## Operations Mémoires
> `(%rdi)` veut dire la case mémoire pointée par `%rdi`. Autrement dit, on déréférence l'adresse stockée dans `%rdi`. Comparer avec `(%rdi)`, veut dire comparer avec la valeur dans la case mémoire `(%rdi)`.

| Instruction                                                               | Opération           | Taille | Description                                   |
| ------------------------------------------------------------------------- | ------------------- | ------ | --------------------------------------------- |
| [`stosb`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store `%al`        | 1Byte  | Charger `%al` dans `(%rdi)`                 |
| [`stosw`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store `%ax`*        | 2Bytes | Charger `%ax`* dans `(%rdi)`                 |
| [`stosd`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store `%eax`*       | 4Bytes | Charger `%eax`* dans `(%rdi)`                |
| [`stosq`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store `%rax`       | 8Bytes | Charger `%rax` dans `(%rdi)`                |
| [`scasb`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Byte           | 1Byte  | Comparer le byte `%al` avec `(%rdi)`        |
| [`scasw`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Word           | 2Bytes | Comparer le word `%ax`* avec `(%rdi)`        |
| [`scasd`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Double Word    | 4Bytes | Comparer le dword `%eax`* avec `(%rdi)`      |
| [`scasq`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Quad Word      | 8Bytes | Comparer le qword `%rax` avec dans `(%rdi)` |
| [`cmpsb`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Byte        | 1Byte  | Comparer `(%rsi)` avec `(%rdi)`             |
| [`cmpsw`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Word        | 2Bytes | Comparer `(%rsi)` avec `(%rdi)`             |
| [`cmpsd`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Double Word | 4Bytes | Comparer `(%rsi)` avec `(%rdi)`             |
| [`cmpsq`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Quad Word   | 8Bytes | Comparer `(%rsi)` avec `(%rdi)`             |
| [`movsb`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Byte           | 1Byte  | Copier `(%rsi)` dans `(%rdi)`               |
| [`movsw`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Word           | 2Bytes | Copier `(%rsi)` dans `(%rdi)`               |
| [`movsd`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Double Word    | 4Bytes | Copier `(%rsi)` dans `(%rdi)`               |
| [`movsq`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Quad Word      | 8Bytes | Copier `(%rsi)` dans `(%rdi)`               |

### Instructions MOVS et préfixes REP

<a href="https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq" target="_blank"> <code class=" docutils literal notranslate">movsb/movsw/movsd/movsq</code> </a> permet de copier une donnée d'une taille donnée (b:1 octet, w: 2 octets, d: 4 octets, q: 8 octets) depuis l'adresse spécifiée par le registre <strong>rsi</strong> vers l'adresse spécifiée par le registre <strong>rdi</strong>. Après chaque opération, ces registres sont automatiquement mis à jour pour pointer vers l'adresse suivante.
La nature de cette mise à jour est contrôlée par le flag de direction (**DF**) dans le registre **RFLAGS**. L'instruction <a href="https://www.felixcloutier.com/x86/cld" target="_blank"> <code class=" docutils literal notranslate">cld</code> </a> (Clear Direction Flag) configure le cpu à incrémenter **rsi** et **rdi**, permettant une copie vers l'avant. À l'inverse, <a href="https://www.felixcloutier.com/x86/std" target="_blank"> <code class=" docutils literal notranslate">std</code> </a>  (Set Direction Flag) les fait décrémenter pour une copie vers l'arrière.

Le préfixe <a href="https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz" target="_blank"> <code class=" docutils literal notranslate">rep</code> </a> transforme une simple instruction de copie en une puissante opération de copie en bloc. Il utilise le registre `%rcx` comme compteur et répète l'instruction autant de fois que spécifié. Par exemple, `rep movsb` copiera exactement `%rcx` octets de la source vers la destination.

Il existe également des variantes plus sophistiquées : REPE/REPZ et REPNE/REPNZ. Ces préfixes **ajoutent** une condition supplémentaire à la répétition(le `%rcx` est toujours utilisé comme compteur). REPE/REPZ continue tant que le flag zéro est actif, tandis que REPNE/REPNZ poursuit tant qu'il est inactif.

```nasm
memory_copy:
    ; Les paramètres suivent la convention System V AMD64 :
    ; rdi contient l'adresse de destination
    ; rsi contient l'adresse source
    ; rdx contient le nombre d'octets à copier
    
    movq %rdx, %rcx        ; Préparation du compteur
    cld                 ; Configuration pour copie vers l'avant
    rep movsb          ; Exécution de la copie
    ret
```


Pour résumer:

1. <a href="https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz" target="_blank"> <code class="docutils literal notranslate">rep</code></a> (Repeat) — Répétition inconditionnelle :
   - Répète l'instruction `%rcx`* fois.
   - Décrémente `%rcx`* après chaque itération.
   - Continue jusqu'à `%rcx = 0`.
   - Exemple : `rep movsb` effectue une copie mémoire de `%rcx`* octets depuis l'adresse dans `%rsi`* vers l'adresse dans `%rdi`.

2. <a href="https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz" target="_blank"> <code class=" docutils literal notranslate">repe/repz</code></a> (Repeat while Equal/Zero) — Répétition conditionnelle sur égalité :
   - Continue tant que **ZF = 1** (résultat égal/zéro) **ET** `%rcx > 0`.
   - S'arrête dès que **ZF = 0** (différence détectée) **OU** `%rcx = 0`.
   - Exemple : `repe cmpsb` compare deux chaînes octet par octet et s'arrête à la première différence.

3. <a href="https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz" target="_blank"> <code class=" docutils literal notranslate">repne/repnz</code></a> (Repeat while Not Equal/Not Zero) — Répétition conditionnelle sur inégalité :
   - Continue tant que **ZF = 0** (résultat différent/non-zéro) **ET** `%rcx > 0`.
   - S'arrête dès que **ZF = 1** (correspondance trouvée) **OU** `%rcx = 0`.
   - Exemple : `repne scasb` recherche **`%al`** dans une chaîne pointée par `%rdi`, s'arrête dès qu'il le trouve.

- Le flag **DF** (Direction Flag) contrôle le sens de parcours : si **DF = 0**, les registres d'adresses (`%rdi`, `%rsi`*) utilisés sont incrémentés ; si **DF = 1**, ils sont décrémentés. Dans le cas de `scasb` seulement `%rdi` est mis à jour, vu que `%rsi`* n'est pas utilisé.

Pour des copies de grande taille, il peut être plus efficace d'utiliser `movsd` ou `movsq` qui copient respectivement 4 ou 8 octets par opération. Voici une version optimisée qui traite les données par blocs de 4 octets :

```nasm
memory_copy_optimized:
    movq %rdx, %rcx
    shr $2, %rcx         ; Division par 4 pour utiliser movsd (4 octets)
    cld
    rep movsd          ; Copie principale par blocs de 4 octets
    
    movq %rdx, %rcx
    andq $3, %rcx         ; Récupération du reste (0,1,2 ou 3)
    rep movsb          ; Copie des octets restants
    ret
```

:::{admonition} Note sur la performance
:class: note
Bien que ces instructions soient optimisées au niveau du processeur, leur efficacité dépend du contexte. Pour de très petites copies (quelques octets), une simple séquence de `mov` peut s'avérer plus rapide. Pour de très grandes copies, les fonctions système comme memcpy, qui peuvent utiliser des instructions SIMD (Single Instruction Multiple Data) ou des optimisations spécifiques au processeur, sont souvent préférables.
:::