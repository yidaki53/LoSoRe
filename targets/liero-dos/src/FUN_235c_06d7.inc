{ liero-dos::FUN_235c_06d7 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_06d7.s via c->pascal+llm(http://localhost:8080,recon:real); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_06d7.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: recon:real decompiler C (unmatched) ---
// #include <stdint.h>
// 
// uint16_t FUN_235c_06d7(uint16_t param_1, int16_t param_2, uint16_t param_3, int16_t param_4) {
//     uint16_t local_6;
//     uint16_t local_4;
// 
//     if ((param_4 < param_2) || ((param_4 <= param_2) && (param_3 < param_1))) {
//         local_6 = param_3;
//         local_4 = param_4;
//     } else {
//         local_6 = param_1;
//         local_4 = param_2;
//     }
//     return (local_4 << 8) | local_6;
// }
// --- end reference ---
function FUN_235c_06d7(param_1: Word; param_2: Integer; param_3: Word; param_4: Integer): Longint;
var
    local_6: Word;
    local_4: Word;
begin
    if (param_4 < param_2) or ((param_4 <= param_2) and (param_3 < param_1)) then
    begin
        local_6 := param_3;
        local_4 := param_4;
    end
    else
    begin
        local_6 := param_1;
        local_4 := param_2;
    end;
    FUN_235c_06d7 := (local_4 shl 8) or local_6;
end;
