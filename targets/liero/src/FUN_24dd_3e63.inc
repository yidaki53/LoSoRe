{ liero::FUN_24dd_3e63 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; register-state host tests).
  Original assembly retained in asm/FUN_24dd_3e63.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// uint __cdecl16far FUN_24dd_3e63(void)
//
// {
//   byte bVar1;
//   uint uVar2;
//   uint in_AX;
//   uint in_CX;
//   uint uVar3;
//   uint in_DX;
//   undefined2 unaff_DS;
//
//   if (*(byte *)0x6420 < 2) {
//     for (uVar3 = in_CX & 0x1f; uVar3 != 0; uVar3 = uVar3 - 1) {
//       uVar2 = in_DX & 1;
//       in_DX = in_DX >> 1;
//       in_AX = (uint)(CONCAT12(uVar2 != 0,in_AX) >> 1);
//     }
//     return in_AX;
//   }
//   bVar1 = (byte)in_CX & 0x1f;
//   return in_AX >> bVar1 | in_DX << 0x10 - bVar1;
// }
//
// --- end reference ---
function FUN_24dd_3e63: Word;
var
  combinedValue: Longword;
  shiftCount: Byte;
begin
  combinedValue := (Longword(RegisterDX) shl 16) or RegisterAX;
  shiftCount := RegisterCX and $1F;
  if DosMemory[$6420] < 2 then
    while shiftCount <> 0 do
    begin
      combinedValue := combinedValue shr 1;
      Dec(shiftCount);
    end
  else
    combinedValue := combinedValue shr shiftCount;
  RegisterDX := Word(combinedValue shr 16);
  RegisterAX := Word(combinedValue);
  FUN_24dd_3e63 := RegisterAX;
end;
