/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0673
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __cdecl16far FUN_24dd_0673(void) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    int iVar3;
    uint16_t *puVar4;
    uint16_t *puVar5;

    puVar4 = (uint16_t *)0xd8;
    puVar5 = (uint16_t *)((int)puVar4 - 0xc);
    *puVar5 = (uint16_t)puVar4;
    for (iVar3 = 6; iVar3 != 0; iVar3--) {
        puVar2 = puVar5;
        puVar5 = puVar5 + 1;
        puVar1 = puVar4;
        puVar4 = puVar4 + 1;
        *puVar2 = *puVar1;
    }
    return;
}
