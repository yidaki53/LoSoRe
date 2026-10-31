{ liero::FUN_24dd_3f86 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host string and flag tests).
  Original assembly retained in asm/FUN_24dd_3f86.s.
  The Ghidra decompiler reference is embedded below; far-pointer addressing
  and compare flags are modeled from the assembly.
}
// --- reference: Ghidra decompiler C ---
//
// void __stdcall16far FUN_24dd_3f86(byte *param_1,byte *param_2)
//
// {
//   byte bVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//
//   pbVar3 = (byte *)param_2;
//   pbVar4 = (byte *)param_1;
//   bVar1 = *param_2;
//   if (*param_1 < *param_2) {
//     bVar1 = *param_1;
//   }
//   if (bVar1 != 0) {
//     uVar2 = (uint)bVar1;
//     do {
//       pbVar4 = pbVar4 + 1;
//       pbVar3 = pbVar3 + 1;
//       if (uVar2 == 0) {
//         return;
//       }
//       uVar2 = uVar2 - 1;
//     } while (*pbVar3 == *pbVar4);
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3f86(param_1, param_2: Longint);
var
  destinationOffset: Word;
  destinationSegment: Word;
  sourceOffset: Word;
  sourceSegment: Word;
  destinationLength: Byte;
  sourceLength: Byte;
  compareLength: Byte;
  remaining: Byte;
  destinationAddress: Longint;
  sourceAddress: Longint;
begin
  destinationOffset := Word(param_1);
  destinationSegment := Word(param_1 shr 16);
  sourceOffset := Word(param_2);
  sourceSegment := Word(param_2 shr 16);
  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  sourceAddress := ((Longint(sourceSegment) shl 4) + sourceOffset) and $FFFFF;
  destinationLength := RealModeMemory[destinationAddress];
  sourceLength := RealModeMemory[sourceAddress];
  Inc(destinationOffset);
  Inc(sourceOffset);

  if sourceLength < destinationLength then
    compareLength := sourceLength
  else
    compareLength := destinationLength;
  remaining := compareLength;
  if remaining = 0 then
  begin
    RegisterZeroFlag := sourceLength = destinationLength;
    RegisterCarryFlag := sourceLength < destinationLength;
    Exit;
  end;

  while remaining <> 0 do
  begin
    destinationAddress := ((Longint(destinationSegment) shl 4) +
      destinationOffset) and $FFFFF;
    sourceAddress := ((Longint(sourceSegment) shl 4) + sourceOffset) and $FFFFF;
    if RealModeMemory[destinationAddress] <> RealModeMemory[sourceAddress] then
    begin
      RegisterZeroFlag := False;
      RegisterCarryFlag :=
        RealModeMemory[sourceAddress] < RealModeMemory[destinationAddress];
      Exit;
    end;
    Inc(destinationOffset);
    Inc(sourceOffset);
    Dec(remaining);
  end;

  RegisterZeroFlag := sourceLength = destinationLength;
  RegisterCarryFlag := sourceLength < destinationLength;
end;
