{ liero-dos::FUN_24dd_3eaf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3eaf.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3eaf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// void FUN_24dd_3eaf(uint8_t param_1, uint8_t *param_2, uint8_t *param_3) {
//     uint8_t bVar1;
//     uint16_t uVar2;
//     uint8_t *pbVar3;
//     uint8_t *pbVar4;
// 
//     pbVar3 = param_3;
//     pbVar4 = param_2;
//     bVar1 = *param_3;
//     if (param_1 < bVar1) {
//         bVar1 = param_1;
//     }
//     *param_2 = bVar1;
//     uVar2 = (uint16_t)bVar1;
//     while (uVar2 != 0) {
//         pbVar4++;
//         pbVar3++;
//         uVar2--;
//         *pbVar4 = *pbVar3;
//     }
// }
// --- end reference ---
procedure FUN_24dd_3eaf(param_1: Byte; param_2, param_3: Pointer);
var
    bVar1: Byte;
    uVar2: Word;
    pbVar3: ^Byte;
    pbVar4: ^Byte;
begin
    pbVar3 := param_3;
    pbVar4 := param_2;
    bVar1 := pbVar3^;
    if param_1 < bVar1 then
        bVar1 := param_1;
    pbVar4^ := bVar1;
    uVar2 := Word(bVar1);
    while uVar2 <> 0 do
    begin
        Inc(pbVar4);
        Inc(pbVar3);
        Dec(uVar2);
        pbVar4^ := pbVar3^;
    end;
end;
