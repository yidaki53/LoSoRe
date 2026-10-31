{ stickman::FUN_42b5_1963 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_1963.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_1963.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_42b5_1963(uint param_1,int param_2,undefined4 param_3)
// 
// {
//   code *pcVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   bool bVar3;
//   undefined1 in_ZF;
//   
//   uVar2 = (undefined2)((ulong)param_3 >> 0x10);
//   FUN_42b5_18b6();
//   if ((bool)in_ZF) {
//     bVar3 = CARRY2(param_2 * *(int *)((int)param_3 + 4),
//                    (uint)((ulong)param_1 * (ulong)*(uint *)((int)param_3 + 4) >> 0x10));
//     pcVar1 = (code *)swi(0x21);
//     uVar2 = (*pcVar1)();
//     if (bVar3) {
//       *(undefined2 *)0x39c = uVar2;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_1963(param_1: Word; param_2: Integer; param_3: Longint);
begin
  { TODO: translate from asm/FUN_42b5_1963.s — UNMATCHED until an oracle passes }
end;

