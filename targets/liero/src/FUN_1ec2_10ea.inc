{ liero::FUN_1ec2_10ea — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_10ea.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_10ea.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_10ea(int param_1,byte *param_2)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   byte bVar3;
//   int iVar4;
//   byte *pbVar5;
//   byte *pbVar6;
//   undefined2 unaff_SS;
//   uint local_30a;
//   uint local_308;
//   uint local_306;
//   byte local_303;
//   byte local_302 [768];
//   
//   pbVar6 = local_302;
//   pbVar5 = (byte *)param_2;
//   for (iVar4 = 0x300; iVar4 != 0; iVar4 = iVar4 + -1) {
//     pbVar2 = pbVar6;
//     pbVar6 = pbVar6 + 1;
//     pbVar1 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   local_303 = 0;
//   while( true ) {
//     local_306 = (uint)local_302[(uint)local_303 * 3] * param_1 >> 5;
//     local_308 = (uint)local_302[(uint)local_303 * 3 + 1] * param_1 >> 5;
//     local_30a = (uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 5;
//     if (0x3f < local_306) {
//       local_306 = 0x3f;
//     }
//     if (0x3f < local_308) {
//       local_308 = 0x3f;
//     }
//     if (0x3f < local_30a) {
//       local_30a = 0x3f;
//     }
//     bVar3 = (byte)((uint)local_302[(uint)local_303 * 3 + 2] * param_1 >> 0xd);
//     FUN_1ec2_10cf(CONCAT11(bVar3,(undefined1)local_30a),CONCAT11(bVar3,(undefined1)local_308),
//                   CONCAT11(bVar3,(undefined1)local_306),CONCAT11(bVar3,local_303));
//     if (local_303 == 0xff) break;
//     local_303 = local_303 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_10ea(param_1: Integer; param_2: Pointer);
var
  source: PByte;
  paletteData: array[0..767] of Byte;
  index: Integer;
  redValue: Longint;
  greenValue: Longint;
  blueValue: Longint;
begin
  source := PByte(param_2);
  for index := 0 to 767 do
  begin
    paletteData[index] := source^;
    Inc(source);
  end;

  for index := 0 to 255 do
  begin
    redValue := (Longint(paletteData[index * 3]) * param_1) shr 5;
    greenValue := (Longint(paletteData[index * 3 + 1]) * param_1) shr 5;
    blueValue := (Longint(paletteData[index * 3 + 2]) * param_1) shr 5;
    if redValue > $3F then redValue := $3F;
    if greenValue > $3F then greenValue := $3F;
    if blueValue > $3F then blueValue := $3F;
    FUN_1ec2_10cf(Byte(blueValue), Byte(greenValue), Byte(redValue), Byte(index));
  end;
end;
