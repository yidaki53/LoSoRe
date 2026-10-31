{ liero::FUN_24dd_3f14 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer tests).
  Original assembly retained in asm/FUN_24dd_3f14.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_3f14(byte *param_1,byte *param_2)
//
// {
//   byte bVar1;
//   byte bVar2;
//   byte bVar3;
//   uint uVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//
//   pbVar5 = (byte *)param_1;
//   bVar2 = *param_2;
//   bVar3 = *param_1;
//   bVar1 = *param_2;
//   *param_2 = *param_2 + bVar3;
//   if (CARRY1(bVar1,bVar3)) {
//     *param_2 = 0xff;
//     bVar3 = ~bVar2;
//   }
//   pbVar6 = (byte *)param_2 + bVar2;
//   uVar4 = (uint)bVar3;
//   while( true ) {
//     pbVar6 = pbVar6 + 1;
//     pbVar5 = pbVar5 + 1;
//     if (uVar4 == 0) break;
//     uVar4 = uVar4 - 1;
//     *pbVar6 = *pbVar5;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3f14(param_1, param_2: Pointer);
var
  sourceByte: PByte;
  destinationByte: PByte;
  originalLength: Byte;
  sourceLength: Byte;
  copyLength: Byte;
  remaining: Byte;
begin
  sourceByte := PByte(param_1);
  destinationByte := PByte(param_2);
  originalLength := destinationByte^;
  sourceLength := sourceByte^;
  Inc(sourceByte);

  copyLength := sourceLength;
  if sourceLength > 255 - originalLength then
  begin
    copyLength := 255 - originalLength;
    destinationByte^ := 255;
  end
  else
    destinationByte^ := originalLength + sourceLength;

  Inc(destinationByte, originalLength + 1);
  remaining := copyLength;
  while remaining <> 0 do
  begin
    destinationByte^ := sourceByte^;
    Inc(sourceByte);
    Inc(destinationByte);
    Dec(remaining);
  end;
end;
