{ liero-dos::FUN_24dd_3f86 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3f86.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3f86.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void __stdcall16far FUN_24dd_3f86(uint8_t *param_1, uint8_t *param_2) {
//     uint8_t bVar1;
//     uint16_t uVar2;
//     uint8_t *pbVar3;
//     uint8_t *pbVar4;
// 
//     pbVar3 = param_2;
//     pbVar4 = param_1;
//     bVar1 = *param_2;
//     if (*param_1 < *param_2) {
//         bVar1 = *param_1;
//     }
//     if (bVar1 != 0) {
//         uVar2 = (uint16_t)bVar1;
//         do {
//             pbVar4 = pbVar4 + 1;
//             pbVar3 = pbVar3 + 1;
//             if (uVar2 == 0) {
//                 return;
//             }
//             uVar2 = uVar2 - 1;
//         } while (*pbVar3 == *pbVar4);
//     }
//     return;
// }
// --- end reference ---
procedure FUN_24dd_3f86(param_1, param_2: Pointer);
var
    bVar1: Byte;
    uVar2: Word;
    pbVar3: ^Byte;
    pbVar4: ^Byte;
begin
    pbVar3 := param_2;
    pbVar4 := param_1;
    bVar1 := pbVar3^;
    if pbVar4^ < pbVar3^ then
        bVar1 := pbVar4^;
    if bVar1 <> 0 then
    begin
        uVar2 := Word(bVar1);
        repeat
            Inc(pbVar4);
            Inc(pbVar3);
            if uVar2 = 0 then
                Exit;
            Dec(uVar2);
        until pbVar3^ <> pbVar4^;
    end;
    Exit;
end;
