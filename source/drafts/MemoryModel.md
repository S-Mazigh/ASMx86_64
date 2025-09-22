- Type sizes:
- La taille des types (long, long long, ...), parler des standard des atleast ..., de l'abi (page 16), de ILP32 et LP64 et LL64 et finir avec une note sur les types explicites de cpp.


https://unix.org/version2/whatsnew/lp64_wp.html
https://www.mjr19.org.uk/IT/C/long.html


- Alignement:
Like the Intel386 architecture, the AMD64 architecture in general does not require all
data accesses to be properly aligned. Misaligned data accesses are slower than aligned
accesses but otherwise behave identically. The only exceptions are that __m128, __m256
and __m512 must always be aligned properly.

Structures and unions assume the alignment of their most strictly aligned component. Each
member is assigned to the lowest available offset with the appropriate alignment. The size
of any object is always a multiple of the object‘s alignment.
An array uses the same alignment as its elements, except that a local or global array
variable of length at least 16 bytes or a C99 variable-length array variable always has
alignment of at least 16 bytes.

There is no sense in which this is true, except for performance advantages of 8-byte loads. x86-64 can do 1, 2, 4, 8, or 16-byte loads. (And with AVX or AVX-512, 32 or 64-byte loads as well.) But it allows unaligned loads for any of these sizes. Some forms of 16-byte loads (like SSE memory operands) require 16-byte alignment, but nothing below 16 does. (There is an Alignment Check (AC) flag you can set in EFLAGS, but it's not very usable most of the time because compilers and libc implementations of memcpy freely use unaligned accesses.) Even microarchitecturally, modern x86 hardware truly does efficient unaligned accesses to its caches.

In modern x86 CPUs, it's actually a whole 64-byte cache line that's loaded from RAM. But we can more or less prove that even the hardware is doing single-byte accesses to cache because byte stores don't cause store-forwarding stalls for adjacent loads, and other factors.

Protocl MESI / MESIF/ MOESI


https://web.archive.org/web/20080607055623/http://www.ibm.com/developerworks/library/pa-dalign/
https://stackoverflow.com/questions/65773788/how-memory-aligment-and-access-granularity-work-in-assembly
https://stackoverflow.com/questions/46721075/can-modern-x86-hardware-not-store-a-single-byte-to-memory

C++:
https://gcc.gnu.org/wiki/Atomic/GCCMM/AtomicSync