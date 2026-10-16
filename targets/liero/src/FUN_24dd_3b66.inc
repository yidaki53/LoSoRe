{ liero::FUN_24dd_3b66 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3b66.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3b66.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3b66(undefined2 param_1,undefined2 *param_2)
// 
// {
//   code *pcVar1;
//   undefined2 uVar2;
//   undefined2 *puVar3;
//   undefined2 uVar4;
//   undefined2 unaff_DS;
//   bool bVar5;
//   undefined2 in_stack_00000000;
//   
//   uVar4 = (undefined2)((ulong)param_2 >> 0x10);
//   puVar3 = (undefined2 *)param_2;
//   if (puVar3[1] != -0x2850) {
//     if (puVar3[1] != -0x284d) {
//       *(undefined2 *)0x6410 = 0x66;
//       return;
//     }
//     FUN_24dd_3bde(puVar3,uVar4);
//   }
//   uVar2 = 1;
//   if (*(char *)(puVar3 + 0x18) != '\0') {
//     bVar5 = false;
//     pcVar1 = (code *)swi(0x21);
//     uVar2 = (*pcVar1)();
//     if (bVar5) {
//       *(undefined2 *)0x6410 = uVar2;
//       return;
//     }
//   }
//   puVar3[1] = 0xd7b3;
//   *param_2 = uVar2;
//   puVar3[2] = param_1;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3b66;
begin
  { TODO: translate from asm/FUN_24dd_3b66.s — UNMATCHED until an oracle passes }
end;

