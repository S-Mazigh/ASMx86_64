---
title: Your Page Title 
index: true
---

# Les registres et l'adressage

## Registres en x86_64

- Il existe plusieurs types de registres dans l'architecture x86_64:
  - **General Purpose Registers**
  - **The pointer register**
  - **Flag Register**
  - *Control Registers*
  - Debug Registers
  - Model-Specific Register
  - XMM Registers
  - x87 Float registers (en pratique, les XMM registers les ont remplacés)
- On va principalement parler des deux premieres familles de registres.

### General Purpose Registers

- En x86_64 les registres généralistes ont une taille maximale de 64-bits (8 octets). Il existe 16 registres dans cette famille, dont certain ont une utilisation spécifique.
- Les registres sont : 
  - **RAX**, **RBX**, **RCX**, **RDX**: version 64-bits des registres: A, B, C, D.
  - **RBP**, **RSP**: version 64-bits des registres de gestion de la pile: BP(base pointer) et SP (stack pointer).
  - **RSI**, **RDI**: version 64-bits des registres pour la copie  de données: SI(source index) et DI(destination index).
  - **R8**,**R9**,**R10**,**R11**,**R12**,**R13**,**R14**,**R15**: registres 64-bits introduit avec l'architecture x86_64 (inexistant en architecture x86 32-bits).

- Ces registres peuvent être accédés de différentes manières, on peut faire en sorte d'accéder que certains octets des registres. 

- Pour commencer, on va examiner les registres traditionnels **(A,B,C,D)**. Comme le montrent les figures et code suivants, chaque nom permet de spécifier les octets à lire ou à écrire.

```nasm
; source:
.global main

main:
    movabsq $0x71ff9b005c4e258a, %rax
    movl %eax, %ebx
    movb $0x41, %ah
    movb $0x41, %al
    movw $0x51, %ax
    movl $0x41, %eax
    movq $0x51, %rax
    movw %ax, %bx
    ret

; compilé (objdump):
;main:
;    1129:	48 b8 8a 25 4e 5c 00 	movabs $0x71ff9b005c4e258a,%rax
;    1130:	9b ff 71 
;    1133:	89 c3                	mov    %eax,%ebx
;    1135:	b4 41                	mov    $0x41,%ah
;    1137:	b0 41                	mov    $0x41,%al
;    1139:	66 b8 51 00          	mov    $0x51,%ax
;    113d:	b8 41 00 00 00       	mov    $0x41,%eax
;    1142:	48 c7 c0 51 00 00 00 	mov    $0x51,%rax
;    1149:	66 89 c3             	mov    %ax,%bx
;    114c:	c3                   	ret   
```

<center>
<iframe class="slideshow-iframe" id="execution-registers" src="./_static/slides/register-sequence.html"
frameborder="0" scrolling="no"></iframe>
</center>

> - On remarque que les deux instructions `movl $0x41, %eax` et `movq $0x51, %rax` se comportent exactement de la même manière dans ce cas de figure. Tout en ayant des tailles différentes: la version avec `%eax` utilisant 2 octets de moins.
> - Pour des raisons de performances de calculs en 32-bits (comme expliqué <a href="https://stackoverflow.com/questions/11177137/why-do-x86-64-instructions-on-32-bit-registers-zero-the-upper-part-of-the-full-6" target="_blank">ici</a>) amd a fait en sorte de forcer les 32-bits de poids fort à zéro.
> - **Retenez juste que les instructions sur les 32-bits de poids faible forcent implicitement les 32-bits de poids fort d'un registre 64-bits à zéro.**

- Les autres registres hérités **(SI,DI,SP,BP)** ne permettent pas d'accéder à leur deuxième octet comme les registres **(A,B,C,D)**. 

<center><div  class="figure-container-small"><figure>
    <img src="./_static/images/register-sp.png" class="figure">
    <figcaption>Les différentes manières d'accéder au registre <strong>%rsp</strong>.</figcaption>
</figure></div></center>

- Pour les nouveaux registres de l'architecture x86_64 **(R8,R9,R10,R11,R12,R13,R14,R15)** on utilise plutôt des suffixes pour spécifier la taille à lire ou à écrire.


<center><div  class="figure-container-small">
<figure>
    <img src="./_static/images/register-8.png" alt="Register 8 calling convention" class="figure">
    <figcaption>Registre 8 de l'architecture x86_64.</figcaption>
