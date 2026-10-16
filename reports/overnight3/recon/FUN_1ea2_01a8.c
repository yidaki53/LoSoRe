/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ea2_01a8
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ea2_01a8(int *param_1, int *param_2, int param_3, int param_4, int param_5) {
    int iVar1;
    int *piVar2;
    int *piVar3;
    uint uVar4;
    uint *puVar5;
    uint *puVar6;

    uVar4 = (uint)param_5 >> 1;
    piVar2 = param_1;
    piVar3 = param_2;
    if ((param_5 & 1) != 0) {
        uVar4 = uVar4 * 2;
        piVar3 = (int *)((int)piVar3 + (param_5 & -2));
    }
    puVar5 = (uint *)((int)piVar2 + uVar4);
    puVar6 = (uint *)((int)piVar3 + uVar4);
    iVar1 = uVar4;
    do {
        for (; iVar1 != 0; iVar1--) {
            *puVar5 = *puVar6;
            puVar5++;
            puVar6++;
        }
        puVar5 = (uint *)((int)puVar5 + (0x140 - uVar4));
        puVar6 = (uint *)((int)puVar6 + (0x140 - uVar4));
        iVar1 = uVar4;
    } while (param_5 != 0);
    return;
}
