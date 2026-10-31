{ liero::FUN_1ec2_0e06 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0e06.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0e06.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0e06(undefined4 param_1,byte param_2,int param_3,int param_4)
// 
// {
//   if (param_2 != 0) {
//     if ((((-1 < param_4) && (param_4 < 0x9e)) && (-1 < param_3)) && (param_3 < 0x9e)) {
//       if (param_2 < 0x27) {
//         param_2 = param_2 + 9;
//       }
//       *(byte *)((int)param_1 + param_3 * 0x140 + param_4) = param_2;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0e06(param_1: Longint; param_2: Byte; param_3, param_4: Integer);
var
  pixelAddress: Longint;
  pixelValue: Byte;
begin
  if (param_2 = 0) or (param_3 < 0) or (param_3 >= $9E) or
     (param_4 < 0) or (param_4 >= $9E) then
    Exit;
  pixelValue := param_2;
  if pixelValue < $27 then
    Inc(pixelValue, 9);
  pixelAddress := (param_1 + Longint(param_3) * $140 + param_4) and $FFFFF;
  RealModeMemory[pixelAddress] := pixelValue;
end;
