{ liero::FUN_1000_01a1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_01a1.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_01a1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_01a1(void)
// 
// {
//   char cVar1;
//   uint uVar2;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined2 uVar5;
//   undefined2 uVar6;
//   undefined1 local_104 [254];
//   undefined2 uStack_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   uStack_6 = 0x1ac;
//   FUN_24dd_0530();
//   if (*(char *)0x4b8 == '\0') {
//     uVar4 = 0x79f0;
//     FUN_24dd_39c3(0,0,0x24dd);
//     FUN_24dd_3930(uVar4,unaff_DS);
//     FUN_24dd_04f4();
//   }
//   else {
//     uVar5 = 0x79f0;
//     uVar4 = unaff_DS;
//     FUN_24dd_39c3(0,0xf,0x24dd);
//     FUN_24dd_3930(uVar5,uVar4);
//     FUN_24dd_04f4();
//     cVar1 = FUN_1e7d_018a(0x65d6,unaff_DS,0x65d5,unaff_DS,0x65d4,unaff_DS,0x65d2,unaff_DS);
//     if (cVar1 == '\0') {
//       uVar5 = 0x79f0;
//       uVar4 = unaff_DS;
//       FUN_24dd_39c3(0,0x2c,0x1e7d);
//       FUN_24dd_3930(uVar5,uVar4);
//       FUN_24dd_04f4();
//       uVar5 = 0x79f0;
//       uVar4 = unaff_DS;
//       FUN_24dd_39c3(0,0,0x24dd);
//       FUN_24dd_3930(uVar5,uVar4);
//       FUN_24dd_04f4();
//       *(undefined1 *)0x4b8 = 0;
//     }
//     else {
//       cVar1 = FUN_235c_0086(*(undefined1 *)0x65d6,*(undefined1 *)0x65d5,*(undefined1 *)0x65d4,
//                             *(undefined2 *)0x65d2);
//       if (cVar1 == '\0') {
//         uVar5 = 0x79f0;
//         uVar4 = unaff_DS;
//         FUN_24dd_39c3(0,0x4f,0x235c);
//         FUN_24dd_3930(uVar5,uVar4);
//         FUN_24dd_04f4();
//         uVar5 = 0x79f0;
//         uVar4 = unaff_DS;
//         FUN_24dd_39c3(0,0,0x24dd);
//         FUN_24dd_3930(uVar5,uVar4);
//         FUN_24dd_04f4();
//         *(undefined1 *)0x4b8 = 0;
//       }
//       else {
//         if (*(char *)0x67cd == '\0') {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0x6d,0x235c);
//           puVar3 = local_104;
//           FUN_1ec2_0018(*(undefined2 *)0x65d2);
//           FUN_24dd_39c3(0,puVar3,unaff_SS);
//           FUN_24dd_39c3(0,0x93,0x24dd);
//           FUN_24dd_3a4b(0,*(undefined1 *)0x65d4,0);
//           FUN_24dd_39c3(0,0xa0,0x24dd);
//           FUN_24dd_3a4b(0,*(undefined1 *)0x65d5,0);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         else {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0x6d,0x235c);
//           puVar3 = local_104;
//           FUN_1ec2_0018(*(undefined2 *)0x65d2);
//           FUN_24dd_39c3(0,puVar3,unaff_SS);
//           FUN_24dd_39c3(0,0x75,0x24dd);
//           FUN_24dd_3a4b(0,*(undefined1 *)0x65d4,0);
//           FUN_24dd_39c3(0,0x7e,0x24dd);
//           FUN_24dd_3a4b(0,*(undefined1 *)0x65d5,0);
//           FUN_24dd_39c3(0,0x88,0x24dd);
//           FUN_24dd_3a4b(0,*(undefined1 *)0x65d6,0);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         uVar5 = 0x79f0;
//         uVar4 = unaff_DS;
//         FUN_24dd_39c3(0,0xae,0x24dd);
//         FUN_24dd_31d8(uVar5);
//         FUN_24dd_3adf(2,0);
//         FUN_24dd_39c3(0,0xbb,0x24dd);
//         FUN_24dd_3951(uVar5,uVar4);
//         FUN_24dd_04f4();
//         if (*(char *)0x67cd == '\0') {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,200,0x24dd);
//           FUN_24dd_3951(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         else {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0xbf,0x24dd);
//           FUN_24dd_3951(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         if (*(char *)0x67cc == '\0') {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0xe1,0x24dd);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         else {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0xd0,0x24dd);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//         }
//         cVar1 = FUN_235c_0340();
//         if (cVar1 == '\0') {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0xee,0x235c);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0x111,0x24dd);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//           FUN_24dd_0116();
//         }
//         else {
//           uVar5 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0x12d,0x235c);
//           FUN_24dd_3930(uVar5,uVar4);
//           FUN_24dd_04f4();
//           uVar6 = 0x79f0;
//           uVar4 = unaff_DS;
//           FUN_24dd_39c3(0,0x155,0x24dd);
//           uVar5 = FUN_235c_0361(uVar6);
//           FUN_24dd_3a4b(0,uVar5,0);
//           FUN_24dd_39c3(0,0x168,0x24dd);
//           FUN_24dd_3951(uVar6,uVar4);
//           FUN_24dd_04f4();
//           uVar2 = FUN_235c_0361();
//           if (uVar2 < 0x2cb) {
//             uVar5 = 0x79f0;
//             uVar4 = unaff_DS;
//             FUN_24dd_39c3(0,0x16c,0x235c);
//             FUN_24dd_3930(uVar5,uVar4);
//             FUN_24dd_04f4();
//             FUN_24dd_0116();
//           }
//           else {
//             uVar5 = 0x79f0;
//             uVar4 = unaff_DS;
//             FUN_24dd_39c3(0,0x182,0x235c);
//             FUN_24dd_3951(uVar5,uVar4);
//             FUN_24dd_04f4();
//             FUN_235c_0482();
//             FUN_235c_04bc(0x194,0x235c);
//             local_4 = 1;
//             while( true ) {
//               FUN_235c_0711(local_4 * 9 + 0x8b,unaff_DS,local_4 * 4 + 0x6734,unaff_DS);
//               if (local_4 == 0x1e) break;
//               local_4 = local_4 + 1;
//             }
//             FUN_235c_04f3();
//           }
//         }
//         FUN_235c_0bbc();
//         uVar4 = 0x79f0;
//         FUN_24dd_39c3(0,0x19e,0x235c);
//         FUN_24dd_3930(uVar4,unaff_DS);
//         FUN_24dd_04f4();
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_01a1;
begin
  { TODO: translate from asm/FUN_1000_01a1.s — UNMATCHED until an oracle passes }
end;

