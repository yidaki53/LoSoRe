{ stickman::FUN_1000_40d4 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_40d4.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_40d4.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_40d4(int param_1,int param_2)
// 
// {
//   uint uVar1;
//   int iVar2;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined2 uVar5;
//   undefined1 local_204 [256];
//   byte local_104 [254];
//   undefined2 uStack_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   uStack_6 = 0x40df;
//   FUN_42b5_04df();
//   FUN_3de3_002d(0x40b1,0x42b5);
//   local_4 = 6;
//   while( true ) {
//     if ((local_4 + param_2 + -6 <= *(int *)0x26c4) && (local_4 + param_2 + -6 != param_1)) {
//       uVar1 = *(uint *)((local_4 + param_2 + -6) * 0x80 + 0x2694);
//       iVar2 = (int)uVar1 >> 0xf;
//       if ((*(int *)0x4fb < iVar2) || ((*(int *)0x4fb <= iVar2 && (*(uint *)0x4f9 < uVar1)))) {
//         FUN_3de3_002d(0x40b8,0x3de3);
//       }
//       else {
//         FUN_3de3_002d(0x40b1,0x3de3);
//       }
//       iVar2 = local_4 + param_2 + -6;
//       FUN_42b5_1766(0xff,local_104,unaff_SS,0,iVar2,iVar2 >> 0xf);
//       while (local_104[0] < 3) {
//         puVar3 = local_204;
//         uVar4 = unaff_SS;
//         FUN_42b5_0bc4(0x40bd,0x42b5);
//         FUN_42b5_0c51(local_104,unaff_SS);
//         FUN_42b5_0bde(0xff,local_104,unaff_SS,puVar3,uVar4);
//       }
//       uVar5 = 10;
//       puVar3 = local_204;
//       uVar4 = unaff_SS;
//       iVar2 = local_4;
//       FUN_42b5_0bc4(local_104,unaff_SS);
//       FUN_42b5_0c51(0x40bf,0x42b5);
//       FUN_42b5_0c51((local_4 + param_2 + -6) * 0x80 + 0x2646,unaff_DS);
//       FUN_3de3_0bea(puVar3,uVar4,iVar2,uVar5);
//     }
//     if (local_4 == 0x15) break;
//     local_4 = local_4 + 1;
//   }
//   FUN_42b5_1766(0xff,local_104,unaff_SS,0,param_1,param_1 >> 0xf);
//   while (local_104[0] < 3) {
//     puVar3 = local_204;
//     uVar4 = unaff_SS;
//     FUN_42b5_0bc4(0x40bd,0x42b5);
//     FUN_42b5_0c51(local_104,unaff_SS);
//     FUN_42b5_0bde(0xff,local_104,unaff_SS,puVar3,uVar4);
//   }
//   uVar5 = 6;
//   iVar2 = (param_1 - param_2) + 6;
//   puVar3 = local_204;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(0x40c1,0x42b5);
//   FUN_42b5_0c51(local_104,unaff_SS);
//   FUN_42b5_0c51(0x40bf,0x42b5);
//   FUN_3de3_0bea(puVar3,uVar4,iVar2,uVar5);
//   FUN_42b5_0bde(0xff,local_104,unaff_SS,param_1 * 0x80 + 0x2646,unaff_DS);
//   while (local_104[0] < 0x21) {
//     puVar3 = local_204;
//     uVar4 = unaff_SS;
//     FUN_42b5_0bc4(local_104,unaff_SS);
//     FUN_42b5_0c51(0x40bf,0x42b5);
//     FUN_42b5_0bde(0xff,local_104,unaff_SS,puVar3,uVar4);
//   }
//   puVar3 = local_204;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(local_104,unaff_SS);
//   FUN_42b5_0c51(0x40d0,0x42b5);
//   FUN_42b5_0bde(0xff,local_104,unaff_SS,puVar3,uVar4);
//   FUN_3de3_002d(local_104,unaff_SS);
//   FUN_1000_3ed4(param_1);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_40d4(param_1, param_2: Integer);
begin
  { TODO: translate from asm/FUN_1000_40d4.s — UNMATCHED until an oracle passes }
end;

