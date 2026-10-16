/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_11aa
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void FUN_235c_11aa(void) {
    int *piVar1;
    int *piVar2;
    int iVar3;
    int iVar4;
    uint8_t *puVar5;
    uint8_t *puVar6;

    iVar4 = *(int *)0x6e6c;
    puVar5 = (uint8_t *)*(uint16_t *)0x6a58;
    puVar6 = (uint8_t *)*(uint16_t *)0x6e86;
    iVar3 = 0x200;
    piVar2 = (int *)0x6a58;
    do {
        if (iVar3 == 0) break;
        iVar3--;
        piVar1 = piVar2;
        piVar2 = piVar2 + 1;
        puVar6 = puVar6 + 1;
        puVar5 = puVar5 + 1;
        *puVar6 = (uint8_t)*puVar5;
    } while (iVar3 != 0);
    return;
}