</figure>
</div></center>

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://wiki.osdev.org/CPU_Registers_x86-64">https://wiki.osdev.org/CPU_Registers_x86-64</a></li>
<li><a href="https://stackoverflow.com/questions/26280229/is-x87-fp-stack-still-relevant">https://stackoverflow.com/questions/26280229/is-x87-fp-stack-still-relevant</a></li>
</ul>
</blockquote>

### Le Registre RIP

- Le pointer register **RIP** contient l'**adresse** mémoire où la prochaine instruction à exécuter est située. Comme vous pouvez le voir dans les captures suivantes, quand le CPU fini d'exécuter l'instruction <a href="https://sourceware.org/binutils/docs/as/i386_002dVariations.html" target="_blank"><code class=" docutils literal notranslate">movabs</code></a> qui est à l'adresse `0x5129` la valeur de `%rip` est l'adresse de l'instruction suivante `mov %eax, %ebx` à l'adresse `0x5133`.

<center><div  class="figure-container"><figure>
    <img src="./_static/images/rip-1.png" class="figure2">
  <img src="./_static/images/rip-2.png" class="figure2">
    <figcaption>La valeur du <strong>%rip</strong> est calculée lors de l'exécution d'une instruction.</figcaption>
</figure></div></center>

- Il faut que vous sachiez que les instructions ont des tailles différentes. Elles varient de `1 octets` jusqu'à `15 octets`. Étant donné qu'en mémoire les données sont stockés par octets. Durant la lecture d'un octet de l'instruction le CPU sait s'il doit interpréter le prochain octet comme faisant partie de cette même instruction grâce aux octets qu'il a déja décodés.

- Les instructions d'appel et de branchement `jmp`, `call`, `ret`, ... ne font que modifier la valeur de ce fameux registre `%rip`, en d'autres termes elles changent l'adresse de la prochaine instruction.

### Résumé sur les registres

<center class="table-wrapper"><table align="center" cellpadding="7px" cellspacing="0" border="2">
<tbody><tr class="header-row">
   <th>64-bits</th>
   <th>32-bits</th>
   <th>16-bits</th>
   <th>8-bits</th>
   <th>Utilisation dans l'ABI Linux AMD64</th>
   <th>Appel de fonction</th>
</tr>
<tr class="green-row">
   <td>rax</td><td>eax</td><td>ax</td><td>ah,al</td>
      <td>Valeur de retour</td>
      <td>Peut être modifié par la fonction appelée</td>
</tr>   
<tr class="red-row">
   <td>rbx</td><td>ebx</td><td>bx</td><td>bh,bl</td>
      <td>&nbsp;</td>
      <td>Doit être sauvegardé par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rcx</td><td>ecx</td><td>cx</td><td>ch,cl</td>
      <td>4<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rdx</td><td>edx</td><td>dx</td><td>dh,dl</td>
      <td>3<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rsi</td><td>esi</td><td>si</td><td>sil</td>
      <td>2<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rdi</td><td>edi</td><td>di</td><td>dil</td>
      <td>1<sup>er</sup>argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="red-row">
   <td>rbp</td><td>ebp</td><td>bp</td><td>bpl</td>
      <td>Début d'une stack frame</td>
      <td>Faire extrêmement attention à son utilisation et à sa sauvegarde</td>
</tr>   
<tr class="red-row">
   <td>rsp</td><td>esp</td><td>sp</td><td>spl</td>
      <td>La fin de la pile (top of stack)</td>
      <td>Faire extrêmement attention à son utilisation et à sa sauvegarde</td>
</tr>
<tr class="green-row">
   <td>r8</td><td>r8d</td><td>r8w</td><td>r8b</td>
      <td>5<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>
<tr class="green-row">
   <td>r9</td><td>r9d</td><td>r9w</td><td>r9b</td>
      <td>6<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>
<tr class="green-row">
   <td>r10</td><td>r10d</td><td>r10w</td><td>r10b</td>
      <td>&nbsp;</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>
<tr class="green-row">
   <td>r11</td><td>r11d</td><td>r11w</td><td>r11b</td>
      <td>&nbsp;</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>
<tr class="red-row">
   <td>r12</td><td>r12d</td><td>r12w</td><td>r12b</td>
      <td>&nbsp;</td>
      <td>Doit être sauvegardé par la fonction appelée</td>
      
