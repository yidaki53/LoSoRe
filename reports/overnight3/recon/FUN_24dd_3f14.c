/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3f14
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void FUN_24dd_3f14(byte *param_1, byte *param_2) {
    byte bVar1;
    byte bVar2;
    byte *pbVar3;
    byte *pbVar4;

    bVar2 = *param_2;
    *param_1 = bVar2 + *param_1;
    if ((bVar2 & 0x80) != 0) {
        *param_1 = 0xff;
        bVar1 = ~bVar2;
        pbVar3 = (byte *)((int)param_2 + (int)param_1);
        pbVar4 = (byte *)((int)param_1 + (int)param_2);
        while (true) {
            *pbVar3 = *pbVar4;
            if (bVar1 == 0) break;
            bVar1--;
            pbVar3++;
            pbVar4++;
        }
    }
    return;
}
