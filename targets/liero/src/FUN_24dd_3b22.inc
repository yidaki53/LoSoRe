{ liero::FUN_24dd_3b22 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host far-pointer memory tests).
  Original assembly retained in asm/FUN_24dd_3b22.s.
  The Ghidra decompiler reference is embedded below.
}
// --- reference: Ghidra decompiler C ---
// 
// void __stdcall16far FUN_24dd_3b22(byte *param_1,undefined2 *param_2)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   undefined2 uVar7;
//   
//   uVar7 = (undefined2)((ulong)param_2 >> 0x10);
//   pbVar6 = (byte *)((undefined2 *)param_2 + 1);
//   *param_2 = 0;
//   pbVar6[0] = 0xb0;
//   pbVar6[1] = 0xd7;
//   for (iVar3 = 0x16; pbVar6 = pbVar6 + 2, iVar3 != 0; iVar3 = iVar3 + -1) {
//     pbVar6[0] = 0;
//     pbVar6[1] = 0;
//   }
//   uVar4 = 0x4f;
//   pbVar5 = (byte *)param_1 + 1;
//   if (0x4e < *param_1) goto LAB_24dd_3b4e;
//   for (uVar4 = (uint)*param_1; uVar4 != 0; uVar4 = uVar4 - 1) {
// LAB_24dd_3b4e:
//     pbVar1 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     if (*pbVar1 == 0) break;
//     pbVar2 = pbVar6;
//     pbVar6 = pbVar6 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   *pbVar6 = 0;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3b22(param_1, param_2: Longint);
var
  sourceOffset: Word;
  sourceSegment: Word;
  destinationOffset: Word;
  destinationSegment: Word;
  sourceLength: Byte;
  remaining: Byte;
  sourceAddress: Longint;
  destinationAddress: Longint;
  byteIndex: Integer;
  currentByte: Byte;
begin
  sourceOffset := Word(param_1);
  sourceSegment := Word(param_1 shr 16);
  destinationOffset := Word(param_2);
  destinationSegment := Word(param_2 shr 16);
  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := 0;
  Inc(destinationOffset);
  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := 0;
  Inc(destinationOffset);
  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := $B0;
  Inc(destinationOffset);
  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := $D7;
  Inc(destinationOffset);

  for byteIndex := 4 to 47 do
  begin
    destinationAddress := ((Longint(destinationSegment) shl 4) +
      Word(Word(param_2) + byteIndex)) and $FFFFF;
    RealModeMemory[destinationAddress] := 0;
  end;
  Inc(destinationOffset, 44);

  sourceAddress := ((Longint(sourceSegment) shl 4) + sourceOffset) and $FFFFF;
  sourceLength := RealModeMemory[sourceAddress];
  if sourceLength < 79 then
    remaining := sourceLength
  else
    remaining := 79;
  Inc(sourceOffset);

  while remaining <> 0 do
  begin
    sourceAddress := ((Longint(sourceSegment) shl 4) + sourceOffset) and
      $FFFFF;
    currentByte := RealModeMemory[sourceAddress];
    if currentByte = 0 then
      Break;
    destinationAddress := ((Longint(destinationSegment) shl 4) +
      destinationOffset) and $FFFFF;
    RealModeMemory[destinationAddress] := currentByte;
    Inc(sourceOffset);
    Inc(destinationOffset);
    Dec(remaining);
  end;

  destinationAddress := ((Longint(destinationSegment) shl 4) +
    destinationOffset) and $FFFFF;
  RealModeMemory[destinationAddress] := 0;
end;
