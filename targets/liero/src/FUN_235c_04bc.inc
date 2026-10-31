{ liero::FUN_235c_04bc — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_04bc.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_04bc.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_235c_04bc(byte *param_1)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   uint uVar3;
//   byte *pbVar4;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   byte local_102;
//   byte abStack_101 [255];
//   
//   pbVar4 = (byte *)param_1;
//   local_102 = *param_1;
//   pbVar2 = abStack_101;
//   for (uVar3 = (uint)local_102; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar4;
//   }
//   *(undefined1 *)0x7690 = 1;
//   FUN_24dd_3eaf(0xff,0x7692,unaff_DS,&local_102,unaff_SS);
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_04bc(param_1: Pointer);
var
  source: PByte;
  localString: array[0..255] of Byte;
  index: Integer;
  stringLength: Byte;
begin
  source := PByte(param_1);
  stringLength := source^;
  localString[0] := stringLength;
  Inc(source);
  for index := 1 to Integer(stringLength) do
  begin
    localString[index] := source^;
    Inc(source);
  end;
  DosMemory[$7690] := 1;
  FUN_24dd_3eaf($FF, @DosMemory[$7692], @localString[0]);
end;
