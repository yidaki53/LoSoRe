{ liero::FUN_1ea2_01a8 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ea2_01a8.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ea2_01a8.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_1ea2_01a8(undefined2 *param_1,int param_2,uint param_3,int param_4,undefined2 *param_5)
// 
// {
//   undefined2 *puVar1;
//   undefined2 *puVar2;
//   undefined2 *puVar3;
//   undefined2 *puVar4;
//   uint uVar5;
//   uint uVar6;
//   undefined2 *puVar7;
//   undefined2 *puVar8;
//   undefined2 uVar9;
//   undefined2 uVar10;
//   
//   uVar10 = (undefined2)((ulong)param_5 >> 0x10);
//   puVar7 = (undefined2 *)param_5;
//   uVar9 = (undefined2)((ulong)param_1 >> 0x10);
//   puVar8 = (undefined2 *)param_1;
//   uVar5 = param_3 >> 1;
//   uVar6 = uVar5;
//   if ((param_3 & 1) == 0) {
//     do {
//       for (; uVar6 != 0; uVar6 = uVar6 - 1) {
//         puVar4 = puVar8;
//         puVar8 = puVar8 + 1;
//         puVar2 = puVar7;
//         puVar7 = puVar7 + 1;
//         *puVar4 = *puVar2;
//       }
//       puVar8 = (undefined2 *)((int)puVar8 + (0x140 - param_3));
//       puVar7 = (undefined2 *)((int)puVar7 + (param_4 - param_3));
//       param_2 = param_2 + -1;
//       uVar6 = uVar5;
//     } while (param_2 != 0);
//   }
//   else {
//     do {
//       puVar3 = (undefined2 *)((int)puVar8 + 1);
//       puVar1 = (undefined2 *)((int)puVar7 + 1);
//       *(undefined1 *)puVar8 = *(undefined1 *)puVar7;
//       for (uVar6 = uVar5; uVar6 != 0; uVar6 = uVar6 - 1) {
//         puVar4 = puVar3;
//         puVar3 = puVar3 + 1;
//         puVar2 = puVar1;
//         puVar1 = puVar1 + 1;
//         *puVar4 = *puVar2;
//       }
//       puVar8 = (undefined2 *)((int)puVar3 + (0x140 - param_3));
//       puVar7 = (undefined2 *)((int)puVar1 + (param_4 - param_3));
//       param_2 = param_2 + -1;
//     } while (param_2 != 0);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ea2_01a8(param_1: Pointer; param_2: Integer; param_3: Word; param_4: Integer; param_5: Pointer);
var
  destinationBytes: PByte;
  sourceBytes: PByte;
  rowCount: Word;
  byteIndex: Word;
begin
  destinationBytes := PByte(param_1);
  sourceBytes := PByte(param_5);
  rowCount := Word(param_2);
  repeat
    for byteIndex := 1 to param_3 do
    begin
      destinationBytes^ := sourceBytes^;
      Inc(destinationBytes);
      Inc(sourceBytes);
    end;
    Inc(destinationBytes, $0140 - param_3);
    Inc(sourceBytes, param_4 - param_3);
    Dec(rowCount);
  until rowCount = 0;
end;
