{ liero::FUN_24dd_384a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_384a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_384a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_384a(void)
// 
// {
//   undefined1 *puVar1;
//   undefined4 uVar2;
//   uint uVar3;
//   uint in_DX;
//   int in_BX;
//   int iVar4;
//   undefined1 *puVar5;
//   undefined2 unaff_ES;
//   undefined2 unaff_DS;
//   bool bVar6;
//   
//   if (*(int *)0x6410 == 0) {
//     if (*(int *)(in_BX + 2) != -0x284e) {
//       *(undefined2 *)0x6410 = 0x69;
//       return;
//     }
//     do {
//       uVar3 = *(int *)(in_BX + 4) - *(int *)(in_BX + 8);
//       bVar6 = in_DX < uVar3;
//       in_DX = in_DX - uVar3;
//       if (bVar6) {
//         uVar3 = uVar3 + in_DX;
//         in_DX = 0;
//       }
//       uVar2 = *(undefined4 *)(in_BX + 0xc);
//       iVar4 = (int)uVar2;
//       puVar5 = (undefined1 *)(*(int *)(in_BX + 8) + iVar4);
//       for (; uVar3 != 0; uVar3 = uVar3 - 1) {
//         puVar1 = puVar5;
//         puVar5 = puVar5 + 1;
//         *puVar1 = 0x20;
//       }
//       iVar4 = (int)puVar5 - iVar4;
//       *(int *)(in_BX + 8) = iVar4;
//       if (iVar4 == *(int *)(in_BX + 4)) {
//         FUN_24dd_396c();
//       }
//     } while (in_DX != 0);
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_384a;
begin
  { TODO: translate from asm/FUN_24dd_384a.s — UNMATCHED until an oracle passes }
end;

