## Basic Instructions

| Category | Operation Type | Opcodes and Links | Explanation |
|----------|---------------|----------|-------------|
| Basic Data Movement | Register/Memory Move | [`mov`](https://www.felixcloutier.com/x86/mov) | Transfers data between registers, memory, or loads immediate values |
| | Conditional Move | [`cmovcc`](https://www.felixcloutier.com/x86/cmovcc) | Moves data only if condition code (cc) is met (e.g., `cmove`, `cmovg`) |
| | Extended Move | [`movsx`](https://www.felixcloutier.com/x86/movsx:movsxd), [`movzx`](https://www.felixcloutier.com/x86/movzx) | Sign-extend (`movsx`) or zero-extend (`movzx`) smaller values to larger sizes |
| Stack Operations | Push | [`push`](https://www.felixcloutier.com/x86/push) | Decrements RSP and stores operand on stack |
| | Pop | [`pop`](https://www.felixcloutier.com/x86/pop) | Loads value from stack and increments RSP |
| | Enter/Leave | [`enter`](https://www.felixcloutier.com/x86/enter), [`leave`](https://www.felixcloutier.com/x86/leave) | Create/remove stack frame |
| Arithmetic | Basic Math | [`add`](https://www.felixcloutier.com/x86/add), [`sub`](https://www.felixcloutier.com/x86/sub) | Addition and subtraction |
| | Multiplication | [`mul`](https://www.felixcloutier.com/x86/mul), [`imul`](https://www.felixcloutier.com/x86/imul) | Unsigned (`mul`) and signed (`imul`) multiplication |
| | Division | [`div`](https://www.felixcloutier.com/x86/div), [`idiv`](https://www.felixcloutier.com/x86/idiv) | Unsigned (`div`) and signed (`idiv`) division |
| | Quick Math | [`inc`](https://www.felixcloutier.com/x86/inc), [`dec`](https://www.felixcloutier.com/x86/dec) | Increment or decrement by 1 |
| | Complex Math | [`lea`](https://www.felixcloutier.com/x86/lea) | Load Effective Address |
| Bitwise | Logic | [`and`](https://www.felixcloutier.com/x86/and), [`or`](https://www.felixcloutier.com/x86/or), [`xor`](https://www.felixcloutier.com/x86/xor) | Basic boolean operations |
| | Shifts | [`shl`](https://www.felixcloutier.com/x86/sal:sar:shl:shr), [`shr`](https://www.felixcloutier.com/x86/sal:sar:shl:shr) | Logical left/right shift |
| | Arithmetic Shifts | [`sal`](https://www.felixcloutier.com/x86/sal:sar:shl:shr), [`sar`](https://www.felixcloutier.com/x86/sal:sar:shl:shr) | Arithmetic left/right shift |
| | Rotates | [`rol`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`ror`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`rcl`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror), [`rcr`](https://www.felixcloutier.com/x86/rcl:rcr:rol:ror) | Rotate bits |
| Comparison | Compare | [`cmp`](https://www.felixcloutier.com/x86/cmp) | Subtracts operands and sets flags |
| | Test | [`test`](https://www.felixcloutier.com/x86/test) | ANDs operands and sets flags |
| Control Flow | Unconditional Jump | [`jmp`](https://www.felixcloutier.com/x86/jmp) | Direct jump to location |
| | Conditional Jump | [`jcc`](https://www.felixcloutier.com/x86/jcc) | Jump if condition met |
| | Call/Return | [`call`](https://www.felixcloutier.com/x86/call), [`ret`](https://www.felixcloutier.com/x86/ret) | Subroutine call and return |
| Flag Control | Carry Flag | [`clc`](https://www.felixcloutier.com/x86/clc), [`stc`](https://www.felixcloutier.com/x86/stc) | Clear/Set carry flag |
| | Direction Flag | [`cld`](https://www.felixcloutier.com/x86/cld), [`std`](https://www.felixcloutier.com/x86/std) | Clear/Set direction flag |
| | Interrupt Flag | [`cli`](https://www.felixcloutier.com/x86/cli), [`sti`](https://www.felixcloutier.com/x86/sti) | Clear/Set interrupt flag |
| System | System Call | [`syscall`](https://www.felixcloutier.com/x86/syscall) | Calls operating system function |
| | Interrupt | [`int`](https://www.felixcloutier.com/x86/int) | Software interrupt |

**lea example:**

```nasm
; Basic array indexing: getting address of array[index]
leal (%ebx, %ecx, 4), %eax    # eax = ebx + ecx*4 (array of dwords)
leaq (%rbx, %rcx, 8), %rax    # rax = rbx + rcx*8 (array of qwords)

; Addition of multiple values
leal 5(%rax, %rbx), %eax      # eax = rax + rbx + 5 (three-operand add)

; Multiplication and addition combined
leal 5(%rax, %rax, 2), %eax   # eax = rax * 3 + 5
```

<center>
<img src="./_static/images/gifs/pulp-fiction-john-travolta-text.gif" alt="Pourquoi cette page est en anglais ?"/>
</center>

## Memory Operations

| Instruction | Operation | Size | Link |
|-------------|-----------|------|------|
| [`stosb`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store AL | Byte | Store from AL to [RDI] |
| [`stosw`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store AX | Word | Store from AX to [RDI] |
| [`stosd`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store EAX | DWord | Store from EAX to [RDI] |
| [`stosq`](https://www.felixcloutier.com/x86/stos:stosb:stosw:stosd:stosq) | Store RAX | QWord | Store from RAX to [RDI] |
| [`scasb`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Byte | Byte | Compares AL with byte at [RDI] |
| [`scasw`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Word | Word | Compares AX with word at [RDI] |
| [`scasd`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Double Word | DWord | Compares EAX with dword at [RDI]|
| [`scasq`](https://www.felixcloutier.com/x86/scas:scasb:scasw:scasd:scasq) | Scan Quad Word | QWord | Compares RAX with qword at [RDI]|
| [`cmpsb`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Byte | Byte | Compare [RSI] with [RDI] |
| [`cmpsw`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Word | Word | Compare [RSI] with [RDI] |
| [`cmpsd`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Double | DWord | Compare [RSI] with [RDI] |
| [`cmpsq`](https://www.felixcloutier.com/x86/cmps:cmpsb:cmpsw:cmpsd:cmpsq) | Compare Quad | QWord | Compare [RSI] with [RDI] |
| [`movsb`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Byte | Byte | Move from [RSI] to [RDI] |
| [`movsw`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Word | Word | Move from [RSI] to [RDI] |
| [`movsd`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Double | DWord | Move from [RSI] to [RDI] |
| [`movsq`](https://www.felixcloutier.com/x86/movs:movsb:movsw:movsd:movsq) | Move Quad | QWord | Move from [RSI] to [RDI] |

**REP Instruction Prefixes (Special Explanation):**

The REP prefixes are powerful tools that automatically repeat memory operations using RCX as a counter:

1. [`rep`](https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz) (Repeat):
   - Repeats instruction RCX times
   - Decrements RCX after each operation
   - Stops when RCX = 0
   - Best used with MOVS and STOS instructions
   - Example: `REP MOVSB` copies RCX bytes from [RSI] to [RDI]

2. [`repe/repz`](https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz) (Repeat while Equal/Zero):
   - Repeats instruction while ZF=1 AND RCX>0
   - Best used with CMPS and SCAS for finding differences
   - Stops if ZF=0 or RCX=0
   - Example: `REPE CMPSB` compares strings until mismatch or RCX=0

3. [`repne/repnz`](https://www.felixcloutier.com/x86/rep:repe:repz:repne:repnz) (Repeat while Not Equal/Not Zero):
   - Repeats instruction while ZF=0 AND RCX>0
   - Best used with CMPS and SCAS for finding matches
   - Stops if ZF=1 or RCX=0
   - Example: `REPNE SCASB` scans for matching byte in string

**Important Notes:**
- Direction Flag (DF) controls increment/decrement:
  - When DF=0: RDI/RSI increment after operation
  - When DF=1: RDI/RSI decrement after operation
- Use `CLD` to clear DF (for increment) and `STD` to set DF (for decrement)
- RCX should be set to the desired count before using REP prefixes
- Memory operations always use RDI for destination, cannot be changed to other registers


