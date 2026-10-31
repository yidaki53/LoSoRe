{ liero::FUN_24dd_3e7c — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; register-state host tests).
  Original assembly retained in asm/FUN_24dd_3e7c.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// int __cdecl16far FUN_24dd_3e7c(void)
//
// {
//   int in_AX;
//   uint in_CX;
//   uint uVar1;
//   undefined2 unaff_DS;
//
//   if (*(byte *)0x6420 < 2) {
//     for (uVar1 = in_CX & 0x1f; uVar1 != 0; uVar1 = uVar1 - 1) {
//       in_AX = in_AX << 1;
//     }
//     return in_AX;
//   }
//   return in_AX << ((byte)in_CX & 0x1f);
// }
//
// --- end reference ---
function FUN_24dd_3e7c: Integer;
var
  combinedValue: Longword;
  shiftCount: Byte;
begin
  combinedValue := (Longword(RegisterDX) shl 16) or RegisterAX;
  shiftCount := RegisterCX and $1F;
  if DosMemory[$6420] < 2 then
    while shiftCount <> 0 do
    begin
      combinedValue := combinedValue shl 1;
      Dec(shiftCount);
    end
  else
    combinedValue := combinedValue shl shiftCount;
  RegisterDX := Word(combinedValue shr 16);
  RegisterAX := Word(combinedValue);
  FUN_24dd_3e7c := SmallInt(RegisterAX);
end;
