# Table des matières
- [Table des matières](#table-des-matières)
- [1. Les bases](#1-les-bases)
  - [1.1. Notes importantes](#11-notes-importantes)
  - [1.2. Registres en x86\_64](#12-registres-en-x86_64)
    - [1.2.1. General Purpose Registers](#121-general-purpose-registers)
    - [1.2.2. Pointer Register (RIP)](#122-pointer-register-rip)
    - [1.2.3. Résumé sur les registres](#123-résumé-sur-les-registres)
  - [1.3. Les flags en x86\_64](#13-les-flags-en-x86_64)
  - [1.4. Stack frame](#14-stack-frame)
  - [1.5. Appeler les fonctions de la libc](#15-appeler-les-fonctions-de-la-libc)
    - [1.5.1. Fonction simple](#151-fonction-simple)
    - [1.5.2. Fonction variadic (nombre d'arguments dynamique)](#152-fonction-variadic-nombre-darguments-dynamique)
  - [1.6. Syscalls en assembleur](#16-syscalls-en-assembleur)
- [2. Svartalfheim](#2-svartalfheim)
  - [2.1. Rex prefix](#21-rex-prefix)
  - [2.2. L'ordre d'exécution](#22-lordre-dexécution)


# 1. Les bases

## 1.1. Notes importantes

> `movabs` est un `mov` qui ne peut utiliser que des immédiats et des registers (pas d'adresse mémoire), par contre il peut utiliser des immédiats de 64 bits.



## 1.2. Registres en x86_64

- Il existe plusieurs types de registres dans l'architecture x86_64:
  - **General Purpose Registers**
  - **The pointer register**
  - *Control Registers*
  - Debug Registers
  - Model-Specific Register
  - XMM Registers
  - Float registers (en pratique XMM registers les ont remplacés)
- On va principalement parler des deux premieres familles de registres.

### 1.2.1. General Purpose Registers

- En x86_64 les registres généralistes ont une taille maximale de 64-bits (8 octets). Il existe 16 registres dans cette famille, dont certain ont une utilisation spécifique.
- Les registres sont : 
  - **rax**, **rbx**, **rcx**, **rdx**: version 64-bits des registres: A, B, C, D.
  - **rbp**, **rsp**: version 64-bits des registres de gestion de la pile: BP(base pointer) et SP (stack pointer).
  - **rsi**, **rdi**: version 64-bits des registres pour la copie  de données: SI(source index) et DI(destination index).
  - **r8**,**r9**,**r10**,**r11**,**r12**,**r13**,**r14**,**r15**: registres 64-bits introduit avec l'architecture x86_64 (inexistant en architecture x86 (32-bits)).

- Les registres hérités de l'architecture x86 **(A,B,C,D)** peuvent être accédés de différentes manières, on peut faire en sorte d'accéder que certains octets des registres. 

- Comme le montrent les figures et code suivants, chaque nom permet de spécifier les octets à lire ou à écrire (sachez qu'il y existe une différence de comportement pour les versions 32-bits et 64-bits, même si à premiere vue elles paraissent equivalentes):

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

; compilé:
main:
    1129:	48 b8 8a 25 4e 5c 00 	movabs $0x71ff9b005c4e258a,%rax
    1130:	9b ff 71 
    1133:	89 c3                	mov    %eax,%ebx
    1135:	b4 41                	mov    $0x41,%ah
    1137:	b0 41                	mov    $0x41,%al
    1139:	66 b8 51 00          	mov    $0x51,%ax
    113d:	b8 41 00 00 00       	mov    $0x41,%eax
    1142:	48 c7 c0 51 00 00 00 	mov    $0x51,%rax
    1149:	66 89 c3             	mov    %ax,%bx
    114c:	c3                   	ret   
```

<center><figure>
	<img src="./images/register-a-1.png" class="figure">
	<figcaption>Charger le registre <strong>%rax</strong> avec une valeur immédiate de 64-bits.</figcaption>
</figure></center>

<center><figure>
	<img src="./images/register-a-2.png" class="figure">
	<figcaption>Charger que les 32-bits de poids faibles de <strong>%rax</strong> dans <strong>%rbx</strong> qui remplira le reste avec des <em>zéros</em>.</figcaption>
</figure></center>

<center><figure>
	<img src="./images/register-a-3.png" class="figure">
	<figcaption>Modifier que le deuxième octet de <strong>%rax</strong>.</figcaption>
</figure></center>

<center><figure>
	<img src="./images/register-a-4.png" class="figure">
	<figcaption>Modifier que le premier octet de <strong>%rax</strong>.</figcaption>
</figure></center>

<center><figure>
	<img src="./images/register-a-5.png" class="figure">
	<figcaption>Modifier que les deux premiers octets (16-bits) de <strong>%rax</strong>.</figcaption>
</figure></center>


<center><figure>
	<img src="./images/register-a-6.png" class="figure">
	<figcaption>Modifier les quatre premiers octets (32-bits) de <strong>%rax</strong> tout en rajoutant des **zéros** jusqu'au 64ème bit.</figcaption>
</figure></center>


<center><figure>
	<img src="./images/register-a-7.png" class="figure">
	<figcaption>Modifier tous les huit octets (64-bits) de <strong>%rax</strong> en rajoutant des zéros s'il le faut.</figcaption>
</figure></center>


<center><figure>
	<img src="./images/register-a-8.png" class="figure">
	<figcaption>Charger les deux premiers octets de <strong>%rax</strong> dans <strong>%rbx</strong>.</figcaption>
</figure></center>

- Les autres registres hérités **(SI,DI,SP,BP)** ne permettent pas d'accéder leur deuxième octet. 

<center><figure>
	<img src="./images/register-sp.png" class="figure">
	<figcaption>Les différentes manières d'accéder au registre <strong>%rsp</strong>.</figcaption>
</figure></center>

- Pour les nouveaux registres de l'architecture x86_64 **(r8,r9,r10,r11,r12,r13,r14,r15)** on utilise plutôt des suffixes pour spécifier la taille à lire ou à écrire.

<figure>
<center>
	<img src="./images/register-8.png" alt="Register 8 calling convention" class="figure">
	<figcaption>Registre 8 de l'architecture x86_64.</figcaption>
</center>
</figure>

> - On remarque que les deux instructions `movl $0x41, %eax` et `movq $0x51, %rax` se comportent exactement de la même maniére dans ce cas de figure, tout en ayant des tailles différentes: la version avec `%eax` utilisant 2 octets de moins.
> - Pour des raisons de performances de calculs en 32-bits (comme expliqué [ici](https://stackoverflow.com/questions/11177137/why-do-x86-64-instructions-on-32-bit-registers-zero-the-upper-part-of-the-full-6)) amd a fait en sorte de forcer les 32-bits de poids fort à zéro.
> - **Retenez juste que les instructions 32-bits forcent les 32-bits de poids fort à zéro.**

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://wiki.osdev.org/CPU_Registers_x86-64">https://wiki.osdev.org/CPU_Registers_x86-64</a></li>
<li><a href="https://stackoverflow.com/questions/26280229/is-x87-fp-stack-still-relevant">https://stackoverflow.com/questions/26280229/is-x87-fp-stack-still-relevant</a></li>
</ul>
</blockquote>

### 1.2.2. Pointer Register (RIP)

- Le pointer register contient l'**adresse** mémoire ou la prochaine instruction à exécuter est située. Comme vous pouvez le voir dans les captures suivantes, quand le CPU fini d'exécuter l'instruction `movabs` qui est à l'adresse `0x5129` la valeur de **rip** est l'adresse de l'instruction suivante `mov %eax, %ebx` à l'adresse `0x5133`.

<center><figure>
	<img src="./images/rip-1.png" class="figure">
  <img src="./images/rip-2.png" class="figure">
	<figcaption>La valeur du <strong>%rip</strong> est calculée lors de l'exécution d'une instruction.</figcaption>
</figure></center>

- Il faut que vous sachiez que les instructions ont des tailles différentes. elles varient de `1 octets` jusqu'à `15 octets`. Vu qu'en mémoire les données sont stockés par octets, durant la lecture d'un octet de l'instruction le CPU sait s'il doit interpréter les prochains octets comme faisant partie de cette même instruction grâce aux octets qu'il a déja décodés.

- Les instructions d'appel et de branchement `jmp, call, ret, ...` ne font que modifier la valeur de ce fameux registre **%rip**, en d'autres termes elles changent l'adresse de la prochaine instruction.

### 1.2.3. Résumé sur les registres

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
      <td>4<sup>th</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rdx</td><td>edx</td><td>dx</td><td>dh,dl</td>
      <td>3<sup>rd</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rsi</td><td>esi</td><td>si</td><td>sil</td>
      <td>2<sup>e</sup> argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="green-row">
   <td>rdi</td><td>edi</td><td>di</td><td>sil</td>
      <td>1<sup>er</sup>argument entier</td>
      <td>Peut être modifié par la fonction appelée</td>
      
</tr>   
<tr class="red-row">
   <td>rbp</td><td>ebp</td><td>bp</td><td>bpl</td>
      <td>Début d'une stack frame</td>
      <td>Bien faire attention à son utilisation et à sa sauvegarde</td>
</tr>   
<tr class="red-row">
   <td>rsp</td><td>esp</td><td>sp</td><td>spl</td>
      <td>La fin de la pile (top of stack)</td>
      <td>Extrêmement faire attention à son utilisation et à sa sauvegarde</td>
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


:pencil: **Remarques:**
- Quand vous appelez une fonction il **ne faut pas** vous attendre à ce que les registres en **vert** aient gardé leur valeur. Autrement dit, si votre programme assembleur utilise le registre `%rdx` il faut qu'il soit sauvegardé (`pushq %rdx`) avant l'appel `call my_func` et puis restauré après l'appel (`popq %rdx`).
- Par contre si une fonction veut utiliser un des registres en **rouge**, elle doit le sauvegarder avant sa modification et le restaurer avant le retour (`ret`).

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
<li><a href="https://wiki.osdev.org/Calling_Conventions">https://wiki.osdev.org/Calling_Conventions</a></li>
<li><a href="https://math.hws.edu/eck/cs220/f22/registers.html">https://math.hws.edu/eck/cs220/f22/registers.html</a></li>
</ul>
</blockquote>

## 1.3. Les flags en x86_64

- Les instructions `mov` ne modifient pas les flags.
- L'instruction test est ... , permet de ...
- L'instruction cmp est tout simplement une soustraction sans sauvegarde du résultat. Elle permet de ...



## 1.4. Stack frame

> parler d'enter et de leave
> https://stackoverflow.com/questions/72649142/difference-between-amd64-and-intel-x86-64-stack-frame

## 1.5. Appeler les fonctions de la libc

### 1.5.1. Fonction simple

### 1.5.2. Fonction variadic (nombre d'arguments dynamique)
> printf
> sinces variadics takes any type of arguments, it is hard to know how much registers to save when calling it, saving XMM registers is too expensive to do it each time, thus %al is used to store the number of vector registers

## 1.6. Syscalls en assembleur
(based on page 124 of the linux amd64 ABI : https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
- Dans les instructions du programme **safe** vous avez découvert l'instruction `syscall`. Si vous lisez la description de l'instruction dans le manuel d'intel, vous trouverez la phrase *"Fast call to privilege level 0 system procedures."*. Ils la décrivent comment étant rapide, cela est en rapport à l'ancienne implémentation ou le syscall était une interruption lambda et le CPU devait vérifier le type de l'interruption à chaque fois.
- Sinon pour faire court, c'est l'instruction assembleur utilisée pour faire appel à un syscall défini par l'OS qui va s'exécuter en mode Kernel (d'où le privilege level 0).
- Vous remarquerez que plusieurs registres sont initialisés avant d'instruction syscall.
<center><figure>
<img src="./images/syscalls.png"/>
<figcaption>Illustration expliquant l'utilisation d'un syscall</figcaption>
</figure></center>

- Le syscall retournera une valeur de retour dans `%rax` comme le font toutes les autres fonctions. En cas d'erreur, la valeur de retour est comprise dans l'intervalle **[-4095,-1]**, chacune pouvant être traduite en un code d'erreur de type **errno**. Pour vérifier si le syscall retourne une erreur en assembleur on utilise les deux instructions suivantes:

```nasm
   cmp $-4095, %rax
   jae errorSyscall
```

- L'instruction `jae` vérifie si la valeur **non signée** dans `%rax` est supérieur ou égale à la valeur **non-signée** de `-4095`.
- En 64-bits (**0b** veut dire nombre binaire):
  -  **-4095**  = 0b**1**111111111111111111111111111111111111111111111111111**00000000000**1 = 184467440737095**47521**
  -  **-1**     = 0b**1**111111111111111111111111111111111111111111111111111**11111111111**1 = 184467440737095**51615**
  -  **0**      = 0b**0**000000000000000000000000000000000000000000000000000000000000000 = **0**
- Les nombres négatifs commencent tous par **1** les rendant supérieurs aux nombre positifs quand on les compare en utilisant leurs valeurs **non signées**. Ajoutant à cela le fait que les representations négatives ont leur valeur **non signée** croître quand on se rapproche de **0**. 
- Avec ces deux notions, il devient clair que l'instruction `jae` ne saute que si la valeur de `%rax` est en dehors de l'intervale **[-4095,-1]**.
  - Si `%rax` a une valeur non signée **inférieure** à celle de **-4095**, cela voudra dire qu'il est soit **positif**, **0**, ou bien, **négatif** avec une valeur **signée** **inférieur** à **-4095**.
  - Autrement, sa valeur non signée sera **égale** ou **supérieure** à celle de **-4095**, avec comme maximum celle de **-1** (que des 1).
- Pour voir les différents syscalls disponible sur le kernel linux pour l'architecture x86-64, regardez [cette page github](https://github.com/torvalds/linux/blob/master/arch/x86/entry/syscalls/syscall_64.tbl). Et pour avoir une idée sur les arguments de chaque syscall il existe [cette page de blog](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) très bien écrite, mais malheureusement elle n'est plus à jour.


<blockquote class="small-text">
Références:
<ul>
<li><a href="https://stackoverflow.com/questions/38751614/what-are-the-return-values-of-system-calls-in-assembly">https://stackoverflow.com/questions/38751614/what-are-the-return-values-of-system-calls-in-assembly</a></li>
</ul>
</blockquote>


# 2. Svartalfheim

## 2.1. Rex prefix

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://wiki.osdev.org/X86-64_Instruction_Encoding">https://wiki.osdev.org/X86-64_Instruction_Encoding</a></li>
</ul>
</blockquote>

## 2.2. L'ordre d'exécution

> Les accès mémoire sont faits de façon asynchrone -> registres doivent être independant.

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://www.wikipedia.com/en/Register_renaming">https://www.wikiwand.com/en/Register_renaming</a></li>
</ul>
</blockquote>