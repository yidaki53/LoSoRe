{ stickman::FUN_1000_568a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_568a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_568a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_568a(void)
// 
// {
//   undefined1 extraout_AH;
//   uint uVar1;
//   int iVar2;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined1 local_2b0 [256];
//   int local_1b0;
//   uint local_1ae;
//   uint local_1ac;
//   int local_1a4;
//   uint local_1a2;
//   uint local_1a0 [4];
//   undefined1 local_198 [256];
//   uint local_98;
//   int local_96;
//   uint local_94;
//   uint local_92;
//   undefined1 local_90 [129];
//   undefined1 local_f [9];
//   undefined2 local_6;
//   int local_4;
//   
//   local_4 = 0x1000;
//   local_6 = 0x5695;
//   FUN_42b5_04df();
//   local_4 = FUN_4170_01b8(CONCAT11(extraout_AH,0x40),0x5634,0x42b5);
//   if (local_4 == -1) {
//     FUN_3de3_0278(0x5641,0x4170);
//   }
//   FUN_4170_024c(0x8a,local_90,unaff_SS,local_4);
//   FUN_4170_049d(local_4);
//   FUN_42b5_1a1f(4,&local_94,unaff_SS,local_f,unaff_SS);
//   local_94 = local_94 ^ 0x4abe;
//   local_92 = local_92 ^ 0x2bad;
//   FUN_428f_0112(&local_1b0,unaff_SS,local_94,local_92);
//   FUN_428f_006c(&local_6,unaff_SS,local_1a0,unaff_SS,&local_1a2,unaff_SS,&local_1a4,unaff_SS);
//   local_1ae = local_1ae + 1;
//   if (0xc < local_1ae) {
//     local_1ae = 1;
//     local_1b0 = local_1b0 + 1;
//   }
//   FUN_42b5_1766(0xff,0xa6c6,unaff_DS,0,local_1ae,0);
//   FUN_42b5_1766(0xff,local_198,unaff_SS,0,local_1ac,0);
//   puVar3 = local_2b0;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(0xa6c6,unaff_DS);
//   FUN_42b5_0c51(0x5669,0x42b5);
//   FUN_42b5_0c51(local_198,unaff_SS);
//   FUN_42b5_0c51(0x5669,0x42b5);
//   FUN_42b5_0bde(0xff,0xa6c6,unaff_DS,puVar3,uVar4);
//   FUN_42b5_1766(0xff,local_198,unaff_SS,0,local_1b0,0);
//   puVar3 = local_2b0;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(0xa6c6,unaff_DS);
//   FUN_42b5_0c51(local_198,unaff_SS);
//   FUN_42b5_0bde(0xff,0xa6c6,unaff_DS,puVar3,uVar4);
//   local_94 = local_1b0 - 0x7bc;
//   local_92 = 0;
//   iVar2 = 0;
//   uVar1 = FUN_42b5_0b14();
//   local_94 = local_1ae + uVar1;
//   iVar2 = iVar2 + (uint)CARRY2(local_1ae,uVar1);
//   local_92 = iVar2;
//   uVar1 = FUN_42b5_0b14();
//   local_94 = local_1ac + uVar1;
//   local_92 = iVar2 + (uint)CARRY2(local_1ac,uVar1);
//   local_98 = local_1a4 + -0x7bc;
//   local_96 = 0;
//   iVar2 = 0;
//   uVar1 = FUN_42b5_0b14();
//   local_98 = local_1a2 + uVar1;
//   iVar2 = iVar2 + (uint)CARRY2(local_1a2,uVar1);
//   local_96 = iVar2;
//   uVar1 = FUN_42b5_0b14();
//   local_98 = local_1a0[0] + uVar1;
//   local_96 = iVar2 + (uint)CARRY2(local_1a0[0],uVar1);
//   if (((int)local_92 < local_96) || (((int)local_92 <= local_96 && (local_94 < local_98)))) {
//     puVar3 = local_2b0;
//     FUN_42b5_0bc4(0x566b,0x42b5);
//     FUN_42b5_0c51(0xa6c6,unaff_DS);
//     FUN_3de3_0278(puVar3,unaff_SS);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_568a;
begin
  { TODO: translate from asm/FUN_1000_568a.s — UNMATCHED until an oracle passes }
end;