</tr>
<tr class="red-row">
   <td>r13</td><td>r13d</td><td>r13w</td><td>r13b</td>
      <td>&nbsp;</td>
      <td>Doit être sauvegardé par la fonction appelée</td>
      
</tr>
<tr class="red-row">
   <td>r14</td><td>r14d</td><td>r14w</td><td>r14b</td>
      <td>&nbsp;</td>
      <td>Doit être sauvegardé par la fonction appelée</td>
      
</tr>
<tr class="red-row">
   <td>r15</td><td>r15d</td><td>r15w</td><td>r15b</td>
      <td>&nbsp;</td>
      <td>Doit être sauvegardé par la fonction appelée</td>
      
</tr>
</tbody></table></center>


:::{important}
- Quand vous appelez une fonction il **ne faut pas** vous attendre à ce que les registres en **vert** aient gardé leur valeur. Autrement dit, si votre programme assembleur utilise le registre `%rdx` il faut qu'il soit sauvegardé (`pushq %rdx`) avant l'appel `call my_func` et puis restauré après l'appel (`popq %rdx`).
- Par contre si une fonction veut utiliser un des registres en **rouge**, elle doit le sauvegarder avant sa modification et le restaurer avant le retour (`ret`).
:::

Le document sur l'ABI AMD64 (section **3.2.3 Parameter Passing**)  présente dans un tableau plus complet sur l'utilisation de chaque registre. Les sources latex officielles sont sur [gitlab](https://gitlab.com/x86-psABIs/x86-64-ABI), vous trouverez un lien pour télécharger le pdf dans le README.

```nasm
my_func:
   pushq %rbx ; sauvegarde %rbx
   pushq %r14 ; sauvegarde %r14
   ; ...
   movq %rdi, %rbx ; modifie %rbx
   ; ...
   movq (%rbx), %r14 ; modifie %r14
   ; ...
   addq %r14, %edx ; modifie %rax
   ; ...
   popq %r14 ; restaure %r14
   popq %rbx ; restaure %rbx
   ret

main:
   ; ...
   movabs $4523902, %rbx
   movl $125, %edx ; utilise %eax
   movl $45, %edi
   pushl %edx
   call my_func
   ; %edx a été changé par my_func
   movl %edx, (%rbx) ; la valeur de %rbx est maintenue par my_func
   ; maintenant, j'ai besoin de mon %edx
   popl %edx
   movl %edx, 4(%rbx) ; la valeur initiale de %edx est écrite en adresse mémoire %rbx + 4
   ; ...
   ret
   
```

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://wiki.osdev.org/Calling_Conventions" target="_blank">https://wiki.osdev.org/Calling_Conventions</a></li>
<li><a href="https://math.hws.edu/eck/cs220/f22/registers.html" target="_blank">https://math.hws.edu/eck/cs220/f22/registers.html</a></li>
</ul>
</blockquote>

## Les flags et le registre RFLAGS en x86_64

- Lors de l'exécution de certaines instructions, il est intéressant de garder certaines informations sur le résultat de ces dernières, pour rendre certaines instructions inter-dépendantes. Par exemple, si on veut additionner des nombres de taille supérieure à 64-bits, disons 128-bits il est primordial de savoir si l'addition des 64-bits de poids faible a généré une retenue pour le 65ème bit pour avoir un résultat correct (<a href="https://www.felixcloutier.com/x86/adc" target="_blank"><code class=" docutils literal notranslate">adc</code></a>). Il existe plein d'autres cas autre que les jump, où l'on veut avoir des informations sur le résultat de l'instruction précédente.

### Le registre RFLAGS : structure et évolution

- En x86_64, on a à notre disposition le registre **RFLAGS** pour stocker et accéder aux informations décrivant la nature du résultat d'une instruction. En x86(32 bits), le registre se nommait **EFLAGS** et à l'âge de l'architecture 16-bits **FLAGS**. Vous pouvez voir comment ce registre fut étendue avec le changements d'architecture dans la figure ci-dessous.
  - En pratique, le registre RFLAGS décrit aussi des restrictions d'exécution, ainsi une instruction va changer son comportement, voir lever une exception si des restrictions sont actives.

<center><div  class="figure-container"><figure>
    <img src="./_static/images/RFLAGS.png" alt="RFLAGS" class="figure">
    <figcaption>Structure complète du registre RFLAGS.</figcaption>
</figure></div></center>

- Lors du développement de l'architecture, les ingénieurs ont dû choisir quelles informations garder sur le résultat d'une instruction. Pour optimiser un maximum la mémoire, tout en gardant l'utilisation simple, ils se sont limité à un seul registre. Chaque **bit** du registre indique la présence ou l'absence d'un flag relié à un état. Les bits vides sont réservés, Intel et AMD les utilisent comme ils veulent.

#### Les différents types de flags

- Les flags sont divisés en **3** groupes:
  - <span style="color: rgba(91, 163, 233);">Status Flags:</span> 
    - **CF**(Carry Flag): **1** s'il y a eu une retenue au-delà du bit de poids fort du résultat, sinon **0**.
    - **PF**(Parity Flag): **1** si le nombre de bits à 1 dans les 8-bits de poids faible est pair, **0** si impair.
    - **AF**(Auxiliary Carry Flag): **1** s'il y a eu une retenue depuis le bit 3 vers le bit 4, sinon **0**.
    - **ZF**(Zero Flag): **1** si le résultat est nul, sinon **0**.
    - **SF**(Sign Flag): **1** si le résultat est négatif, sinon **0**.
    - **OF**(Overflow Flag): **1** si le résultat d'une opération signée dépasse la capacité du registre (changement de signe inattendu), sinon **0**.
  - <span style="color: rgba(200, 80, 200);">Control Flags:</span>
    - **IF**(Interrupt Flag): **1** si les interruptions sont actives, **0** si désactivées.
    - **DF**(Direction Flag): **1** pour que les adresses soient décrementées lors des instructions iteratives (<a href="https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz" target="_blank"><code class=" docutils literal notranslate">rep</code></a>), **0** pour les incrémenter.
    - **TF**(Trap Flag): **1**  pour appeler une fonction après chaque instruction permettant d'avoir une exécution pas à pas (debug), **0** pour une exécution classique.
  - <span style="color: rgba(233, 100, 100);">System Flags:</span>
    - **IOPL**(I/O privilege level).
    - ...

#### Mécanismes de mise à jour des flags
- La mise à jour des flags nécessite des tests et des écritures, cela prend du temps. Pour ne pas en perdre inutilement, les ingénieurs ont fait en sorte que certaines instructions ne touchent pas aux flags (le `mov` par exemple). Et même les instructions mettant à jour les flags, ne touchent pas à tous les flags, seulement ceux nécessaires. Entre autres, l'instruction `add` ne met à jour que les **status flags**.
   - En général, on dit que les instructions qui ne font **que** **déplacer** des données ne modifient pas les flags. Par contre, celles qui **effectuent** des **calculs** mettent à jour les flags nécessaires.
   - Il existe certaines exceptions d'instructions qui calculent mais ne mettent pas à jour les flags, parmi elles : <a href="https://www.felixcloutier.com/x86/not" target="_blank"><code class=" docutils literal notranslate">not</code></a> et <a href="https://www.felixcloutier.com/x86/lea" target="_blank"><code class=" docutils literal notranslate">lea</code></a>.

#### Instructions de manipulation des flags
- Il est possible d'accéder au registre **RFLAGS** via des instructions spéciales : 
  - <a href="https://www.felixcloutier.com/x86/lahf" target="_blank"><code class=" docutils literal notranslate">lahf</code></a> enregistre les 8-bits de poids faibles de **FLAGS** dans **ah**. <a href="https://www.felixcloutier.com/x86/sahf" target="_blank"><code class=" docutils literal notranslate">sahf</code></a> récupère les valeurs de **SF**, **ZF**, **AF**, **PF**, et **CF** (les 8-bits de poids faible) depuis **ah**.
  - <a href="https://www.felixcloutier.com/x86/clc" target="_blank"><code class=" docutils literal notranslate">clc</code></a> (mettre CF à 0), <a href="https://www.felixcloutier.com/x86/stc" target="_blank"><code class=" docutils literal notranslate">stc</code></a> (mettre CF à 1), <a href="https://www.felixcloutier.com/x86/cmc" target="_blank"><code class=" docutils literal notranslate">cmc</code></a> (inverser CF), <a href="https://www.felixcloutier.com/x86/cli" target="_blank"><code class=" docutils literal notranslate">cli</code></a> (mettre IF à 0), <a href="https://www.felixcloutier.com/x86/sti" target="_blank"><code class=" docutils literal notranslate">sti</code></a> (mettre IF à 1), <a href="https://www.felixcloutier.com/x86/cld" target="_blank"><code class=" docutils literal notranslate">cld</code></a> (mettre DF à 0), <a href="https://www.felixcloutier.com/x86/std" target="_blank"><code class=" docutils literal notranslate">std</code></a> (mettre DF à 1).

- L'instruction `cmp i1, i2` fait une soustraction `i2 - i1` sans sauvegarder le résultat dans l'opérant destination et met à jour les flags **CF**, **OF**, **SF**, **ZF**, **AF**, et **PF**.
- L'instruction `test i1, i2` fait un bit-wise AND `i2 & i1` et met à jour les flags **PF**, **SF**, **ZF**. Entre autres, elle permet de tester si un registre est nul `testq %rax, %rax`, en étant plus compacte que `cmp $0, %rax`.
- Les instructions de la famille <a href="https://www.felixcloutier.com/x86/jcc" target="_blank"><code class=" docutils literal notranslate">jcc</code></a> vérifient les flags pour charger l'adresse spécifiée dans le registre **rip** ou pas (**rip** pointe vers l'instruction suivante).

