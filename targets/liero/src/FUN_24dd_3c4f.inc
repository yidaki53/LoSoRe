{ liero::FUN_24dd_3c4f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3c4f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3c4f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_24dd_3c4f(uint *param_1,uint param_2,undefined2 param_3,undefined2 param_4,undefined4 param_5)
// 
// {
//   code *pcVar1;
//   uint uVar2;
//   undefined2 uVar3;
//   undefined2 unaff_BP;
//   undefined2 uVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   bool bVar6;
//   undefined1 in_ZF;
//   undefined2 in_stack_00000000;
//   
//   uVar3 = 0x65;
//   uVar4 = (undefined2)((ulong)param_5 >> 0x10);
//   FUN_24dd_3c03();
//   iVar5 = (int)((ulong)param_1 >> 0x10);
//   if ((bool)in_ZF) {
//     uVar2 = 0;
//     if (param_2 != 0) {
//       bVar6 = (int)((ulong)param_2 * (ulong)*(uint *)((int)param_5 + 4) >> 0x10) != 0;
//       pcVar1 = (code *)swi(0x21);
//       uVar2 = (*pcVar1)();
//       if (bVar6) {
//         *(uint *)0x6410 = uVar2;
//         goto LAB_24dd_3c9e;
//       }
//       uVar2 = uVar2 / *(uint *)((int)param_5 + 4);
//       uVar3 = unaff_BP;
//       unaff_DS = in_stack_00000000;
//     }
//     if (iVar5 == 0 && (uint *)param_1 == (uint *)0x0) {
//       if (uVar2 != param_2) {
//         *(undefined2 *)0x6410 = uVar3;
//       }
//     }
//     else {
//       *param_1 = uVar2;
//     }
//   }
//   else {
// LAB_24dd_3c9e:
//     if (iVar5 != 0 || (uint *)param_1 != (uint *)0x0) {
//       *param_1 = 0;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3c4f;
begin
  { TODO: translate from asm/FUN_24dd_3c4f.s — UNMATCHED until an oracle passes }
end;

