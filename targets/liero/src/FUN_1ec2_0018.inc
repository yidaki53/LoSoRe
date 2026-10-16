{ liero::FUN_1ec2_0018 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_0018.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_0018.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_0018(uint param_1,undefined4 param_2)
// 
// {
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar1;
//   undefined2 uVar2;
//   undefined1 *puVar3;
//   undefined2 uVar4;
//   undefined1 local_402 [256];
//   undefined1 local_302 [256];
//   undefined1 local_202 [256];
//   undefined1 local_102 [256];
//   
//   puVar3 = local_102;
//   uVar4 = unaff_SS;
//   FUN_24dd_3fb1(*(undefined1 *)((param_1 >> 0xc) + 0x4a6));
//   puVar1 = local_202;
//   uVar2 = unaff_SS;
//   FUN_24dd_3fb1(*(undefined1 *)(((param_1 & 0xf00) >> 8) + 0x4a6));
//   FUN_24dd_3f14(puVar1,uVar2);
//   puVar1 = local_302;
//   uVar2 = unaff_SS;
//   FUN_24dd_3fb1(*(undefined1 *)(((param_1 & 0xf0) >> 4) + 0x4a6));
//   FUN_24dd_3f14(puVar1,uVar2);
//   puVar1 = local_402;
//   FUN_24dd_3fb1(*(undefined1 *)((param_1 & 0xf) + 0x4a6));
//   FUN_24dd_3f14(puVar1,unaff_SS);
//   FUN_24dd_3eaf(0xff,(int)param_2,(int)((ulong)param_2 >> 0x10),puVar3,uVar4);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_0018;
begin
  { TODO: translate from asm/FUN_1ec2_0018.s — UNMATCHED until an oracle passes }
end;

