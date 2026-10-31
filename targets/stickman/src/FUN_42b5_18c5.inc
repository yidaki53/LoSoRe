{ stickman::FUN_42b5_18c5 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_18c5.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_18c5.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_18c5(undefined2 param_1,undefined2 param_2,undefined4 param_3)
// 
// {
//   code *pcVar1;
//   int iVar2;
//   int iVar3;
//   int iVar4;
//   int unaff_BP;
//   undefined1 in_CF;
//   undefined1 in_ZF;
//   undefined2 in_stack_00000000;
//   
//   FUN_42b5_18b6();
//   if ((bool)in_ZF) {
//     iVar4 = *(int *)((int)param_3 + 4);
//     pcVar1 = (code *)swi(0x21);
//     iVar2 = (*pcVar1)();
//     iVar3 = iVar2;
//     if (((bool)in_CF) || (iVar3 = unaff_BP, iVar2 != iVar4)) {
//       *(int *)0x39c = iVar3;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_18c5(param_1, param_2: Word; param_3: Longint);
begin
  { TODO: translate from asm/FUN_42b5_18c5.s — UNMATCHED until an oracle passes }
end;

