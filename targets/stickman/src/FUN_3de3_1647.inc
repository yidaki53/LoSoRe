{ stickman::FUN_3de3_1647 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_3de3_1647.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_3de3_1647.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_3de3_1647(void)
// 
// {
//   undefined1 extraout_AH;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined2 uVar3;
//   undefined2 uVar4;
//   undefined2 uVar5;
//   undefined2 uVar6;
//   undefined1 local_402 [256];
//   undefined1 local_302 [256];
//   undefined1 local_202 [256];
//   undefined1 local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x3de3;
//   uStack_6 = 0xf482;
//   FUN_42b5_04df();
//   FUN_410e_01c0();
//   uVar3 = 0xec16;
//   uVar5 = unaff_DS;
//   FUN_42b5_08b5(0,CONCAT11(extraout_AH,7));
//   FUN_42b5_0917(0,0x1476,0x42b5);
//   FUN_42b5_0848(uVar3,uVar5);
//   FUN_42b5_04a9();
//   uVar4 = 0xec16;
//   puVar2 = local_202;
//   uVar3 = unaff_SS;
//   uVar6 = unaff_DS;
//   FUN_42b5_0bc4(0x148a,0x42b5);
//   puVar1 = local_102;
//   uVar5 = unaff_SS;
//   FUN_4170_0e7d(0x138,unaff_DS);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x1496,0x42b5);
//   FUN_42b5_0917(0,puVar2,uVar3);
//   FUN_42b5_0848(uVar4,uVar6);
//   FUN_42b5_04a9();
//   uVar4 = 0xec16;
//   puVar2 = local_202;
//   uVar3 = unaff_SS;
//   uVar6 = unaff_DS;
//   FUN_42b5_0bc4(0x14c9,0x42b5);
//   puVar1 = local_102;
//   uVar5 = unaff_SS;
//   FUN_4170_0e7d(0x138,unaff_DS);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x14d5,0x42b5);
//   FUN_42b5_0917(0,puVar2,uVar3);
//   FUN_42b5_0848(uVar4,uVar6);
//   FUN_42b5_04a9();
//   uVar4 = 0xec16;
//   puVar2 = local_202;
//   uVar3 = unaff_SS;
//   uVar6 = unaff_DS;
//   FUN_42b5_0bc4(0x14c9,0x42b5);
//   puVar1 = local_102;
//   uVar5 = unaff_SS;
//   FUN_4170_0e7d(0x138,unaff_DS);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x14fe,0x42b5);
//   FUN_42b5_0917(0,puVar2,uVar3);
//   FUN_42b5_0848(uVar4,uVar6);
//   FUN_42b5_04a9();
//   uVar4 = 0xec16;
//   puVar2 = local_202;
//   uVar3 = unaff_SS;
//   uVar6 = unaff_DS;
//   FUN_42b5_0bc4(0x14c9,0x42b5);
//   puVar1 = local_102;
//   uVar5 = unaff_SS;
//   FUN_4170_0e7d(0x138,unaff_DS);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x152e,0x42b5);
//   FUN_42b5_0917(0,puVar2,uVar3);
//   FUN_42b5_0848(uVar4,uVar6);
//   FUN_42b5_04a9();
//   uVar3 = 0xec16;
//   uVar5 = unaff_DS;
//   FUN_42b5_0917(0,0x155a,0x42b5);
//   FUN_42b5_0848(uVar3,uVar5);
//   FUN_42b5_04a9();
//   uVar3 = 0xec16;
//   uVar5 = unaff_DS;
//   FUN_42b5_0917(0,0x159a,0x42b5);
//   FUN_42b5_0848(uVar3,uVar5);
//   FUN_42b5_04a9();
//   uVar3 = 0xec16;
//   uVar5 = unaff_DS;
//   FUN_42b5_0917(0,0x15e0,0x42b5);
//   FUN_42b5_0848(uVar3,uVar5);
//   FUN_42b5_04a9();
//   uVar5 = 0xec16;
//   FUN_42b5_0917(0,0x162c,0x42b5);
//   FUN_42b5_0848(uVar5,unaff_DS);
//   FUN_42b5_04a9();
//   puVar2 = local_202;
//   uVar3 = unaff_SS;
//   FUN_42b5_0bc4(0x162d,0x42b5);
//   puVar1 = local_102;
//   uVar5 = unaff_SS;
//   FUN_42b5_1a56(1);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x1645,0x42b5);
//   puVar1 = local_302;
//   uVar5 = unaff_SS;
//   FUN_42b5_1a56(2);
//   FUN_42b5_0c51(puVar1,uVar5);
//   FUN_42b5_0c51(0x1645,0x42b5);
//   puVar1 = local_402;
//   FUN_42b5_1a56(3);
//   FUN_42b5_0c51(puVar1,unaff_SS);
//   FUN_3de3_00e2(puVar2,uVar3);
//   FUN_42b5_00e9();
//   return;
// }
// 
// --- end reference ---
procedure FUN_3de3_1647;
begin
  { TODO: translate from asm/FUN_3de3_1647.s — UNMATCHED until an oracle passes }
end;

