/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_249c_0037
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=3 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_249c_0013(void *stack_ptr);
void FUN_249c_0000(uint16_t param1, uint16_t param2);
void FUN_24dd_3930(uint16_t seg, uint16_t ds);
void FUN_24dd_04f4(void);

void __stdcall16far FUN_249c_0037(uint16_t ds, uint16_t seg, byte *param_1, byte param_2, byte param_3) {
    byte local_102[256];
    byte *pbVar1 = local_102;
    byte *pbVar5 = param_1;
    uint uVar4 = (uint)local_102[0];
    byte local_10a;
    byte local_108;
    byte local_105;
    char local_103;
    byte bVar2;

    local_102[0] = *param_1;
    for (; uVar4 != 0; uVar4--) {
        *pbVar1++ = *pbVar5++;
    }
    FUN_249c_0013((void *)0xfffe);
    local_10a = (byte)(((uint)param_2 * 0x50 + (uint)param_3) * 2);
    uint16_t uVar3 = (uint16_t)((uint)local_10a >> 8);
    FUN_249c_0000(((uint16_t)uVar3 << 8) | param_2, ((uint16_t)uVar3 << 8) | param_3);
    bVar2 = local_102[0];
    local_103 = '\0';
    if (local_102[0] != 0) {
        local_108 = 1;
        while (true) {
            if (local_103 == '\0') {
                if (local_102[local_108] == 0) {
                    local_103 = '\x01';
                } else {
                    *(byte *)(seg * 16 + local_10a) = local_102[local_108];
                    *(byte *)(seg * 16 + local_10a + 1) = local_105;
                    local_10a += 2;
                }
            } else if (local_103 == '\x01') {
                local_103 = '\x02';
                FUN_249c_0013((void *)0xfffe);
            } else if (local_103 == '\x02') {
                local_103 = '\0';
                FUN_249c_0013((void *)0xfffe);
            }
            if (local_108 == bVar2) break;
            local_108++;
        }
    }
    FUN_249c_0000(((uint16_t)((uint)param_3 + (uint)local_102[0] >> 8) << 8) | param_2, (uint16_t)param_3 + (uint16_t)local_102[0]);
    FUN_24dd_3930(0x79f0, ds);
    FUN_24dd_04f4();
}
