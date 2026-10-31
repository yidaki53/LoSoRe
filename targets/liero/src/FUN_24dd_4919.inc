{ liero::FUN_24dd_4919 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; exhaustive host behavior test).
  Original assembly retained in asm/FUN_24dd_4919.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// byte __stdcall16far FUN_24dd_4919(byte param_1)
// 
// {
//   if ((0x60 < param_1) && (param_1 < 0x7b)) {
//     param_1 = param_1 - 0x20;
//   }
//   return param_1;
// }
// 
// --- end reference ---
function FUN_24dd_4919(param_1: Byte): Byte;
begin
  if (param_1 >= $61) and (param_1 <= $7A) then
    FUN_24dd_4919 := param_1 - $20
  else
    FUN_24dd_4919 := param_1;
end;
