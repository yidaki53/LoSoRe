{ liero::FUN_24dd_3f40 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host far-pointer search tests).
  Original assembly retained in asm/FUN_24dd_3f40.s.
  The Ghidra decompiler reference is embedded below.
}
// --- reference: Ghidra decompiler C ---
// 
// byte * __stdcall16far FUN_24dd_3f40(byte *param_1,byte *param_2)
// 
// {
//   byte *pbVar1;
//   int iVar2;
//   int iVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   byte *pbVar7;
//   undefined2 uVar8;
//   undefined2 uVar9;
//   bool bVar10;
//   
//   uVar9 = (undefined2)((ulong)param_2 >> 0x10);
//   if (*param_2 != 0) {
//     uVar4 = (uint)*param_2;
//     uVar8 = (undefined2)((ulong)param_1 >> 0x10);
//     if (uVar4 <= *param_1) {
//       iVar2 = (*param_1 - uVar4) + 1;
//       pbVar7 = (byte *)param_1 + 1;
//       pbVar6 = pbVar7;
//       do {
//         pbVar5 = (byte *)param_2 + 1;
//         bVar10 = pbVar6 == (byte *)0x0;
//         do {
//           if (iVar2 == 0) break;
//           iVar2 = iVar2 + -1;
//           pbVar1 = pbVar7;
//           pbVar7 = pbVar7 + 1;
//           bVar10 = *pbVar5 == *pbVar1;
//         } while (!bVar10);
//         if (!bVar10) {
//           return (byte *)0x0;
//         }
//         iVar3 = uVar4 - 1;
//         bVar10 = iVar3 == 0;
//         pbVar6 = pbVar7;
//         do {
//           pbVar5 = pbVar5 + 1;
//           if (iVar3 == 0) break;
//           iVar3 = iVar3 + -1;
//           pbVar1 = pbVar6;
//           pbVar6 = pbVar6 + 1;
//           bVar10 = *pbVar5 == *pbVar1;
//         } while (bVar10);
//         if (bVar10) {
//           return pbVar7 + (-1 - (int)(byte *)param_1);
//         }
//         pbVar6 = (byte *)param_2 + 1;
//       } while( true );
//     }
//   }
//   return (byte *)0x0;
// }
// 
// --- end reference ---
function FUN_24dd_3f40(param_1, param_2: Longint): Word;
var
  haystackOffset: Word;
  haystackSegment: Word;
  needleOffset: Word;
  needleSegment: Word;
  haystackLength: Byte;
  needleLength: Byte;
  candidate: Word;
  matchIndex: Word;
  haystackAddress: Longint;
  needleAddress: Longint;
  matches: Boolean;
begin
  haystackOffset := Word(param_1);
  haystackSegment := Word(param_1 shr 16);
  needleOffset := Word(param_2);
  needleSegment := Word(param_2 shr 16);
  haystackAddress := ((Longint(haystackSegment) shl 4) + haystackOffset) and
    $FFFFF;
  needleAddress := ((Longint(needleSegment) shl 4) + needleOffset) and
    $FFFFF;
  haystackLength := RealModeMemory[haystackAddress];
  needleLength := RealModeMemory[needleAddress];
  FUN_24dd_3f40 := 0;
  if (needleLength = 0) or (needleLength > haystackLength) then
    Exit;

  for candidate := 0 to haystackLength - needleLength do
  begin
    matches := True;
    for matchIndex := 0 to needleLength - 1 do
    begin
      haystackAddress :=
        ((Longint(haystackSegment) shl 4) +
         Word(haystackOffset + 1 + candidate + matchIndex)) and $FFFFF;
      needleAddress :=
        ((Longint(needleSegment) shl 4) +
         Word(needleOffset + 1 + matchIndex)) and $FFFFF;
      if RealModeMemory[haystackAddress] <>
         RealModeMemory[needleAddress] then
      begin
        matches := False;
        Break;
      end;
    end;
    if matches then
    begin
      FUN_24dd_3f40 := candidate + 1;
      Exit;
    end;
  end;
end;
