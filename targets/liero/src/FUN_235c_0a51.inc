{ liero::FUN_235c_0a51 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0a51.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0a51.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_235c_0a51(void)
// 
// {
//   int iVar1;
//   uint uVar2;
//   int iVar3;
//   undefined4 uVar4;
//   int iVar5;
//   undefined2 uVar6;
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   local_3 = 0;
//   while( true ) {
//     if (*(char *)(local_3 + 0x67fc) != '\0') {
//       uVar4 = *(undefined4 *)((uint)local_3 * 10 + 0x6804);
//       uVar6 = (undefined2)((ulong)uVar4 >> 0x10);
//       iVar5 = (int)uVar4;
//       iVar1 = *(int *)(iVar5 + 8);
//       uVar2 = *(uint *)((uint)local_3 * 10 + 0x6809);
//       iVar3 = *(int *)((uint)local_3 * 10 + 0x680b);
//       if ((iVar1 < iVar3) || ((iVar1 <= iVar3 && (*(uint *)(iVar5 + 6) <= uVar2)))) {
//         FUN_235c_091d(CONCAT11((char)(uVar2 >> 8),local_3));
//         *(char *)0x67ce = *(char *)0x67ce + -1;
//       }
//     }
//     if (local_3 == 7) break;
//     local_3 = local_3 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_0a51;
begin
  { TODO: translate from asm/FUN_235c_0a51.s — UNMATCHED until an oracle passes }
end;

