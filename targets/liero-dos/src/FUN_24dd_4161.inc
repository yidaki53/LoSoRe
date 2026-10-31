{ liero-dos::FUN_24dd_4161 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_4161.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_4161.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:contested decompiler C (unmatched) ---
// #include <stdint.h>
// 
// int16_t __cdecl16far FUN_24dd_4161(uint16_t in_AX, uint16_t in_DX) {
//     int8_t sVar1;
//     uint8_t bVar2;
//     uint8_t bVar3;
// 
//     bVar2 = (uint8_t)(in_AX >> 3);
//     bVar3 = (uint8_t)(in_DX >> 8);
//     if ((bVar3 <= bVar2) && ((uint8_t)(bVar2 - bVar3) < (uint8_t)in_DX)) {
//         sVar1 = (int8_t)(in_AX & 0xff07);
//         bVar2 = (uint8_t)((in_AX & 0xff07) >> 8);
//         return ((uint16_t)bVar2 << 8) | (bVar2 << sVar1) | (bVar2 >> (8 - sVar1));
//     }
//     return (int16_t)(in_AX >> 0xf);
// }
// --- end reference ---
function FUN_24dd_4161: Integer;
begin
  { TODO: translate from asm/FUN_24dd_4161.s — UNMATCHED until an oracle passes }
end;

