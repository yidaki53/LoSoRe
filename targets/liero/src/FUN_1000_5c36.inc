{ liero::FUN_1000_5c36 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_5c36.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_5c36.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_5c36(int param_1)
// 
// {
//   uint *puVar1;
//   uint uVar2;
//   uint uVar3;
//   undefined4 uVar4;
//   byte bVar5;
//   char cVar6;
//   int iVar7;
//   char *pcVar8;
//   undefined2 uVar9;
//   undefined2 unaff_DS;
//   undefined4 local_6;
//   
//   FUN_24dd_0530();
//   uVar9 = (undefined2)((ulong)*(undefined4 *)0x6690 >> 0x10);
//   pcVar8 = (char *)((int)*(undefined4 *)0x6690 + param_1 * 0x11);
//   local_6 = (char *)CONCAT22(uVar9,pcVar8);
//   uVar3 = *(uint *)(pcVar8 + 9);
//   iVar7 = *(int *)(pcVar8 + 0xb);
//   puVar1 = (uint *)(pcVar8 + 1);
//   uVar2 = *puVar1;
//   *puVar1 = *puVar1 + uVar3;
//   *(uint *)(pcVar8 + 3) = *(int *)(pcVar8 + 3) + iVar7 + (uint)CARRY2(uVar2,uVar3);
//   uVar3 = *(uint *)(pcVar8 + 0xd);
//   iVar7 = *(int *)(pcVar8 + 0xf);
//   puVar1 = (uint *)(pcVar8 + 5);
//   uVar2 = *puVar1;
//   *puVar1 = *puVar1 + uVar3;
//   *(uint *)(pcVar8 + 7) = *(int *)(pcVar8 + 7) + iVar7 + (uint)CARRY2(uVar2,uVar3);
//   if ((((*(int *)(pcVar8 + 3) < 0) || (0x1f7 < *(int *)(pcVar8 + 3))) || (*(int *)(pcVar8 + 7) < 0))
//      || (0x15d < *(int *)(pcVar8 + 7))) {
//     *local_6 = '\0';
//   }
//   if (*local_6 != '\0') {
//     iVar7 = 0x20;
//     bVar5 = FUN_24dd_4161();
//     if ((*(byte *)(iVar7 + 0x14c0) & bVar5) != 0) {
//       puVar1 = (uint *)(pcVar8 + 0xd);
//       uVar2 = *puVar1;
//       *puVar1 = *puVar1 + 1000;
//       *(uint *)(pcVar8 + 0xf) = *(int *)(pcVar8 + 0xf) + (uint)(0xfc17 < uVar2);
//     }
//     uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(pcVar8 + 7) * 4);
//     bVar5 = *(byte *)((int)uVar4 + *(int *)(pcVar8 + 3));
//     if ((bVar5 == 0) || ((2 < bVar5 && ((bVar5 < 0x4d || (0x4f < bVar5)))))) {
//       if (*(int *)(pcVar8 + 7) < 0x15e) {
//         iVar7 = 0x20;
//         bVar5 = FUN_24dd_4161();
//         if ((*(byte *)(iVar7 + 0x6624) & bVar5) == 0) {
//           iVar7 = 0x20;
//           bVar5 = FUN_24dd_4161();
//           if ((*(byte *)(iVar7 + 0x14a0) & bVar5) != 0) {
//             cVar6 = FUN_24dd_4654(3);
//             uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(pcVar8 + 7) * 4);
//             *(char *)((int)uVar4 + *(int *)(pcVar8 + 3)) = cVar6 + 'U';
//             *local_6 = '\0';
//           }
//         }
//         else {
//           cVar6 = FUN_24dd_4654(3);
//           uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(pcVar8 + 7) * 4);
//           *(char *)((int)uVar4 + *(int *)(pcVar8 + 3)) = cVar6 + 'R';
//           *local_6 = '\0';
//         }
//       }
//       else {
//         *local_6 = '\0';
//       }
//     }
//     else {
//       cVar6 = FUN_24dd_4654(3);
//       uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + *(int *)(pcVar8 + 7) * 4);
//       *(char *)((int)uVar4 + *(int *)(pcVar8 + 3)) = cVar6 + 'M';
//       *local_6 = '\0';
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_5c36;
begin
  { TODO: translate from asm/FUN_1000_5c36.s — UNMATCHED until an oracle passes }
end;

