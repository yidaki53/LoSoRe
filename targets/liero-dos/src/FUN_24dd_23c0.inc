{ liero-dos::FUN_24dd_23c0 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_23c0.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_23c0.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// uint16_t FUN_24dd_23c0(uint16_t in_DX, uint16_t *unaff_SI) {
//     uint16_t uVar1 = *unaff_SI;
//     uint8_t bVar2 = (uint8_t)(uVar1 >> 8);
//     uint16_t result = ((uint16_t)(bVar2 >> 4) * '\n' + (bVar2 & 0xf)) * 10 + (uVar1 >> 4 & 0xf) * 10 + (uVar1 & 0xf);
//     return result;
// }
// --- end reference ---
function FUN_24dd_23c0: Longint;
begin
  { TODO: translate from asm/FUN_24dd_23c0.s — UNMATCHED until an oracle passes }
end;

