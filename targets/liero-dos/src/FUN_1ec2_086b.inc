{ liero-dos::FUN_1ec2_086b — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_086b.s via c->pascal+llm(http://localhost:8080,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_086b.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 FUN_1ec2_086b(undefined2 param_1,int param_2)
// 
// {
//   undefined2 local_4;
//   
//   if (param_2 < 0) {
//     local_4 = 0xffff;
//   }
//   else if (param_2 < 1) {
//     local_4 = 0;
//   }
//   else {
//     local_4 = 1;
//   }
//   return local_4;
// }
// 
// --- end reference ---
function FUN_1ec2_086b(param_1: Word; param_2: Integer): Word;
var
  local_4: Word;
begin
  if param_2 < 0 then
    local_4 := $FFFF
  else if param_2 < 1 then
    local_4 := 0
  else
    local_4 := 1;
  FUN_1ec2_086b := local_4;
end;
