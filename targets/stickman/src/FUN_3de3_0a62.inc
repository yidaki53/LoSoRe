{ stickman::FUN_3de3_0a62 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_3de3_0a62.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_3de3_0a62.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __cdecl16far FUN_3de3_0a62(void)
// 
// {
//   char cVar1;
//   undefined2 uVar2;
//   uint uVar3;
//   int in_DX;
//   int iVar4;
//   undefined2 unaff_DS;
//   bool bVar5;
//   uint local_8;
//   int local_6;
//   undefined1 local_3;
//   
//   FUN_42b5_04df();
//   cVar1 = FUN_405f_0234();
//   if (cVar1 == '\0') {
//     local_3 = 0;
//     local_8 = FUN_4170_0096();
//     if ((in_DX < *(int *)0xa7d4) ||
//        ((local_6 = in_DX, in_DX <= *(int *)0xa7d4 && (local_8 < *(uint *)0xa7d2)))) {
//       bVar5 = 0x7a2 < local_8;
//       local_8 = local_8 - 0x7a3;
//       local_6 = in_DX + 0x17 + (uint)bVar5;
//     }
//     uVar3 = *(uint *)0xa7d2 + *(uint *)0x132;
//     iVar4 = (*(int *)0xa7d4 + *(int *)0x134 + (uint)CARRY2(*(uint *)0xa7d2,*(uint *)0x132)) -
//             (uint)(uVar3 < 0x111);
//     if (((iVar4 < local_6) || ((iVar4 <= local_6 && (uVar3 - 0x111 < local_8)))) &&
//        ((*(int *)0x14c != *(int *)0xa7d4 || (*(int *)0x14a != *(int *)0xa7d2)))) {
//       uVar2 = *(undefined2 *)0xa7d4;
//       *(undefined2 *)0x14a = *(undefined2 *)0xa7d2;
//       *(undefined2 *)0x14c = uVar2;
//       FUN_3de3_002d(0xa12,0x4170);
//     }
//     iVar4 = *(int *)0xa7d4 + *(int *)0x134 + (uint)CARRY2(*(uint *)0xa7d2,*(uint *)0x132);
//     if ((iVar4 < local_6) || ((iVar4 <= local_6 && (*(uint *)0xa7d2 + *(uint *)0x132 < local_8)))) {
//       FUN_3de3_0278(0xa49,0x4170);
//     }
//   }
//   else {
//     local_3 = 1;
//     uVar2 = FUN_4170_0096();
//     *(undefined2 *)0xa7d2 = uVar2;
//     *(int *)0xa7d4 = in_DX;
//   }
//   return local_3;
// }
// 
// --- end reference ---
function FUN_3de3_0a62: Byte;
begin
  { TODO: translate from asm/FUN_3de3_0a62.s — UNMATCHED until an oracle passes }
end;

