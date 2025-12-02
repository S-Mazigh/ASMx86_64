---
title: Your Page Title 
index: true
---

# Rappels sur la compilation avec gcc

## Les différentes étapes de la compilation

La compilation d'un programme C est un processus en plusieurs étapes, chacune transformant le code d'un format à un autre.

```{mermaid}
flowchart TD
    subgraph source["Fichiers Source"]
        A1[fichier1.c]
        A2[fichier2.c]
        A3[fichier3.c]
    end
    
    subgraph preproc["Prétraitement"]
        B1[fichier1.i]
        B2[fichier2.i]
        B3[fichier3.i]
    end
    
    subgraph compil["Compilation: C -> ASM"]
        C1[fichier1.s]
        C2[fichier2.s]
        C3[fichier3.s]
    end
    
    subgraph assem["Assembleur: ASM -> BIN"]
        D1[fichier1.o]
        D2[fichier2.o]
        D3[fichier3.o]
    end
    
    subgraph link["ÉDITEUR DE LIENS"]
        E[programme ELF]
        F[Bibliothèques externes]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    
    B1 --> C1
    B2 --> C2
    B3 --> C3
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    
    D1 --> E
    D2 --> E
    D3 --> E
    F --> E
	
	style source fill:#e1f5ff,stroke:#666,stroke-width:2px
    style preproc fill:#fff4e1,stroke:#666,stroke-width:2px
    style compil fill:#f0e1ff,stroke:#666,stroke-width:2px
    style assem fill:#e1ffe1,stroke:#666,stroke-width:2px
    style link fill:#ffe1e1,stroke:#666,stroke-width:2px

```

### Étape 1 : Preprocessing (Prétraitement)

**Commande** : `gcc -E fichier.c -o fichier.i`

