{ stickman::FUN_42b5_081a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_081a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_081a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_081a(undefined4 param_1)
// 
// {
//   char cVar1;
//   int in_BX;
//   undefined1 in_ZF;
//   
//   FUN_42b5_0776();
//   if ((bool)in_ZF) {
//     do {
//       cVar1 = FUN_42b5_079a();
//       if (cVar1 == '\x1a') goto LAB_42b5_083b;
//       in_BX = in_BX + 1;
//     } while (cVar1 != '\r');
//     cVar1 = FUN_42b5_079a();
//     if (cVar1 == '\n') {
//       in_BX = in_BX + 1;
//     }
//   }
// LAB_42b5_083b:
//   *(int *)((int)param_1 + 8) = in_BX;
//   FUN_42b5_0879();
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_081a(param_1: Longint);
begin
  { TODO: translate from asm/FUN_42b5_081a.s — UNMATCHED until an oracle passes }
end;