:::{admonition} pushf et popf
:class: dropdown
<a href="https://www.felixcloutier.com/x86/pushf:pushfd:pushfq" target="_blank"><code class=" docutils literal notranslate">pushf</code>/<a href="https://www.felixcloutier.com/x86/popf:popfd:popfq" target="_blank"><code class=" docutils literal notranslate">popf</code></a> empile/dépile le registre **RFLAGS** sur/depuis la pile d'une certaine manière. Les descriptions de `pushf` et `popf` expliquent plus en détails les restrictions de ces instructions. En se limitant à l'architecture 64-bits, on a:
- Les flags `VM` et `RF` ne sont jamais push, ils sont toujours forcés à zéro. 
 - Par défaut, l'instruction (mnemonic) `pushfq` empile les 8 octets de **RFLAGS**. Et on écrit `pushf` pour empiler que les 2 octets **FLAGS**. Il est impossible d'empiler que les 4 octets **EFLAGS**. Même si les instructions ont le même opcode `0x9C`, le préfixe `0x66` permet de passer en mode 16-bits.
   - Malheureusement, un différent assembleur peut ne pas séparer les deux mnemonics `pushf` et `pushfq`.
- Pour ce qui est de `popf`, le cpu va mettre à jour **RFLAGS** en rapport à son mode actuel [Table 4-16](https://www.felixcloutier.com/x86/popf:popfd:popfq#tbl-4-16).
:::

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://fr.wikibooks.org/wiki/Programmation_Assembleur/x86/Les_flags" target="_blank">https://fr.wikibooks.org/wiki/Programmation_Assembleur/x86/Les_flags</a></li>
<li><a href="https://en.wikipedia.org/wiki/FLAGS_register" target="_blank">https://en.wikipedia.org/wiki/FLAGS_register</a></li>
</ul>
</blockquote>

<!-- http://ref.x86asm.net/coder64.html -->

## Les modes d'adressage

Commençons par le commencement : l'adressage, c'est tout simplement la façon dont on dit au processeur "hé, va chercher/mettre cette donnée à tel endroit !".

### Modes Directs

#### 1. Mode d'adressage immédiat

Le mode le plus simple, c'est l'adressage immédiat. Imaginez que vous dites directement "le nombre c'est 42". Pas besoin de chercher ailleurs, la valeur est directement dans l'instruction. C'est comme écrire une constante dans du code C ou autre.


```nasm
; AT&T
movq $42, %rax    ; Charge la valeur 42 dans rax
addq $10, %rbx    ; Ajoute 10 à rbx
```

#### 2. Mode d'adressage par registre

L'adressage par registre utilise directement les registres du processeur pour stocker et manipuler les données. C'est le mode d'accès le plus rapide, car les registres sont intégrés au cœur du CPU. Ils constituent un espace de stockage limité mais immédiatement accessible, similaire à des variables globales en C, mais en nombre fixe et restreint.


```nasm
; AT&T
movq %rbx, %rax    ; Copie rbx dans rax
xorq %rax, %rax    ; Mise à zéro rapide de rax
```

#### 3. Mode d'adressage mémoire direct

Maintenant, parlons de l'adressage mémoire direct, ce mode utilise une adresse mémoire fixe. Vous dites au processeur "va chercher ce qu'il y a à l'adresse 0x1234". C'est utile pour accéder à des variables globales ou des constantes dont on connait l'adresse à la compilation (pas de `malloc`).


```nasm
; AT&T
movq value, %rax      ; Charge depuis l'adresse 'value'
movq %rbx, target     ; Stocke dans l'adresse 'target'
```


### 4. Modes Indirects

Les choses deviennent plus intéressantes avec l'adressage indirect. Ici l'adresse qu'on cherche à accéder n'est pas directement accessible, soit une lecteur ou un calcul sont nécessaires.

#### 1. Mode d'adressage indirect par registre

L'adressage indirect peut utiliser un registre comme pointeur vers la mémoire. Au lieu de dire "va à telle adresse", on dit "va à l'adresse qui est stockée dans ce registre". C'est la base de la manipulation des pointeurs.


```nasm
; AT&T
movq (%rbx), %rax     ; Charge depuis l'adresse contenue dans rbx
movq %rax, (%rcx)     ; Stocke à l'adresse contenue dans rcx
```

#### 2. Mode d'adressage avec déplacement

Ce mode combine un registre et un déplacement pour calculer l'adresse finale. Parfait pour les tableaux et structures.


```nasm
; AT&T
movq 10(%rbx), %rax      ; Adresse = rbx + 10
movq %rax, 18(%rbx)      ; Stocke à rbx + 18
```

#### 3. Mode d'adressage RIP-relative

Le mode d'adressage RIP-relative est spécifique à l'architecture x86-64. Ce mode est fondamental pour le Position Independent Code (PIC). Les adresses sont calculées relativement à la position courante du pointeur d'instruction (**rip**), permettant au code d'être chargé à n'importe quelle adresse en mémoire virtuelle sans nécessiter de relocation. C'est une technique fondamentale pour les bibliothèques partagées. L'assembler (ex:`gnu as` ou `nasm`) et le linker se charge de calculer le deplacement et le mettre dans le code machine finale.

```nasm
; 1. Déplacement constant :
; AT&T
movq 1234(%rip), %rax    ; Accède à l'adresse rip+1234
                         ; (1234 octets après la fin de l'instruction courante, i.e le début de l'instruction suivante)
; 2. Symboles :
; AT&T
movq symbol(%rip), %rax  ; Accède au symbole de manière relative
                         ; Plus efficace et plus compact que l'adressage absolu 

```


:::{important}
En syntaxe AT&T, pour les instructions de contrôle de flux (`jmp`, `call`), le préfixe `*` distingue l'adressage absolu de l'adressage relatif :
```nasm
; AT&T
jmp label        ; Adressage relatif à rip
jmp *label       ; Adressage absolu : utilise l'adresse fixe de 'label'
call *%rax       ; Appel indirect : utilise l'adresse contenue dans rax
```

Sans `*`, le code machine encode un **déplacement relatif** depuis rip (plus compact, position-independent). Avec `*`, il encode une **adresse absolue** (nécessaire pour les sauts indirects).
:::

#### 4. Mode d'adressage base + index + échelle + déplacement

Le mode le plus complet, permettant des calculs d'adresse complexes.

```nasm
; AT&T
; Format général : déplacement(base,index,échelle)

movq 8(%rbx,%rcx,4), %rax    ; déplacement=8, base=rbx, index=rcx, échelle=4
                             ; Adresse = rbx + (rcx*4) + 8

movq 8(%rbx,%rcx), %rax      ; déplacement=8, base=rbx, index=rcx, échelle=1 (implicite)
                             ; Adresse = rbx + (rcx*1) + 8

movq (%rbx,%rcx), %rax       ; déplacement=0 (omis), base=rbx, index=rcx, échelle=1 (implicite)
                             ; Adresse = rbx + (rcx*1)
```

:::{admonition} Notes sur la performance
:class: note
- Les modes impliquant des accès mémoire sont généralement plus lents
- L'utilisation de l'échelle peut ajouter des cycles supplémentaires
- Les registres sont toujours les mémoires les plus rapides à lire et à écrire.
:::

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://sourceware.org/binutils/docs/as/i386_002dMemory.html
" target="_blank">https://sourceware.org/binutils/docs/as/i386_002dMemory.html</a>
</blockquote>