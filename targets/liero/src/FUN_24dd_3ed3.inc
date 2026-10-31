{ liero::FUN_24dd_3ed3 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer tests).
  Original assembly retained in asm/FUN_24dd_3ed3.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_3ed3(uint param_1,uint param_2,byte *param_3,byte *param_4)
//
// {
//   byte *pbVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//
//   pbVar4 = (byte *)param_4;
//   if ((int)param_2 < 1) {
//     param_2 = 1;
//   }
//   pbVar3 = (byte *)param_3 + param_2;
//   if (*param_3 < param_2) {
//     uVar2 = 0;
//   }
//   else {
//     uVar2 = (*param_3 - param_2) + 1;
//     if ((int)param_1 < 0) {
//       param_1 = 0;
//     }
//     if (param_1 < uVar2) {
//       uVar2 = param_1;
//     }
//   }
//   *param_4 = (byte)uVar2;
//   for (; pbVar4 = pbVar4 + 1, uVar2 != 0; uVar2 = uVar2 - 1) {
//     pbVar1 = pbVar3;
//     pbVar3 = pbVar3 + 1;
//     *pbVar4 = *pbVar1;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3ed3(param_1, param_2: Word; param_3, param_4: Pointer);
var
  sourceByte: PByte;
  destinationByte: PByte;
  sourceLength: Byte;
  startPosition: Word;
  sourceOffset: Word;
  maxBytes: Word;
  availableBytes: Word;
  remainingBytes: Byte;
begin
  sourceByte := PByte(param_3);
  destinationByte := PByte(param_4);
  sourceLength := sourceByte^;

  if SmallInt(param_2) < 1 then
    startPosition := 1
  else
    startPosition := param_2;
  sourceOffset := startPosition;
  while sourceOffset <> 0 do
  begin
    Inc(sourceByte);
    Dec(sourceOffset);
  end;

  if SmallInt(param_1) < 0 then
    maxBytes := 0
  else
    maxBytes := param_1;

  availableBytes := 0;
  if startPosition <= sourceLength then
    availableBytes := sourceLength - startPosition + 1;
  if availableBytes > maxBytes then
    availableBytes := maxBytes;

  remainingBytes := Byte(availableBytes);
  destinationByte^ := remainingBytes;
  Inc(destinationByte);
  while remainingBytes <> 0 do
  begin
    destinationByte^ := sourceByte^;
    Inc(sourceByte);
    Inc(destinationByte);
    Dec(remainingBytes);
  end;
end;
