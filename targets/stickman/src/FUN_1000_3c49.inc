{ stickman::FUN_1000_3c49 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_3c49.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_3c49.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_3c49(void)
// 
// {
//   char cVar1;
//   undefined1 extraout_AH;
//   undefined2 uVar2;
//   undefined2 unaff_SS;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined1 local_4bc [187];
//   byte abStack_401 [65];
//   undefined2 auStack_3c0 [347];
//   undefined1 local_10a [256];
//   int local_a;
//   int local_8;
//   int local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0x3c54;
//   FUN_42b5_04df();
//   FUN_3de3_002d(0x3bd6,0x42b5);
//   local_6 = FUN_4170_01b8(CONCAT11(extraout_AH,0x40),0x3bf7,0x3de3);
//   if (local_6 == -1) {
//     uVar2 = 0x42b5;
//     FUN_42b5_1a42(0x200,0x2b2,auStack_3c0 + 2,unaff_SS);
//   }
//   else {
//     FUN_4170_024c(0x2b2,auStack_3c0 + 2,unaff_SS,local_6);
//     uVar2 = 0x4170;
//     FUN_4170_049d(local_6);
//   }
//   cVar1 = FUN_4170_0a65(0x3c0b,uVar2,0x3c02,uVar2);
//   if (cVar1 != '\0') {
//     cVar1 = FUN_4170_0a65(0x3c22,0x4170,0x3c19,0x4170);
//     if (cVar1 != '\0') {
//       local_8 = FUN_4170_01b8(0x12,0x3c0b,0x4170);
//       local_a = FUN_4170_01b8(0x12,0x3c22,0x4170);
//       if (local_8 != -1) {
//         FUN_4170_02fc(0,0,2,local_8);
//       }
//       if (local_a != -1) {
//         FUN_4170_02fc(0,0,2,local_a);
//       }
//       uVar2 = 0x4170;
//       FUN_1000_3b3e(&stack0xfffe,0x3c30,0x4170);
//       local_4 = 1;
//       while( true ) {
//         if ((bool)((byte)local_4 & 1)) {
//           FUN_1000_3b3e(&stack0xfffe,0x3c37,uVar2);
//         }
//         else {
//           FUN_1000_3b3e(&stack0xfffe,0x3c3d,uVar2);
//         }
//         FUN_42b5_1766(0xff,local_10a,unaff_SS,2,local_4,local_4 >> 0xf);
//         puVar3 = local_4bc;
//         uVar2 = unaff_SS;
//         FUN_42b5_0bc4(local_10a,unaff_SS);
//         FUN_42b5_0c51(0x3c43,0x42b5);
//         FUN_1000_3b3e(&stack0xfffe,puVar3,uVar2);
//         puVar3 = local_4bc;
//         uVar2 = unaff_SS;
//         FUN_42b5_0bc4(local_10a,unaff_SS);
//         FUN_42b5_0c51(0x3c43,0x42b5);
//         FUN_1000_3b8a(&stack0xfffe,puVar3,uVar2);
//         FUN_42b5_1766(0xff,local_10a,unaff_SS,0xb,*(undefined2 *)((int)auStack_3c0 + local_4 * 0x45)
//                       ,*(undefined2 *)((int)auStack_3c0 + local_4 * 0x45 + 2));
//         while (abStack_401[local_4 * 0x45] < 0x40) {
//           puVar3 = local_4bc;
//           uVar2 = unaff_SS;
//           FUN_42b5_0bc4(abStack_401 + local_4 * 0x45,unaff_SS);
//           FUN_42b5_0c51(0x3c43,0x42b5);
//           FUN_42b5_0bde(0x40,abStack_401 + local_4 * 0x45,unaff_SS,puVar3,uVar2);
//         }
//         puVar3 = local_4bc;
//         uVar2 = unaff_SS;
//         FUN_42b5_0bc4(local_10a,unaff_SS);
//         FUN_42b5_0c51(0x3c43,0x42b5);
//         FUN_42b5_0c51(abStack_401 + local_4 * 0x45,unaff_SS);
//         FUN_42b5_0c51(0x3c45,0x42b5);
//         FUN_42b5_0c51(0x3c47,0x42b5);
//         FUN_1000_3b3e(&stack0xfffe,puVar3,uVar2);
//         puVar3 = local_4bc;
//         uVar4 = unaff_SS;
//         FUN_42b5_0bc4(local_10a,unaff_SS);
//         FUN_42b5_0c51(0x3c43,0x42b5);
//         FUN_42b5_0c51(abStack_401 + local_4 * 0x45,unaff_SS);
//         FUN_42b5_0c51(0x3c45,0x42b5);
//         uVar2 = 0x42b5;
//         FUN_42b5_0c51(0x3c47,0x42b5);
//         FUN_1000_3b8a(&stack0xfffe,puVar3,uVar4);
//         if (local_4 == 10) break;
//         local_4 = local_4 + 1;
//       }
//       if (local_8 != -1) {
//         FUN_4170_049d(local_8);
//       }
//       if (local_a != -1) {
//         FUN_4170_049d(local_a);
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_3c49;
begin
  { TODO: translate from asm/FUN_1000_3c49.s — UNMATCHED until an oracle passes }
end;

