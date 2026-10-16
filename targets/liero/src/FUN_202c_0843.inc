{ liero::FUN_202c_0843 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0843.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0843.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __stdcall16far FUN_202c_0843(byte *param_1)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   undefined1 uVar3;
//   int iVar4;
//   uint uVar5;
//   byte *pbVar6;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 local_184 [128];
//   byte local_104;
//   byte abStack_103 [257];
//   
//   pbVar6 = (byte *)param_1;
//   local_104 = *param_1;
//   pbVar2 = abStack_103;
//   for (uVar5 = (uint)local_104; pbVar6 = pbVar6 + 1, uVar5 != 0; uVar5 = uVar5 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar6;
//   }
//   FUN_24dd_3b22(&local_104,unaff_SS,local_184,unaff_SS);
//   *(undefined1 *)0x6422 = 0;
//   FUN_24dd_3b5d(0x80,local_184,unaff_SS);
//   FUN_24dd_3bde(local_184,unaff_SS);
//   iVar4 = FUN_24dd_04ed();
//   if ((iVar4 == 0) && (local_104 != 0)) {
//     uVar3 = 1;
//   }
//   else {
//     uVar3 = 0;
//   }
//   return uVar3;
// }
// 
// --- end reference ---
procedure FUN_202c_0843;
begin
  { TODO: translate from asm/FUN_202c_0843.s — UNMATCHED until an oracle passes }
end;

