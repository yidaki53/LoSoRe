{ liero-dos::FUN_235c_135f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_135f.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_135f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// void __cdecl16far FUN_235c_135f(void) {
//     *((uint8_t*)(0x67fa)) = 0;
//     *((uint8_t*)(0x7688)) = 0;
//     *((uint8_t*)(0x7690)) = 0;
//     return;
// }
// --- end reference ---
procedure FUN_235c_135f;
var
  p1: ^Byte;
  p2: ^Byte;
  p3: ^Byte;
begin
  p1 := Pointer($67fa);
  p2 := Pointer($7688);
  p3 := Pointer($7690);
  p1^ := 0;
  p2^ := 0;
  p3^ := 0;
end;
