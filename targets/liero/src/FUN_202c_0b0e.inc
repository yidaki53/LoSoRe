{ liero::FUN_202c_0b0e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0b0e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0b0e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 FUN_202c_0b0e(undefined2 param_1,byte *param_2)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   undefined4 uVar3;
//   undefined2 uVar4;
//   undefined1 uVar5;
//   undefined1 extraout_AH;
//   uint uVar6;
//   byte *pbVar7;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 local_188 [2];
//   int local_186;
//   undefined1 local_184 [128];
//   byte local_104;
//   byte abStack_103 [256];
//   char local_3;
//   
//   pbVar7 = (byte *)param_2;
//   local_104 = *param_2;
//   pbVar2 = abStack_103;
//   for (uVar6 = (uint)local_104; pbVar7 = pbVar7 + 1, uVar6 != 0; uVar6 = uVar6 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar7;
//   }
//   uVar4 = FUN_202c_0843(&local_104,unaff_SS);
//   local_3 = (char)uVar4;
//   uVar5 = (undefined1)((uint)uVar4 >> 8);
//   if (local_3 != '\0') {
//     FUN_24dd_3b22(&local_104,unaff_SS,local_184,unaff_SS);
//     FUN_24dd_3b5d(1,local_184,unaff_SS);
//     FUN_24dd_04f4();
//     local_186 = 0;
//     while( true ) {
//       uVar3 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_186 * 4);
//       FUN_24dd_3c48(local_188,unaff_SS,0x1f8,(int)uVar3,(int)((ulong)uVar3 >> 0x10),local_184,
//                     unaff_SS);
//       FUN_24dd_04f4();
//       if (local_186 == 0x15d) break;
//       local_186 = local_186 + 1;
//     }
//     FUN_24dd_3bde(local_184,unaff_SS);
//     FUN_24dd_04f4();
//     uVar5 = extraout_AH;
//   }
//   return CONCAT11(uVar5,local_3);
// }
// 
// --- end reference ---
procedure FUN_202c_0b0e;
begin
  { TODO: translate from asm/FUN_202c_0b0e.s — UNMATCHED until an oracle passes }
end;

