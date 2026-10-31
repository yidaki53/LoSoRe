{ stickman::FUN_1000_30c3 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_30c3.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_30c3.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_1000_30c3(void)
// 
// {
//   uint *puVar1;
//   uint uVar2;
//   uint uVar3;
//   int iVar4;
//   undefined2 unaff_DS;
//   
//   FUN_42b5_04df();
//   uVar2 = *(uint *)(*(int *)0x4fd * 0x80 + 0x2696);
//   iVar4 = (int)uVar2 >> 0xf;
//   if ((*(int *)0x4fb < iVar4) || ((*(int *)0x4fb <= iVar4 && (*(uint *)0x4f9 < uVar2)))) {
//     iVar4 = *(int *)(*(int *)0x4fd * 0x80 + 0x2696);
//     *(int *)0x4f9 = iVar4;
//     *(int *)0x4fb = iVar4 >> 0xf;
//   }
//   puVar1 = (uint *)0x501;
//   uVar2 = *puVar1;
//   *puVar1 = *puVar1 + 1;
//   *(int *)0x503 = *(int *)0x503 + (uint)(0xfffe < uVar2);
//   puVar1 = (uint *)0x4fd;
//   uVar2 = *puVar1;
//   *puVar1 = *puVar1 + 1;
//   *(int *)0x4ff = *(int *)0x4ff + (uint)(0xfffe < uVar2);
//   iVar4 = (int)*(uint *)0x26c4 >> 0xf;
//   if ((iVar4 < *(int *)0x4ff) || ((iVar4 <= *(int *)0x4ff && (*(uint *)0x26c4 < *(uint *)0x4fd)))) {
//     *(undefined2 *)0x4fd = 1;
//     *(undefined2 *)0x4ff = 0;
//   }
//   uVar2 = *(uint *)0x3aa;
//   uVar3 = *(uint *)0x505;
//   iVar4 = *(int *)0x507;
//   *(int *)0x505 = uVar2 + *(uint *)0x505;
//   *(int *)0x507 = ((int)uVar2 >> 0xf) + iVar4 + (uint)CARRY2(uVar2,uVar3);
//   FUN_1000_2e9e();
//   return;
// }
// 
// --- end reference ---
procedure FUN_1000_30c3;
begin
  { TODO: translate from asm/FUN_1000_30c3.s — UNMATCHED until an oracle passes }
end;

