{ liero::FUN_24dd_3eaf — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer tests).
  Original assembly retained in asm/FUN_24dd_3eaf.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_3eaf(byte param_1,byte *param_2,byte *param_3)
//
// {
//   byte bVar1;
//   uint uVar2;
//   byte *pbVar3;
//   byte *pbVar4;
//
//   pbVar3 = (byte *)param_3;
//   pbVar4 = (byte *)param_2;
//   bVar1 = *param_3;
//   if (param_1 < *param_3) {
//     bVar1 = param_1;
//   }
//   *param_2 = bVar1;
//   uVar2 = (uint)bVar1;
//   while( true ) {
//     pbVar4 = pbVar4 + 1;
//     pbVar3 = pbVar3 + 1;
//     if (uVar2 == 0) break;
//     uVar2 = uVar2 - 1;
//     *pbVar4 = *pbVar3;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3eaf(param_1: Byte; param_2, param_3: Pointer);
var
  sourceByte: PByte;
  destinationByte: PByte;
  remainingBytes: Byte;
begin
  sourceByte := PByte(param_3);
  destinationByte := PByte(param_2);
  remainingBytes := sourceByte^;
  if remainingBytes > param_1 then
    remainingBytes := param_1;
  destinationByte^ := remainingBytes;
  Inc(sourceByte);
  Inc(destinationByte);
  while remainingBytes <> 0 do
  begin
    destinationByte^ := sourceByte^;
    Inc(sourceByte);
    Inc(destinationByte);
    Dec(remainingBytes);
  end;
end;
