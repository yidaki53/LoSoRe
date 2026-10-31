{ liero::FUN_1ec2_10cf — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_10cf.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_10cf.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __stdcall16far
// FUN_1ec2_10cf(undefined1 param_1,undefined1 param_2,undefined1 param_3,undefined1 param_4)
// 
// {
//   out(0x3c8,param_4);
//   out(0x3c9,param_3);
//   out(0x3c9,param_2);
//   out(0x3c9,param_1);
//   return param_1;
// }
// 
// --- end reference ---
function FUN_1ec2_10cf(param_1, param_2, param_3, param_4: Byte): Byte;
begin
  VideoPalette[param_4].Red := param_3;
  VideoPalette[param_4].Green := param_2;
  VideoPalette[param_4].Blue := param_1;
  FUN_1ec2_10cf := param_1;
end;
