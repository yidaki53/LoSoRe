{ stickman::FUN_3de3_0d8a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_3de3_0d8a.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_3de3_0d8a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_3de3_0d8a(void)
// 
// {
//   char cVar1;
//   uint uVar2;
//   int extraout_DX;
//   int iVar3;
//   int iVar4;
//   undefined2 uVar5;
//   undefined2 unaff_SS;
//   undefined2 unaff_DS;
//   undefined1 *puVar6;
//   undefined1 local_106 [256];
//   uint local_6;
//   int local_4;
//   
//   local_4 = 0x3de3;
//   uVar5 = 0x42b5;
//   local_6 = 0xebc5;
//   FUN_42b5_04df();
//   FUN_3de3_002d(0xd79,0x42b5);
//   do {
//     cVar1 = FUN_3de3_0a62();
//     if (cVar1 != '\0') {
//       FUN_3de3_002d(0xd88,uVar5);
//       return;
//     }
//     FUN_3de3_08cd();
//     *(int *)0x14e = *(int *)0x14e + 1;
//     if ((int)(uint)*(byte *)0x150 < *(int *)0x14e) {
//       *(undefined2 *)0x14e = 1;
//     }
//     puVar6 = local_106;
//     uVar5 = unaff_SS;
//     FUN_42b5_0cf4(*(undefined1 *)(*(int *)0x14e + 0x150));
//     FUN_42b5_0c51(0xd84,0x42b5);
//     FUN_3de3_002d(puVar6,uVar5);
//     iVar3 = extraout_DX;
//     local_6 = FUN_4170_0096();
//     local_4 = iVar3;
//     while( true ) {
//       uVar2 = FUN_4170_0096();
//       if ((iVar3 <= local_4) && ((iVar3 < local_4 || (uVar2 < local_6)))) break;
//       uVar2 = FUN_4170_0096();
//       iVar4 = local_4 + (uint)(0xfffd < local_6);
//       if ((iVar4 <= iVar3) && ((iVar4 < iVar3 || (local_6 + 2 < uVar2)))) break;
//       cVar1 = FUN_3de3_0a62();
//       if (cVar1 != '\0') break;
//       FUN_405f_017d();
//       iVar3 = iVar4;
//     }
//     uVar5 = 0x4170;
//   } while( true );
// }
// 
// --- end reference ---
procedure FUN_3de3_0d8a;
begin
  { TODO: translate from asm/FUN_3de3_0d8a.s — UNMATCHED until an oracle passes }
end;

