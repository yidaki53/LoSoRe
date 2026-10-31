{ stickman::FUN_42b5_19da — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_19da.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_19da.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16near FUN_42b5_19da(undefined2 param_1,undefined2 param_2,undefined4 param_3)
// 
// {
//   code *pcVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   
//   if (*(int *)((int)param_3 + 2) == -0x284d) {
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     pcVar1 = (code *)swi(0x21);
//     uVar2 = (*pcVar1)();
//     return uVar2;
//   }
//   *(undefined2 *)0x39c = 0x67;
//   return 0;
// }
// 
// --- end reference ---
function FUN_42b5_19da(param_1, param_2: Word; param_3: Longint): Word;
begin
  { TODO: translate from asm/FUN_42b5_19da.s — UNMATCHED until an oracle passes }
end;

