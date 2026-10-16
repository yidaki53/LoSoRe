{ liero::FUN_24dd_3bde — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3bde.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3bde.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3bde(uint *param_1)
// 
// {
//   code *pcVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   bool bVar3;
//   undefined1 in_ZF;
//   
//   FUN_24dd_3c03();
//   if ((bool)in_ZF) {
//     bVar3 = *param_1 < 4;
//     if (4 < *param_1) {
//       pcVar1 = (code *)swi(0x21);
//       uVar2 = (*pcVar1)();
//       if (bVar3) {
//         *(undefined2 *)0x6410 = uVar2;
//       }
//     }
//     ((uint *)param_1)[1] = 0xd7b0;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3bde;
begin
  { TODO: translate from asm/FUN_24dd_3bde.s — UNMATCHED until an oracle passes }
end;

