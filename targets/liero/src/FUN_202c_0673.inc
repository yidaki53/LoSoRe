{ liero::FUN_202c_0673 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0673.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0673.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// int __stdcall16far FUN_202c_0673(byte *param_1)
// 
// {
//   byte *pbVar1;
//   uint uVar2;
//   byte *pbVar3;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   int local_108;
//   uint local_106;
//   byte local_104 [258];
//   
//   pbVar3 = (byte *)param_1;
//   local_104[0] = *param_1;
//   pbVar1 = local_104;
//   for (uVar2 = (uint)local_104[0]; pbVar1 = pbVar1 + 1, pbVar3 = pbVar3 + 1, uVar2 != 0;
//       uVar2 = uVar2 - 1) {
//     *pbVar1 = *pbVar3;
//   }
//   local_108 = 1;
//   if (local_104[0] != 0) {
//     local_106 = 1;
//     while( true ) {
//       if (local_104[local_106] == 0xff) {
//         local_106 = local_106 + 2;
//       }
//       local_108 = local_108 + (uint)*(byte *)((local_104[local_106] - 2) * 0x40 + 0x19e5);
//       if (local_106 == local_104[0]) break;
//       local_106 = local_106 + 1;
//     }
//   }
//   return local_108 + 2;
// }
// 
// --- end reference ---
function FUN_202c_0673(param_1: Pointer): Integer;
var
  sourceText: PByte;
  localText: array[0..257] of Byte;
  textLength: Byte;
  position: Word;
  glyphIndex: Word;
  glyphWidth: Byte;
  accumulatedWidth: Word;
begin
  { Assembly copies the Pascal string to its stack frame before walking it. }
  sourceText := PByte(param_1);
  textLength := sourceText^;
  localText[0] := textLength;
  Inc(sourceText);
  position := 1;
  while position <= textLength do
  begin
    localText[position] := sourceText^;
    Inc(sourceText);
    Inc(position);
  end;

  accumulatedWidth := 1;
  if textLength <> 0 then
  begin
    position := 1;
    while True do
    begin
      if localText[position] = $FF then
        Inc(position, 2);

      glyphIndex := Word(localText[position]);
      Dec(glyphIndex);
      Dec(glyphIndex);
      glyphWidth := CodeMemory[Word($19E5 + Word(glyphIndex shl 6))];
      accumulatedWidth := Word(accumulatedWidth + glyphWidth);

      if position = textLength then
        Break;
      Inc(position);
    end;
  end;

  accumulatedWidth := Word(accumulatedWidth + 2);
  RegisterAX := accumulatedWidth;
  FUN_202c_0673 := SmallInt(accumulatedWidth);
end;
