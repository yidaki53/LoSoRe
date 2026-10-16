/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0628
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __cdecl16far FUN_24dd_0628(void) {
    int *piVar1;
    int *piVar2;
    int iVar3;
    int *piVar4;
    int *piVar5;

    piVar5 = (int *)0xd8;
    *piVar5 = (int)(0xd8 - 0xc);
    piVar4 = (int *)0x0;
    for (iVar3 = 6; iVar3 != 0; iVar3--) {
        piVar2 = piVar4;
        piVar4 = piVar4 + 1;
        *piVar2 = *piVar5;
    }
    return;
}
