{ liero::FUN_202c_0706 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0706.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0706.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 __stdcall16far FUN_202c_0706(byte *param_1)
// 
// {
//   byte *pbVar1;
//   byte *pbVar2;
//   uint uVar3;
//   byte *pbVar4;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   int local_10c;
//   undefined4 local_10a;
//   byte local_106;
//   byte abStack_105 [259];
//   
//   pbVar4 = (byte *)param_1;
//   local_106 = *param_1;
//   pbVar2 = abStack_105;
//   for (uVar3 = (uint)local_106; pbVar4 = pbVar4 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
//     pbVar1 = pbVar2;
//     pbVar2 = pbVar2 + 1;
//     *pbVar1 = *pbVar4;
//   }
//   local_10a = FUN_24dd_4824(&local_10c,unaff_SS,&local_106,unaff_SS);
//   FUN_24dd_46e9();
//   if (local_10c != 0) {
//     local_10a = CONCAT22(*(undefined2 *)0x6414,*(undefined2 *)0x6412);
//   }
//   return local_10a;
// }
// 
// --- end reference ---
procedure FUN_202c_0706;
begin
  { TODO: translate from asm/FUN_202c_0706.s — UNMATCHED until an oracle passes }
end;

