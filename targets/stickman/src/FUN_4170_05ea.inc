{ stickman::FUN_4170_05ea — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_05ea.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_05ea.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_4170_05ea(undefined4 param_1,undefined4 param_2)
// 
// {
//   undefined1 extraout_AH;
//   int iVar1;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar2;
//   undefined2 uVar3;
//   undefined1 *puVar4;
//   undefined2 uVar5;
//   undefined2 uVar6;
//   undefined1 local_504 [256];
//   undefined1 local_404 [256];
//   undefined1 local_304 [256];
//   char local_204;
//   char local_203;
//   int local_104;
//   byte local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x4170;
//   uStack_6 = 0x1cf5;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   FUN_4170_00c3(local_102,unaff_SS);
//   FUN_42b5_1a1f(0x80,local_304,unaff_SS,0x80,*(undefined2 *)0x398);
//   FUN_42b5_0bde(0xff,&local_204,unaff_SS,local_304,unaff_SS);
//   FUN_4170_00c3(&local_204,unaff_SS);
//   puVar4 = local_404;
//   uVar5 = unaff_SS;
//   FUN_42b5_0bc4(0x5e1,0x42b5);
//   FUN_42b5_0c51(local_102,unaff_SS);
//   FUN_42b5_0c51(0x5e3,0x42b5);
//   local_104 = FUN_42b5_0c7d(&local_204,unaff_SS,puVar4,uVar5);
//   uVar5 = (undefined2)((ulong)param_2 >> 0x10);
//   if (local_104 == 0) {
//     puVar4 = local_504;
//     puVar2 = local_404;
//     uVar3 = unaff_SS;
//     uVar6 = unaff_SS;
//     FUN_42b5_0bc4(0x5e5,0x42b5);
//     FUN_42b5_0c51(local_102,unaff_SS);
//     FUN_428f_01f2(puVar2,uVar3);
//     FUN_42b5_0bde(0xff,&local_204,unaff_SS,puVar4,uVar6);
//     FUN_42b5_0bde(0xff,(int)param_2,uVar5,&local_204,unaff_SS);
//   }
//   else {
//     FUN_42b5_0bde(0xff,&local_204,unaff_SS,local_304,unaff_SS);
//     FUN_42b5_0d75(local_104 + 1 + (uint)local_102[0],1,&local_204,unaff_SS);
//     if ((local_204 == '\0') || (local_203 != '\"')) {
//       iVar1 = FUN_42b5_0c7d(&local_204,unaff_SS,0x5e8,0x42b5);
//       if (iVar1 != 0) {
//         puVar4 = local_404;
//         uVar3 = unaff_SS;
//         FUN_4170_0df2(&local_204,unaff_SS,0x20);
//         FUN_42b5_0bde(0xff,&local_204,unaff_SS,puVar4,uVar3);
//       }
//     }
//     else {
//       FUN_42b5_0d75(1,1,&local_204,unaff_SS);
//       puVar4 = local_404;
//       uVar3 = unaff_SS;
//       FUN_4170_0df2(&local_204,unaff_SS,CONCAT11(extraout_AH,0x22));
//       FUN_42b5_0bde(0xff,&local_204,unaff_SS,puVar4,uVar3);
//     }
//     FUN_42b5_0bde(0xff,(int)param_2,uVar5,&local_204,unaff_SS);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_4170_05ea(param_1, param_2: Longint);
begin
  { TODO: translate from asm/FUN_4170_05ea.s — UNMATCHED until an oracle passes }
end;

