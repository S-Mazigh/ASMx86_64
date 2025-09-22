# Svartalfheim

## SSE for Scalar Floating-point
uses xmm registers and floating point types
movsd: sd for single double precision
ss for a single single precision
ps for a vector of single precision f operation
pd for a vector of a double precision  f operation

schema sur les vector ALU hardware SIMD !

paddq : p prefix dinstiguises and integer vector instruction

## AVX and AVX-2

Uses wider registers ymmm, and operations have three operands as in mips
vaddpd(avx) vs addpd (sse)
vpaddpd vs paddpd
the v is for avx

## Pileplining
Instruction fecth (if), Instruction Decode (ID), Execute (EX), Memory (MA), Write back (WB)

ymm register aliases the xmm register as for ax and ha and la

Haswell microarchictecture between 14 to 19 pipeline stages

### Instruction level parallelism

Les stalls: La dependence entre les instructions. Utilisation des même registres, attente de mémoire, les branch !

RAW
WAR
Output dependence: flag actualization, could be dependency with other instructions

Bypassing: Read data directly from the alu instead of waiting for the write back.

Cela require des changer l'ordre des instructions

### Speculative Execution

When a branch is encountered, the code after the branch instruction is executed without checking if the jump is to be taken or not. Thus, the execution must be nullified if the branch is indeedly taken.


### Superscalar

fetch several and decode multiple instructions

Instructions are split into simpler micro-ops, for instance xor %rax, %rax doesn't use the ALU, the cpu just resets rax



## Rex prefix

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://wiki.osdev.org/X86-64_Instruction_Encoding" target="_blank">https://wiki.osdev.org/X86-64_Instruction_Encoding</a></li>
</ul>
</blockquote>

## L'ordre d'exécution

> Les accès mémoire sont faits de façon asynchrone -> registres doivent être indépendant.

<blockquote class="small-text">
Références:
<ul>
<li><a href="https://en.wikipedia.org/wiki/Register_renaming" target="_blank">https://en.wikipedia.org/wiki/Register_renaming</a></li>
</ul>
</blockquote>

