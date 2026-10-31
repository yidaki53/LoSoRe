{ liero::FUN_1ec2_0dc8 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0dc8.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0dc8.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0dc8(undefined4 param_1,char param_2,int param_3,int param_4)
// 
// {
//   if (param_2 != '\0') {
//     if ((((-1 < param_4) && (param_4 < 0x9e)) && (-1 < param_3)) && (param_3 < 0x9e)) {
//       *(char *)((int)param_1 + param_3 * 0x140 + param_4) = param_2;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0dc8(param_1: Longint; param_2: Char; param_3, param_4: Integer);
var
  pixelAddress: Longint;
begin
  if (param_2 = #0) or (param_3 < 0) or (param_3 >= $9E) or
     (param_4 < 0) or (param_4 >= $9E) then
    Exit;
  pixelAddress := (param_1 + Longint(param_3) * $140 + param_4) and $FFFFF;
  RealModeMemory[pixelAddress] := Byte(param_2);
end;
