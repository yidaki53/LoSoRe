{ liero::FUN_235c_10a3 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_10a3.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_10a3.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_235c_10a3(byte param_1)
// 
// {
//   char *pcVar1;
//   uint uVar2;
//   char *pcVar3;
//   int iVar4;
//   int iVar5;
//   int *piVar6;
//   undefined2 uVar7;
//   undefined2 unaff_DS;
//   undefined4 local_8;
//   int local_4;
//   
//   iVar4 = (uint)param_1 * 10;
//   local_8 = (undefined4 *)CONCAT22(unaff_DS,(undefined4 *)(iVar4 + 0x6804));
//   if (*(char *)(iVar4 + 0x680d) == '\0') {
//     uVar7 = (undefined2)((ulong)*local_8 >> 0x10);
//     iVar5 = (int)*local_8;
//     uVar2 = *(uint *)(iVar5 + 6);
//     iVar5 = (*(int *)(iVar5 + 8) - *(int *)(iVar4 + 0x680b)) -
//             (uint)(uVar2 < *(uint *)(iVar4 + 0x6809));
//     if ((iVar5 < 1) && ((iVar5 < 0 || (uVar2 - *(uint *)(iVar4 + 0x6809) < 0x201)))) {
//       local_4 = *(int *)((int)*local_8 + 6) - *(int *)(iVar4 + 0x6809);
//     }
//     else {
//       local_4 = 0x200;
//     }
//   }
//   else {
//     local_4 = 0x200;
//   }
//   FUN_235c_0f57(*(undefined1 *)((uint)param_1 * 10 + 0x680d),local_4,(uint)param_1 * 10 + 0x6809,
//                 unaff_DS,*(undefined2 *)((uint)param_1 * 10 + 0x6804),
//                 *(undefined2 *)((uint)param_1 * 10 + 0x6806));
//   pcVar3 = (char *)0x6856;
//   piVar6 = (int *)0x6a58;
//   do {
//     pcVar1 = pcVar3;
//     pcVar3 = pcVar3 + 1;
//     *piVar6 = *piVar6 + (int)*pcVar1;
//     piVar6 = piVar6 + 1;
//     local_4 = local_4 + -1;
//   } while (local_4 != 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_10a3;
begin
  { TODO: translate from asm/FUN_235c_10a3.s — UNMATCHED until an oracle passes }
end;

