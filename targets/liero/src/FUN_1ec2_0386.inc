{ liero::FUN_1ec2_0386 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0386.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0386.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ec2_0386(char param_1,char param_2,undefined4 param_3,byte *param_4,int param_5,int param_6)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   int iVar3;
//   byte *pbVar4;
//   byte *pbVar5;
//   undefined2 uVar6;
//   undefined2 uVar7;
//   undefined2 unaff_SS;
//   int local_108;
//   int local_104;
//   byte local_102 [256];
//   
//   pbVar5 = local_102;
//   pbVar4 = (byte *)param_4;
//   for (iVar3 = 0x100; iVar3 != 0; iVar3 = iVar3 + -1) {
//     pbVar2 = pbVar5;
//     pbVar5 = pbVar5 + 1;
//     pbVar1 = pbVar4;
//     pbVar4 = pbVar4 + 1;
//     *pbVar2 = *pbVar1;
//   }
//   uVar6 = (undefined2)param_3;
//   uVar7 = (undefined2)((ulong)param_3 >> 0x10);
//   if (param_1 == '\0') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x74 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 5,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x74 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 5,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_1 == '\x01') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x72 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 3,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x72 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 3,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_1 == '\x02') {
//     if (param_2 == '\0') {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x70 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 1,
//                           param_5 + local_108,(0xe - local_104) + param_6);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//     else {
//       local_108 = 0;
//       while( true ) {
//         local_104 = 2;
//         while( true ) {
//           if (0x70 < local_102[local_108 * 0x10 + local_104]) {
//             FUN_1ec2_0dc8(uVar6,uVar7,local_102[local_108 * 0x10 + local_104] - 1,
//                           param_5 + local_108,param_6 + local_104);
//           }
//           if (local_104 == 0xd) break;
//           local_104 = local_104 + 1;
//         }
//         if (local_108 == 0xf) break;
//         local_108 = local_108 + 1;
//       }
//     }
//   }
//   else if (param_2 == '\0') {
//     local_108 = 0;
//     while( true ) {
//       for (local_104 = 2; iVar3 = (0xe - local_104) + param_6,
//           FUN_1ec2_0dc8(uVar6,uVar7,
//                         CONCAT11((char)((uint)iVar3 >> 8),local_102[local_108 * 0x10 + local_104]),
//                         param_5 + local_108,iVar3), local_104 != 0xd; local_104 = local_104 + 1) {
//       }
//       if (local_108 == 0xf) break;
//       local_108 = local_108 + 1;
//     }
//   }
//   else {
//     local_108 = 0;
//     while( true ) {
//       for (local_104 = 2;
//           FUN_1ec2_0dc8(uVar6,uVar7,
//                         CONCAT11((char)((uint)(param_6 + local_104) >> 8),
//                                  local_102[local_108 * 0x10 + local_104]),param_5 + local_108,
//                         param_6 + local_104), local_104 != 0xd; local_104 = local_104 + 1) {
//       }
//       if (local_108 == 0xf) break;
//       local_108 = local_108 + 1;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0386(param_1, param_2: Char; param_3: Longint; param_4: Pointer; param_5, param_6: Integer);
var
  bitmap: array[0..255] of Byte;
  source: ^Byte;
  rowIndex: Integer;
  columnIndex: Integer;
  pixelColor: Byte;
  minimumColor: Byte;
begin
  source := param_4;
  for rowIndex := 0 to 255 do
  begin
    bitmap[rowIndex] := source^;
    Inc(source);
  end;
  if (param_1 = #0) then
    minimumColor := $75
  else if param_1 = #1 then
    minimumColor := $73
  else
    minimumColor := $71;

  for rowIndex := 0 to 15 do
    for columnIndex := 2 to 13 do
    begin
      pixelColor := bitmap[rowIndex * 16 + columnIndex];
      if param_1 = #0 then
      begin
        if pixelColor <= minimumColor then
          Continue;
        Dec(pixelColor, 5);
      end
      else if param_1 = #1 then
      begin
        if pixelColor <= minimumColor then
          Continue;
        Dec(pixelColor, 3);
      end
      else if param_1 = #2 then
      begin
        if pixelColor <= minimumColor then
          Continue;
        Dec(pixelColor, 1);
      end;

      if param_2 = #0 then
        FUN_1ec2_0dc8(param_3, Char(pixelColor), param_5 + rowIndex,
          (14 - columnIndex) + param_6)
      else
        FUN_1ec2_0dc8(param_3, Char(pixelColor), param_5 + rowIndex,
          param_6 + columnIndex);
    end;
end;
