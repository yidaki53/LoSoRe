{ liero-dos::FUN_235c_0361 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0361.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0361.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// uint16_t __cdecl16far FUN_235c_0361(void) {
//     uint16_t result;
//     result = FUN_2494_001e();
//     return result;
// }
// --- end reference ---
function FUN_235c_0361: Word;
var
    result: Word;
begin
    result := FUN_2494_001e;
    FUN_235c_0361 := result;
end;
