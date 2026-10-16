{ liero::FUN_235c_0bbc — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0bbc.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0bbc.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_235c_0bbc(void)
// 
// {
//   undefined1 uVar1;
//   uint uVar2;
//   undefined2 uVar3;
//   int iVar4;
//   undefined2 unaff_DS;
//   undefined4 uVar5;
//   uint local_4;
//   
//   for (local_4 = 0; FUN_235c_091d(local_4 & 0xff), local_4 != 7; local_4 = local_4 + 1) {
//   }
//   *(undefined1 *)0x67ce = 0;
//   if (*(char *)0x67cd == '\0') {
//     uVar5 = FUN_24dd_028a(0x800);
//     *(undefined2 *)0x6e58 = (int)uVar5;
//     *(undefined2 *)0x6e5a = (int)((ulong)uVar5 >> 0x10);
//     FUN_235c_0aff(*(undefined2 *)0x6e58,*(undefined2 *)0x6e5a);
//     uVar2 = 0;
//     iVar4 = 1;
//     FUN_24dd_3dbd();
//     if ((int)(iVar4 + (uint)(0xfbff < uVar2)) < 1) {
//       uVar3 = *(undefined2 *)0x6e5a;
//       *(undefined2 *)0x6e5c = *(undefined2 *)0x6e58;
//       *(undefined2 *)0x6e5e = uVar3;
//     }
//     else {
//       uVar5 = FUN_235c_0b33((int)*(undefined4 *)0x6e58 + 0x400,
//                             (int)((ulong)*(undefined4 *)0x6e58 >> 0x10));
//       *(undefined2 *)0x6e5c = (int)uVar5;
//       *(undefined2 *)0x6e5e = (int)((ulong)uVar5 >> 0x10);
//     }
//     local_4 = 1;
//     while( true ) {
//       uVar5 = FUN_235c_0b33((int)*(undefined4 *)0x6e5c + local_4 * 0x200 + -0x200,
//                             (int)((ulong)*(undefined4 *)0x6e5c >> 0x10));
//       *(undefined2 *)(local_4 * 4 + 0x6e60) = (int)uVar5;
//       *(undefined2 *)(local_4 * 4 + 0x6e62) = (int)((ulong)uVar5 >> 0x10);
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     uVar5 = FUN_235c_0aff(*(undefined2 *)0x6e5c,*(undefined2 *)0x6e5e);
//     *(undefined2 *)0x6e70 = (int)uVar5;
//     *(undefined2 *)0x6e72 = (int)((ulong)uVar5 >> 0x10);
//     uVar1 = FUN_24dd_3dbd();
//     *(undefined1 *)0x6e74 = uVar1;
//     uVar3 = 0;
//     FUN_24dd_3dbd();
//     *(undefined2 *)0x6e76 = uVar3;
//     local_4 = 1;
//     while( true ) {
//       uVar5 = FUN_235c_0aff(*(undefined2 *)(local_4 * 4 + 0x6e60),
//                             *(undefined2 *)(local_4 * 4 + 0x6e62));
//       *(undefined2 *)(local_4 * 4 + 0x6e74) = (int)uVar5;
//       *(undefined2 *)(local_4 * 4 + 0x6e76) = (int)((ulong)uVar5 >> 0x10);
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     local_4 = 1;
//     while( true ) {
//       uVar1 = FUN_24dd_3dbd();
//       *(undefined1 *)(local_4 + 0x6e7f) = uVar1;
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     local_4 = 1;
//     while( true ) {
//       uVar3 = 0;
//       FUN_24dd_3dbd();
//       *(undefined2 *)(local_4 * 2 + 0x6e80) = uVar3;
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     FUN_24dd_4905(0xff80,0x400,(int)*(undefined4 *)0x6e5c,
//                   (int)((ulong)*(undefined4 *)0x6e5c >> 0x10));
//     FUN_235c_0b7c();
//   }
//   else {
//     uVar5 = FUN_24dd_028a(0x1000);
//     *(undefined2 *)0x6e58 = (int)uVar5;
//     *(undefined2 *)0x6e5a = (int)((ulong)uVar5 >> 0x10);
//     FUN_235c_0aff(*(undefined2 *)0x6e58,*(undefined2 *)0x6e5a);
//     FUN_24dd_3dbd();
//     uVar2 = 0;
//     iVar4 = 1;
//     FUN_24dd_3dbd();
//     if ((int)(iVar4 + (uint)(0xfbff < uVar2)) < 1) {
//       uVar3 = *(undefined2 *)0x6e5a;
//       *(undefined2 *)0x6e60 = *(undefined2 *)0x6e58;
//       *(undefined2 *)0x6e62 = uVar3;
//     }
//     else {
//       uVar5 = FUN_235c_0b33((int)*(undefined4 *)0x6e58 + 0x800,
//                             (int)((ulong)*(undefined4 *)0x6e58 >> 0x10));
//       *(undefined2 *)0x6e60 = (int)uVar5;
//       *(undefined2 *)0x6e62 = (int)((ulong)uVar5 >> 0x10);
//     }
//     local_4 = 1;
//     while( true ) {
//       uVar5 = FUN_235c_0b33((int)*(undefined4 *)0x6e60 + local_4 * 0x400 + -0x400,
//                             (int)((ulong)*(undefined4 *)0x6e60 >> 0x10));
//       *(undefined2 *)(local_4 * 4 + 0x6e60) = (int)uVar5;
//       *(undefined2 *)(local_4 * 4 + 0x6e62) = (int)((ulong)uVar5 >> 0x10);
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     uVar5 = FUN_235c_0aff(*(undefined2 *)0x6e60,*(undefined2 *)0x6e62);
//     *(undefined2 *)0x6e70 = (int)uVar5;
//     *(undefined2 *)0x6e72 = (int)((ulong)uVar5 >> 0x10);
//     uVar1 = FUN_24dd_3dbd();
//     *(undefined1 *)0x6e74 = uVar1;
//     FUN_24dd_3dbd();
//     uVar3 = 0;
//     FUN_24dd_3dbd();
//     *(undefined2 *)0x6e76 = uVar3;
//     local_4 = 1;
//     while( true ) {
//       uVar5 = FUN_235c_0aff(*(undefined2 *)(local_4 * 4 + 0x6e60),
//                             *(undefined2 *)(local_4 * 4 + 0x6e62));
//       *(undefined2 *)(local_4 * 4 + 0x6e74) = (int)uVar5;
//       *(undefined2 *)(local_4 * 4 + 0x6e76) = (int)((ulong)uVar5 >> 0x10);
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     local_4 = 1;
//     while( true ) {
//       uVar1 = FUN_24dd_3dbd();
//       *(undefined1 *)(local_4 + 0x6e7f) = uVar1;
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     local_4 = 1;
//     while( true ) {
//       FUN_24dd_3dbd();
//       uVar3 = 0;
//       FUN_24dd_3dbd();
//       *(undefined2 *)(local_4 * 2 + 0x6e80) = uVar3;
//       if (local_4 == 2) break;
//       local_4 = local_4 + 1;
//     }
//     FUN_24dd_4905(0,0x800,(int)*(undefined4 *)0x6e60,(int)((ulong)*(undefined4 *)0x6e60 >> 0x10));
//   }
//   FUN_24dd_4905(0,0x400,0x6a58,unaff_DS);
//   FUN_235c_0aad(1);
//   *(undefined2 *)0x67c2 = 0;
//   *(undefined2 *)0x67c4 = 0;
//   FUN_235c_03a1();
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_0bbc;
begin
  { TODO: translate from asm/FUN_235c_0bbc.s — UNMATCHED until an oracle passes }
end;

