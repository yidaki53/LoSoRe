/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_118c
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void FUN_235c_118c(void) {
    int *piVar1;
    int *piVar2;
    int iVar3;
    int *piVar4;

    piVar4 = (int *)0x6a58;
    piVar1 = (int *)0x6e6c;
    iVar3 = 0x200;
    do {
        piVar2 = piVar4;
        piVar4 = piVar4 + 1;
        *piVar2 = *piVar1 * 0x10000 + *piVar2;
        iVar3 = iVar3 - 1;
        piVar1 = piVar1 + 1;
    } while (iVar3 != 0);
    return;
}
