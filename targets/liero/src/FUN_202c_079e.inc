{ liero::FUN_202c_079e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_079e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_079e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __stdcall16far
// FUN_202c_079e(undefined2 param_1,undefined2 param_2,undefined4 param_3,byte *param_4)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   char cVar3;
//   uint uVar4;
//   byte *pbVar5;
//   undefined2 unaff_SS;
//   undefined2 local_186;
//   undefined1 local_184 [128];
//   byte local_104;
//   byte abStack_103 [257];
//   
//   pbVar5 = (byte *)param_4;
//   local_104 = *param_4;
//   pbVar2 = abStack_103;
//   for (uVar4 = (uint)local_104; pbVar5 = pbVar5 + 1, uVar4 != 0; uVar4 = uVar4 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar5;
//   }
//   local_186 = 0;
//   cVar3 = FUN_202c_0843(&local_104,unaff_SS);
//   if (cVar3 != '\0') {
//     FUN_24dd_3b22(&local_104,unaff_SS,local_184,unaff_SS);
//     FUN_24dd_3b5d(1,local_184,unaff_SS);
//     FUN_24dd_04f4();
//     FUN_24dd_3cb0(param_2,0,local_184,unaff_SS);
//     FUN_24dd_04f4();
//     FUN_24dd_3c48(&local_186,unaff_SS,param_1,(int)param_3,(int)((ulong)param_3 >> 0x10),local_184,
//                   unaff_SS);
//     FUN_24dd_04f4();
//     FUN_24dd_3bde(local_184,unaff_SS);
//     FUN_24dd_04f4();
//   }
//   return local_186;
// }
// 
// --- end reference ---
procedure FUN_202c_079e;
begin
  { TODO: translate from asm/FUN_202c_079e.s — UNMATCHED until an oracle passes }
end;

