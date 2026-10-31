{ stickman::FUN_1000_2a76 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_2a76.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_2a76.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_2a76(void)
// 
// {
//   char cVar1;
//   int iVar2;
//   uint uVar3;
//   undefined2 uVar4;
//   int iVar5;
//   int iVar6;
//   int iVar7;
//   int extraout_DX;
//   undefined2 unaff_DS;
//   int *local_e;
//   uint local_4;
//   
//   FUN_42b5_04df();
//   local_4 = 1;
//   do {
//     iVar6 = (int)((ulong)local_4 * 0x275 >> 0x10);
//     iVar2 = (int)((ulong)local_4 * 0x275);
//     _local_e = (int *)CONCAT22(unaff_DS,(int *)(iVar2 + 0x459));
//     iVar7 = iVar6;
//     if (*_local_e != 0) {
//       uVar3 = FUN_4170_0096();
//       iVar7 = iVar6;
//       if ((*(int *)(iVar2 + 0x46b) <= iVar6) &&
//          ((*(int *)(iVar2 + 0x46b) < iVar6 || (*(uint *)(iVar2 + 0x469) <= uVar3)))) {
//         uVar3 = FUN_4170_0096();
//         iVar7 = *(int *)(iVar2 + 0x46b) + (uint)(0xfffa < *(uint *)(iVar2 + 0x469));
//         if ((iVar6 <= iVar7) && ((iVar6 < iVar7 || (uVar3 <= *(uint *)(iVar2 + 0x469) + 5))))
//         goto LAB_1000_2b8e;
//       }
//       cVar1 = FUN_3de3_0a62();
//       if (cVar1 == '\0') {
//         uVar4 = FUN_4170_0096();
//         *(undefined2 *)(iVar2 + 0x469) = uVar4;
//         *(int *)(iVar2 + 0x46b) = iVar7;
//         FUN_3de3_0b67(*(int *)(iVar2 + 0x45b) + 1,*_local_e);
//         FUN_3de3_002d(iVar2 + 0x58e,unaff_DS);
//         iVar7 = *_local_e + *(int *)(iVar2 + 0x45f);
//         cVar1 = FUN_1000_287f(local_4,iVar7);
//         if (cVar1 == '\0') {
//           *(int *)(iVar2 + 0x45f) = -*(int *)(iVar2 + 0x45f);
//         }
//         else {
//           *_local_e = iVar7;
//         }
//         FUN_3de3_0b67(*(int *)(iVar2 + 0x45b) + 1,*_local_e);
//         FUN_3de3_002d(iVar2 + 0x48e,unaff_DS);
//         FUN_3de3_002d(0x2a71,0x3de3);
//         iVar7 = extraout_DX;
//       }
//     }
// LAB_1000_2b8e:
//     if (local_4 == 10) break;
//     local_4 = local_4 + 1;
//   } while( true );
//   if (((*(char *)0x541 == '\x01') && (cVar1 = FUN_3de3_0a62(), cVar1 == '\0')) &&
//      (*(int *)0xaaec != 0)) {
//     FUN_405f_017d();
//     iVar6 = FUN_4170_0096();
//     iVar2 = iVar7;
//     do {
//       iVar5 = FUN_4170_0096();
//       if (iVar2 != iVar7) break;
//     } while (iVar5 == iVar6);
//     iVar6 = FUN_4170_0096();
//     iVar7 = iVar2;
//     do {
//       iVar5 = FUN_4170_0096();
//       if (iVar7 != iVar2) {
//         return;
//       }
//     } while (iVar5 == iVar6);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_2a76;
begin
  { TODO: translate from asm/FUN_1000_2a76.s — UNMATCHED until an oracle passes }
end;

