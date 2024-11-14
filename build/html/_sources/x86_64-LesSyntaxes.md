# Les syntaxes AT&T et Intel

La principale différence entre les syntaxes AT&T et Intel réside dans l'ordre des opérandes et leur notation. Pour une instruction de la forme `<op> A, B` :

1. **Ordre des opérandes** :
   - AT&T : `B <- B <op> A` (destination à droite)
   - Intel : `A <- A <op> B` (destination à gauche)

2. **Caractéristiques de la syntaxe AT&T** :
   - Préfixe `$` pour les valeurs immédiates
   - Préfixe `%` pour les registres
   - Préfixe `*` pour les sauts/appels absolus
   - Suffixe de taille sur l'instruction (`b`, `w`, `l`, `q`)

3. **Caractéristiques de la syntaxe Intel** :
   - Pas de préfixes pour les valeurs immédiates et registres
   - Spécification de la taille des données mémoire via des préfixes (`byte ptr`, `word ptr`, etc.)
   - Notation plus simple pour les opérations de base
4. **Les appels/sauts lointains** :
   - AT&T : `lcall` et `ljmp`
   - Intel : `call far` et `jump far`
> [!important]
> Sur AT&T les saut et appels absolu doivent être préfixés par '\*', Sans '\*', l'assembleur utilise l'adressage relatif au **rip**.

Exemple:
```nasm
; Copier 42 dans eax
;AT&T:
movl $42, %eax      ; B ← B op A
;Intel:
mov eax, 42         ; A ← A op B
```

## Spécification de la taille

**AT&T** utilise des suffixes sur l'instruction :
- `b` : byte (8 bits)
- `w` : word (16 bits)
- `l` : long (32 bits)
- `q` : quad (64 bits)


**Intel** utilise des préfixes sur l'opérande pour spécifié la taille des données à lire/écrire en mémoire (voyez le comme le type d'un pointeur en C) :
- `byte ptr` : 8 bits
- `word ptr` : 16 bits
- `dword ptr` : 32 bits
- `qword ptr` : 64 bits


Exemple :
```nasm
; Charger une valeur 16 bits depuis la mémoire
;AT&T:
movw (%ebx), %ax
;Intel:
mov ax, word ptr [ebx]
```


| Caractéristique     | Intel                | AT&T                    | Exemple Intel          | Exemple AT&T               |
| ------------------- | -------------------- | ----------------------- | ---------------------- | -------------------------- |
| Ordre des opérandes | Destination, Source  | Source, Destination     | `mov eax, 42`          | `movl $42, %eax`           |
| Préfixe registre    | (aucun)              | %                       | `eax`                  | `%eax`                     |
| Préfixe immédiat    | (aucun)              | $                       | `42`                   | `$42`                      |
| Taille opération    | Préfixe sur opérande | Suffixe sur instruction | `dword ptr`            | `movl`                     |
| Mode d'adressage    | `[ebx+ecx*2]`        | `(%ebx,%ecx,2)`         | `mov eax, [ebx+ecx*2]` | `movl (%ebx,%ecx,2), %eax` |

## Extensions de signe et de zéro

Format AT&T : `mov` + `s`(sign)/`z`(zero) + source size (`b`,`w`,`l`) + destination size (`w`,`l`,`q`)

Exemples courants :
```nasm
; Sign-extend byte vers long (32 bits)
   ;AT&T:
   movsbl %al, %eax
   ;Intel:
   movsx eax, al

; Zero-extend byte vers long
   ;AT&T: 
   movzbl %al, %eax
   ;Intel:
   movzx eax, al
```

Pour résumer, les instructions d'extensions avec `mov` sont:

| Opération              | Intel               | AT&T (variantes)          |
| ---------------------- | ------------------- | ------------------------- |
| sign-extend 8→16 bits  | `movsx r16, r/m8`   | `movsbw`/`movsxb`/`movsx` |
| sign-extend 8→32 bits  | `movsx r32, r/m8`   | `movsbl`/`movsxb`/`movsx` |
| sign-extend 8→64 bits  | `movsx r64, r/m8`   | `movsbq`/`movsxb`/`movsx` |
| sign-extend 16→32 bits | `movsx r32, r/m16`  | `movswl`/`movsxw`         |
| sign-extend 16→64 bits | `movsx r64, r/m16`  | `movswq`/`movsxw`         |
| sign-extend 32→64 bits | `movsxd r64, r/m32` | `movslq`/`movsxl`         |
| zero-extend 8→16 bits  | `movzx r16, r/m8`   | `movzbw`/`movzxb`/`movzx` |
| zero-extend 8→32 bits  | `movzx r32, r/m8`   | `movzbl`/`movzxb`/`movzx` |
| zero-extend 8→64 bits  | `movzx r64, r/m8`   | `movzbq`/`movzxb`/`movzx` |
| zero-extend 16→32 bits | `movzx r32, r/m16`  | `movzwl`/`movzxw`         |
| zero-extend 16→64 bits | `movzx r64, r/m16`  | `movzwq`/`movzxw`         |

- Certaines instructions ont plusieurs noms équivalents en AT&T (par exemple `movsbl`/`movsxb`/`movsx`) pour maintenir la compatibilité avec différentes conventions.

Il existe des instructions d'extension de signe specialement pour le registre `a`.

| Description                     | Intel  | AT&T   |
| ------------------------------- | ------ | ------ |
| byte(%al) → word(%ax)           | `cbw`  | `cbtw` |
| word(%ax) → dword(%eax)         | `cwde` | `cwtl` |
| dword(%eax) → quad(%rax)        | `cdqe` | `cltq` |
| word(%ax) → dword(%dx:%ax)      | `cwd`  | `cwtd` |
| dword(%eax) → quad(%edx:%eax)   | `cdq`  | `cltd` |
| quad(%rax) → octuple(%rdx:%rax) | `cqo`  | `cqto` |

## Notes Additionnelles

### Commentaires AT&T
- `#` : commentaire jusqu'à la fin de la ligne
- `;` : séparateur d'instructions
- `/` : commentaire (si --divide non activé)

### Optimisations courantes
- `xor %rax, %rax` est plus efficace que `mov $0, %rax` pour mettre à zéro un registre.
- `test %rax, %rax` est plus efficace que `cmp $0, %rax` pour tester si un registre est à zéro.
- Le compilateur peut ajouter des instructions `nop` (qui font rien) pour optimiser l'alignement en mémoire et l'utilisation du cache d'instructions.

### Notes pour sur le mode 64 bits
- Les opérations 32 bits sur les registres étends implicitement leur valeur à 64 bits avec des zéros. Par exemple, charger une valeur de 32-bits dans `%rax` va forcer les 32 bits de poids fort à zero même si la valeur est négative.
- `movslq`/`movsxd` sont nécessaire pour l'extension de signe 32→64 bits.
- `movq` ne peut pas être utilisée avec une valeur immédiates de 8 octets (64 bits). Utilisez `movabs` pour cela, par contre elle ne peut pas accèder directement à la mémoire, elle prend comme prend opérand que des registres et immédiats.