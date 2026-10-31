{ stickman::FUN_410e_00e5 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_00e5.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_00e5.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_410e_00e5(void)
// 
// {
//   uint uVar1;
//   uint uVar2;
//   undefined1 uVar3;
//   byte extraout_DL;
//   byte bVar4;
//   undefined2 uVar5;
//   undefined2 unaff_DS;
//   
//   uVar1 = FUN_410e_0609();
//   FUN_410e_0609();
//   uVar3 = 0;
//   bVar4 = extraout_DL;
//   if ((extraout_DL == 0) && (bVar4 = 0x18, (byte)uVar1 < 4)) {
//     uVar3 = 1;
//   }
//   uVar5 = CONCAT11(bVar4,(char)(uVar1 >> 8) + -1);
//   uVar2 = uVar1 & 0xff;
//   if (0x18 < bVar4) {
//     uVar2 = CONCAT11(1,(byte)uVar1);
//   }
//   *(uint *)0xeb06 = uVar2;
//   *(undefined2 *)0xeb10 = uVar5;
//   *(undefined1 *)0xeb05 = uVar3;
//   *(undefined1 *)0xeb04 = 1;
//   *(undefined2 *)0xeb0a = 0;
//   *(undefined2 *)0xeb0c = uVar5;
//   return;
// }
// 
// --- end reference ---
procedure FUN_410e_00e5;
begin
  { TODO: translate from asm/FUN_410e_00e5.s — UNMATCHED until an oracle passes }
end;

