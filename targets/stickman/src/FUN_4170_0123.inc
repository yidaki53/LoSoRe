{ stickman::FUN_4170_0123 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_0123.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_0123.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __stdcall16far FUN_4170_0123(undefined4 param_1)
// 
// {
//   undefined2 unaff_SS;
//   undefined1 *puVar1;
//   undefined2 uVar2;
//   undefined1 local_218 [256];
//   undefined2 local_118;
//   undefined2 local_114;
//   undefined1 *local_112;
//   uint local_106;
//   undefined1 local_104;
//   undefined1 local_103 [253];
//   undefined2 uStack_6;
//   undefined2 local_4;
//   
//   local_4 = 0x4170;
//   uStack_6 = 0x182e;
//   FUN_42b5_04df();
//   FUN_42b5_0bde(0xff,&local_104,unaff_SS,(int)param_1,(int)((ulong)param_1 >> 0x10));
//   puVar1 = local_218;
//   uVar2 = unaff_SS;
//   FUN_42b5_0bc4(&local_104,unaff_SS);
//   FUN_42b5_0c51(0x121,0x42b5);
//   FUN_42b5_0bde(0xff,&local_104,unaff_SS,puVar1,uVar2);
//   local_118 = CONCAT11(0x3c,(undefined1)local_118);
//   local_114 = 0;
//   local_112 = local_103;
//   FUN_428f_0000(0x42b5,&local_118);
//   if ((local_106 & 1) == 0) {
//     local_4 = local_118;
//   }
//   else {
//     local_4 = 0xffff;
//   }
//   return local_4;
// }
// 
// --- end reference ---
function FUN_4170_0123(param_1: Longint): Word;
begin
  { TODO: translate from asm/FUN_4170_0123.s — UNMATCHED until an oracle passes }
end;

