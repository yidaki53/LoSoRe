{ stickman::FUN_3de3_1029 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_3de3_1029.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_3de3_1029.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_3de3_1029(void)
// 
// {
//   undefined1 extraout_AH;
//   undefined1 extraout_AH_00;
//   undefined1 extraout_AH_01;
//   undefined1 extraout_AH_02;
//   undefined1 extraout_AH_03;
//   undefined1 uVar1;
//   undefined1 extraout_AH_04;
//   undefined1 extraout_AH_05;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar2;
//   undefined2 uVar3;
//   undefined2 uVar4;
//   undefined1 local_206 [256];
//   byte local_106 [256];
//   uint local_6;
//   uint local_4;
//   
//   local_4 = 0x3de3;
//   local_6 = 0xee64;
//   FUN_42b5_04df();
//   FUN_3de3_002d(0xf70,0x42b5);
//   local_4 = FUN_410e_023f();
//   local_4 = local_4 & 0xff;
//   local_6 = FUN_410e_024b();
//   local_6 = local_6 & 0xff;
//   FUN_410e_0213(0x18,1);
//   puVar2 = local_206;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(0xf7b,0x410e);
//   FUN_42b5_0c51(0x138,unaff_DS);
//   FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar2,uVar4);
//   if (*(char *)0x137 == '\0') {
//     puVar2 = local_206;
//     uVar4 = unaff_SS;
//     FUN_42b5_0bc4(local_106,unaff_SS);
//     FUN_42b5_0c51(0xf86,0x42b5);
//     FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar2,uVar4);
//   }
//   else {
//     puVar2 = local_206;
//     uVar4 = unaff_SS;
//     FUN_42b5_0bc4(local_106,unaff_SS);
//     FUN_42b5_0c51(0xf7f,0x42b5);
//     FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar2,uVar4);
//   }
//   puVar2 = local_206;
//   uVar4 = unaff_SS;
//   FUN_42b5_0bc4(local_106,unaff_SS);
//   FUN_42b5_0c51(0xf8d,0x42b5);
//   FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar2,uVar4);
//   while (local_106[0] < 0x4f) {
//     puVar2 = local_206;
//     uVar4 = unaff_SS;
//     FUN_42b5_0bc4(0xfcc,0x42b5);
//     FUN_42b5_0c51(local_106,unaff_SS);
//     FUN_42b5_0bde(0xff,local_106,unaff_SS,puVar2,uVar4);
//   }
//   uVar3 = 0xec16;
//   uVar4 = unaff_DS;
//   FUN_42b5_0917(0,local_106,unaff_SS);
//   FUN_42b5_086c(uVar3,uVar4);
//   FUN_42b5_04a9();
//   FUN_410e_0213(CONCAT11(extraout_AH,0x18),CONCAT11(extraout_AH,0x29));
//   uVar3 = 0xec16;
//   uVar4 = unaff_DS;
//   FUN_42b5_0917(0,0xa7d6,unaff_DS);
//   FUN_42b5_086c(uVar3,uVar4);
//   FUN_42b5_04a9();
//   FUN_410e_0213(CONCAT11(extraout_AH_00,0x19),CONCAT11(extraout_AH_00,1));
//   uVar3 = 0xec16;
//   uVar4 = unaff_DS;
//   FUN_42b5_0917(0,0xfce,0x410e);
//   FUN_42b5_086c(uVar3,uVar4);
//   FUN_42b5_04a9();
//   FUN_410e_0213(CONCAT11(extraout_AH_01,0x19),CONCAT11(extraout_AH_01,0xe));
//   if (*(int *)0xaaec == 0) {
//     uVar3 = 0xec16;
//     uVar4 = unaff_DS;
//     FUN_42b5_0917(0,0x101e,0x410e);
//     FUN_42b5_086c(uVar3,uVar4);
//     FUN_42b5_04a9();
//     uVar1 = extraout_AH_02;
//   }
//   else {
//     uVar3 = 0xec16;
//     uVar4 = unaff_DS;
//     FUN_42b5_09ad(0,*(undefined1 *)0xa8e7,0);
//     FUN_42b5_086c(uVar3,uVar4);
//     FUN_42b5_04a9();
//     uVar1 = extraout_AH_03;
//   }
//   FUN_410e_0213(CONCAT11(uVar1,0x19),CONCAT11(uVar1,0x20));
//   uVar4 = 0xec16;
//   puVar2 = local_206;
//   FUN_4170_11bc(puVar2);
//   FUN_42b5_0917(0,puVar2,unaff_SS);
//   FUN_42b5_086c(uVar4,unaff_DS);
//   FUN_42b5_04a9();
//   FUN_410e_0213(CONCAT11(extraout_AH_04,(undefined1)local_6),
//                 CONCAT11(extraout_AH_04,(undefined1)local_4));
//   FUN_410e_0180(CONCAT11(extraout_AH_05,0x17),CONCAT11(extraout_AH_05,0x50),
//                 CONCAT11(extraout_AH_05,1),CONCAT11(extraout_AH_05,1));
//   FUN_3de3_002d(0x1024,0x410e);
//   return;
// }
// 
// --- end reference ---
procedure FUN_3de3_1029;
begin
  { TODO: translate from asm/FUN_3de3_1029.s — UNMATCHED until an oracle passes }
end;