Le préprocesseur effectue les opérations suivantes :
- Il supprime les commentaires du code source
- Il développe les macros (#define)
- Il inclut récursivement les fichiers d'en-tête (#include .h)
- Il traite les directives conditionnelles (#ifdef, #ifndef, etc.)

À la fin de cette étape, nous obtenons du code C pur et compilable. Le fichier contient également des "line markers" (méta-données) commençant par `#`, qui permettent de tracer l'origine du code (de quel include une ligne vient).

**Exemple** :
```c
// Avant preprocessing
#include <stdio.h>
#define MAX 100
int main() {
    printf("Max: %d\n", MAX);
}

// Après preprocessing (fichier .i)
// [Contenu de stdio.h et des includes imbriqués]
int main() {
    printf("Max: %d\n", 100);
}
```

### Étape 2 : Compilation

**Commande** : `gcc -S fichier.i -o fichier.s`

Maintenant que nous avons tout le code C nécessaire au bon fonctionnement de notre programme, il faut le traduire en un langage plus compréhensible pour la machine. Cette étape se charge de :
- L'analyse syntaxique du code
- La vérification des types
- L'optimisation du code (-O1, -O2, -O3)
- La génération du code assembleur pour l'architecture ciblée

La majorité des optimisations s'effectue à cette étape. L'objectif est de bien traduire le langage de haut niveau (le C dans notre exemple) en code assembleur tout en tirant parti des optimisations offertes par l'architecture ciblée.

Le code assembleur se compose d'un mnémonique d'opération et d'opérandes. Il reste compréhensible par l'humain, mais moins que les langages de haut niveau comme le C ou Java.

```nasm
; 'movl' est le mnémonique, '$100' et '%esi' sont les opérandes
movl    $100, %esi
```

**Options importantes** :
- `-march=architecture` : Spécifie l'architecture cible
- `-O[0-3]` : Niveau d'optimisation
- `-fverbose-asm` : Ajoute des commentaires dans l'assembleur

**Exemple** :
```nasm
	.file	"exemple.c"
	.text
	.section	.rodata
.LC0:
	.string	"Max: %d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$100, %esi
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
```

### Étape 3 : Assembly (Assemblage)

**Commande** : 
- Via GCC : `gcc -c fichier.s -o fichier.o`
- Direct : `as fichier.s -o fichier.o`

Malheureusement, même le code assembleur n'est pas compréhensible par nos CPU qui ne fonctionnent qu'avec des 0 et des 1. L'assembleur `as` se charge de faire la dernière traduction en transformant les instructions en valeurs binaires. Cette représentation binaire est directement exécutable par le processeur, elle est compréhensibles par le décodeur du CPU, la partie qui dit aux autres composants quoi faire.

L'assembleur :
- Convertit le code assembleur en code machine
- Crée une table des symboles
- Génère des relocations si nécessaire
- Produit un fichier objet au format ELF

### Étape 4 : Linkage (Édition des liens)

**Commande** : 
- Via GCC : `gcc fichier.o -o executable`
- Direct : `ld fichier.o -o executable`

On a tendance à bien structurer notre code et à le séparer en plusieurs fichiers pour mieux s'y retrouver lors de la relecture, que ce soit nous ou une autre personne. Il se peut même qu'on fasse appel à du code que nous n'avons pas écrit nous-mêmes, la libc étant le meilleur exemple (longue vie à printf !).

L'éditeur de liens `ld` (invoqué par `gcc`) a pour mission de rassembler tous ces morceaux de code. 

:::{Attention}
Les deux commandes ci-dessus ne sont **pas équivalentes**. GCC configure beaucoup de choses en arrière-plan, afin de simplifier le processus.

Par exemple, le vrai point d'entrée d'un exécutable est `_start`, pas `main`. GCC inclut automatiquement les fichiers de démarrage qui contiennent `_start` et qui appellent ensuite votre fonction `main`. 

Si vous utilisez `ld` directement, vous devrez fournir beaucoups d'éléments manuellement (dont la libc `-lc`).
:::

Pour voir ce que GCC fait réellement en coulisses :
```bash
gcc -v -o executable fichier.o
```

Il existe deux façons principales de lier ces différentes parties :

1. **La liaison statique** : 
- Toutes les bibliothèques sont directement copiées dans l'exécutable final
- Avantages : l'exécutable est autonome et portable
- Inconvénients : taille plus importante de l'exécutable, pas de mise à jour automatique des bibliothèques

2. **La liaison dynamique** (avec les .so) :
- Seules les références aux bibliothèques sont incluses dans l'exécutable
- Les bibliothèques partagées (.so - Shared Objects sous Linux) sont chargées au moment de l'exécution (les pages mémoire sont partagées par tous les processus l'utilisant)
- Avantages : 
  - Économie d'espace disque (les .so sont partagées entre les programmes)
  - Mise à jour des bibliothèques sans recompiler les programmes
  - Chargement à la demande des bibliothèques
- Inconvénients : 
  - Dépendance aux bibliothèques installées sur le système
  - Potentielles incompatibilités lors des mises à jour

L'éditeur de liens effectue donc plusieurs tâches cruciales :
- Résout les symboles externes (trouve où se trouvent les fonctions et variables utilisées)
- Combine les fichiers objets (.o)
- Gère les liaisons avec les bibliothèques (statiques .a ou dynamiques .so)
- Vérifie que toutes les dépendances sont satisfaites
- Génère l'exécutable final au format ELF

**Exemple pratique** :
```bash
# Création d'une bibliothèque partagée
gcc -shared -fPIC my_lib.c -o libmy_lib.so

# Compilation avec liaison dynamique (par défaut)
gcc my_prog.c -L. -lmy_lib -o prog

# Compilation avec liaison statique
gcc my_prog.c -static -L. -lmy_lib -o prog_static
```

Cette étape finale du processus de compilation est cruciale car elle détermine non seulement comment notre programme va s'exécuter, mais aussi comment il va interagir avec le reste du système.

<blockquote class="small-text">
Références :
<ul>
<li><a href="https://stackoverflow.com/questions/77108297/breaking-down-the-c-compilation-process-into-preprocessing-compilation-assembl">https://stackoverflow.com/questions/77108297/breaking-down-the-c-compilation-process-into-preprocessing-compilation-assembl</a></li>
</ul>
</blockquote>

## Récupérer l'assembleur d'un ELF

### objdump

`objdump` est un outil puissant de la suite binutils qui permet d'analyser et de désassembler des fichiers objets et des exécutables.

| Option          | Description                                                    | Exemple d'utilisation               |
| --------------- | -------------------------------------------------------------- | ----------------------------------- |
| `-d`            | Désassemble les sections contenant des instructions            | `objdump -d executable`             |
| `-D`            | Désassemble toutes les sections (y compris .data) sauf le .bss | `objdump -D executable`             |
| `-S`            | Mélange code source si disponible et assembleur                | `objdump -S executable`             |
|                 |                                                                |                                     |
| `-j section`    | Affiche uniquement la section spécifiée                        | `objdump -d -j .text executable`    |
| `--section=sec` | Identique à -j                                                 | `objdump --section=.plt executable` |
|                 |                                                                |                                     |
| `-M intel`      | Utilise la syntaxe Intel                                       | `objdump -M intel -d executable`    |
| `-M att`        | Utilise la syntaxe AT&T (par défaut)                           | `objdump -M att -d executable`      |

### nm

Affiche les symboles d'un fichier objet :

```bash
nm fichier.o
```

### readelf

Analyse détaillée des fichiers ELF :

```bash
# En-tête ELF
readelf -h executable

# Table des sections
readelf -S executable

# Segments (Program Headers)
readelf -l executable
```