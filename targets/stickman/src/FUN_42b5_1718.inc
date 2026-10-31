{ stickman::FUN_42b5_1718 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1718.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1718.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// uint __cdecl16near FUN_42b5_1718(void)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   uint in_AX;
//   uint uVar3;
//   char cVar4;
//   uint in_DX;
//   uint uVar5;
//   uint uVar6;
//   uint uVar7;
//   uint in_BX;
//   uint uVar8;
//   uint uVar9;
//   uint uVar10;
//   bool bVar11;
//   
//   cVar4 = (char)in_AX;
//   if (cVar4 != '\0') {
//     uVar5 = in_DX | 0x8000;
//     uVar6 = uVar5 >> 2;
//     uVar8 = (uint)(((ulong)((in_DX & 2) != 0) << 0x10 |
//                    (ulong)(CONCAT12((in_DX & 1) != 0,in_BX) >> 1)) >> 1);
//     uVar1 = (uint)(((ulong)((in_BX & 2) != 0) << 0x10 |
//                    (ulong)((CONCAT12((in_BX & 1) != 0,in_AX) & 0xffff00) >> 1)) >> 1);
//     uVar3 = uVar1 + (in_AX & 0xff00);
//     uVar1 = (uint)CARRY2(uVar1,in_AX & 0xff00);
//     uVar2 = uVar8 + in_BX;
//     uVar9 = uVar2 + uVar1;
//     uVar1 = (uint)(CARRY2(uVar8,in_BX) || CARRY2(uVar2,uVar1));
//     uVar2 = uVar6 + uVar5;
//     uVar7 = uVar2 + uVar1;
//     uVar8 = uVar7;
//     uVar10 = uVar9;
//     if (CARRY2(uVar6,uVar5) || CARRY2(uVar2,uVar1)) {
//       uVar8 = (uint)(CONCAT12(CARRY2(uVar6,uVar5) || CARRY2(uVar2,uVar1),uVar7) >> 1);
//       uVar10 = (uint)(CONCAT12((uVar7 & 1) != 0,uVar9) >> 1);
//       uVar3 = (uint)(CONCAT12((uVar9 & 1) != 0,uVar3) >> 1);
//       bVar11 = cVar4 == -1;
//       cVar4 = cVar4 + '\x01';
//       if (bVar11) {
//         return uVar3;
//       }
//     }
//     in_AX = uVar3 + 0x80;
//     if ((!CARRY2(uVar8,(uint)CARRY2(uVar10,(uint)(0xff7f < uVar3)))) ||
//        (bVar11 = cVar4 != -1, cVar4 = cVar4 + '\x01', bVar11)) {
//       in_AX = CONCAT11((char)(in_AX >> 8),cVar4 + '\x03');
//     }
//   }
//   return in_AX;
// }
// 
// --- end reference ---
function FUN_42b5_1718: Word;
begin
  { TODO: translate from asm/FUN_42b5_1718.s — UNMATCHED until an oracle passes }
end;

