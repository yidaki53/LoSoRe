{ stickman::FUN_1000_0007 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0007.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0007.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_1000_0007(undefined4 param_1)
// 
// {
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar1;
//   undefined2 uVar2;
//   undefined1 local_202 [256];
//   byte local_102 [252];
//   undefined2 uStack_6;
//   undefined2 uStack_4;
//   
//   uStack_4 = 0x1000;
//   uStack_6 = 0x12;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,local_102,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   if (*(char *)0x50a != '\0') {
//     *(int *)0x3b6 = 0x4b - (uint)local_102[0];
//     FUN_42b5_0bde(0xff,0x3b8,unaff_DS,local_102,unaff_SS);
//     FUN_3de3_0b67(0x17,*(undefined2 *)0x3b6);
//     puVar1 = local_202;
//     uVar2 = unaff_SS;
//     FUN_42b5_0bc4(0,0x3de3);
//     FUN_42b5_0c51(local_102,unaff_SS);
//     FUN_3de3_002d(puVar1,uVar2);
//     *(undefined1 *)0x136 = 0;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_0007(param_1: Longint);
begin
  { TODO: translate from asm/FUN_1000_0007.s — UNMATCHED until an oracle passes }
end;

