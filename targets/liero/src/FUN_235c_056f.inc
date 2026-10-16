{ liero::FUN_235c_056f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_056f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_056f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_235c_056f(byte *param_1)
// 
// {
//   bool bVar1;
//   byte *pbVar2;
//   char cVar3;
//   undefined2 uVar4;
//   uint uVar5;
//   undefined2 extraout_DX;
//   undefined2 uVar6;
//   byte *pbVar7;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   int local_120;
//   int local_11e;
//   undefined1 local_11c [8];
//   undefined2 local_114;
//   undefined2 local_112;
//   undefined2 local_110;
//   undefined2 local_10e;
//   undefined1 local_10c [8];
//   int local_104;
//   byte local_102 [256];
//   
//   pbVar7 = (byte *)param_1;
//   pbVar2 = local_102;
//   local_102[0] = *param_1;
//   for (uVar5 = (uint)*param_1; pbVar2 = pbVar2 + 1, pbVar7 = pbVar7 + 1, uVar5 != 0;
//       uVar5 = uVar5 - 1) {
//     *pbVar2 = *pbVar7;
//   }
//   if (*(char *)0x7690 == '\0') {
//     FUN_24dd_3b22(local_102,unaff_SS,0x7792,unaff_DS);
//     FUN_24dd_3b5d(1,0x7792,unaff_DS);
//     FUN_24dd_04f4();
//     FUN_24dd_486c(0x7792,unaff_DS);
//     uVar6 = extraout_DX;
//     uVar4 = FUN_24dd_04f4();
//     *(undefined2 *)0x7812 = uVar4;
//     *(undefined2 *)0x7814 = uVar6;
//   }
//   else {
//     local_120 = 1;
//     while( true ) {
//       if ((int)(uint)local_102[0] < local_120) {
//         local_10c[local_120 + -1] = 0;
//       }
//       else {
//         local_10c[local_120 + -1] = local_102[local_120];
//       }
//       if (local_120 == 8) break;
//       local_120 = local_120 + 1;
//     }
//     FUN_24dd_3b22(0x7692,unaff_DS,0x7792,unaff_DS);
//     FUN_24dd_3b5d(1,0x7792,unaff_DS);
//     FUN_24dd_04f4();
//     FUN_24dd_3c48(0,0,2,&local_104,unaff_SS,0x7792,unaff_DS);
//     FUN_24dd_04f4();
//     bVar1 = false;
//     local_11e = 0;
//     while ((!bVar1 && (local_11e < local_104))) {
//       local_11e = local_11e + 1;
//       FUN_24dd_3c48(0,0,0x10,local_11c,unaff_SS,0x7792,unaff_DS);
//       FUN_24dd_04f4();
//       cVar3 = FUN_235c_0502(local_10c,unaff_SS,local_11c,unaff_SS);
//       if (cVar3 != '\0') {
//         bVar1 = true;
//       }
//     }
//     if (bVar1) {
//       FUN_24dd_3cb0(local_114,local_112,0x7792,unaff_DS);
//       FUN_24dd_04f4();
//       *(undefined2 *)0x7812 = local_110;
//       *(undefined2 *)0x7814 = local_10e;
//     }
//     else {
//       FUN_24dd_0116();
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_056f;
begin
  { TODO: translate from asm/FUN_235c_056f.s — UNMATCHED until an oracle passes }
end;

