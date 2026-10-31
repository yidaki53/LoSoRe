{ stickman::FUN_42b5_0000 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_0000.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_0000.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_42b5_0000(void)
// 
// {
//   code *pcVar1;
//   int iVar2;
//   undefined2 in_BX;
//   undefined2 *puVar3;
//   undefined2 unaff_ES;
//   int unaff_SS;
//   
//   DAT_4473_036a = ((uint)&stack0x0013 >> 4) + unaff_SS;
//   DAT_4473_036e = DAT_4473_036a + DAT_4473_0364;
//   DAT_4473_0380 = *(undefined2 *)0x2;
//   DAT_4473_038a = 0xa9;
//   DAT_4473_038c = 0x42b5;
//   puVar3 = (undefined2 *)0xed16;
//   iVar2 = 0x13;
//   DAT_4473_036c = DAT_4473_036a;
//   DAT_4473_0378 = DAT_4473_036e;
//   DAT_4473_037c = DAT_4473_036e;
//   DAT_4473_0384 = DAT_4473_036e;
//   DAT_4473_0398 = unaff_ES;
//   do {
//     pcVar1 = (code *)swi(0x21);
//     (*pcVar1)();
//     *puVar3 = in_BX;
//     puVar3[1] = unaff_ES;
//     puVar3 = puVar3 + 2;
//     iVar2 = iVar2 + -1;
//   } while (iVar2 != 0);
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   pcVar1 = (code *)swi(0x21);
//   (*pcVar1)();
//   FUN_42b5_04f5();
//   FUN_42b5_0565();
//   FUN_42b5_04f5();
//   FUN_42b5_056a();
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_0000;
begin
  { TODO: translate from asm/FUN_42b5_0000.s — UNMATCHED until an oracle passes }
end;

