{ stickman::FUN_405f_0121 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_405f_0121.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_405f_0121.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_405f_0121(undefined1 param_1)
// 
// {
//   char cVar1;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   if (*(int *)0x156 == *(int *)0x158) {
//     cVar1 = FUN_405f_0067(CONCAT11((char)((uint)*(int *)0x156 >> 8),param_1));
//     if (cVar1 == '\0') {
//       FUN_405f_00ad(&stack0xfffe);
//     }
//   }
//   else {
//     FUN_405f_00ad(&stack0xfffe);
//     while ((*(int *)0x156 != *(int *)0x158 &&
//            (cVar1 = FUN_405f_0067(CONCAT11((char)((uint)*(int *)0x156 >> 8),
//                                            *(undefined1 *)(*(int *)0x158 + -0x54fe))), cVar1 != '\0'
//            ))) {
//       *(int *)0x158 = *(int *)0x158 + 1;
//       if (0x3fff < *(int *)0x158) {
//         *(int *)0x158 = *(int *)0x158 + -0x4000;
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_405f_0121(param_1: Byte);
begin
  { TODO: translate from asm/FUN_405f_0121.s — UNMATCHED until an oracle passes }
end;

