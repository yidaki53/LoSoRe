{ stickman::FUN_42b5_141f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_42b5_141f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_42b5_141f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_42b5_141f(void)
// 
// {
//   undefined1 *puVar1;
//   byte bVar2;
//   undefined1 uVar3;
//   int in_CX;
//   int iVar4;
//   undefined2 in_DX;
//   int extraout_DX;
//   int iVar5;
//   int extraout_DX_00;
//   int extraout_DX_01;
//   int extraout_DX_02;
//   uint uVar6;
//   undefined1 *unaff_DI;
//   undefined1 *puVar7;
//   undefined2 unaff_ES;
//   undefined2 unaff_SS;
//   uint local_16 [7];
//   int local_8;
//   byte local_6;
//   int local_4;
//   
//   if (0xb < in_CX) {
//     in_CX = 0xb;
//   }
//   if (in_CX < -0xb) {
//     in_CX = -0xb;
//   }
//   local_6 = (byte)((uint)in_DX >> 8);
//   local_4 = in_CX;
//   FUN_42b5_1517();
//   local_8 = in_CX;
//   if (local_4 < 0) {
//     uVar6 = -local_4;
//   }
//   else {
//     uVar6 = local_4 + in_CX + 1;
//     if ((int)uVar6 < 0) {
//       local_16[0] = local_16[0] & 0xff00;
//       goto LAB_42b5_148c;
//     }
//   }
//   if (0xb < uVar6) {
//     uVar6 = 0xb;
//   }
//   bVar2 = *(byte *)((int)local_16 + uVar6);
//   *(undefined1 *)((int)local_16 + uVar6) = 0;
//   if (0x34 < bVar2) {
//     while (-1 < (int)(uVar6 - 1)) {
//       (&stack0xffe9)[uVar6] = (&stack0xffe9)[uVar6] + '\x01';
//       if ((byte)(&stack0xffe9)[uVar6] < 0x3a) goto LAB_42b5_148c;
//       (&stack0xffe9)[uVar6] = 0;
//       uVar6 = uVar6 - 1;
//     }
//     local_16[0] = 0x31;
//     local_8 = local_8 + 1;
//   }
// LAB_42b5_148c:
//   if (local_4 < 0) {
//     uVar3 = 0x20;
//     if ((local_6 & 0x80) != 0) {
//       uVar3 = 0x2d;
//     }
//     *unaff_DI = uVar3;
//     uVar3 = FUN_42b5_150b();
//     puVar7 = unaff_DI + 2;
//     unaff_DI[1] = uVar3;
//     if (extraout_DX_01 != -1) {
//       puVar1 = puVar7;
//       puVar7 = unaff_DI + 3;
//       *puVar1 = 0x2e;
//       do {
//         uVar3 = FUN_42b5_150b();
//         puVar1 = puVar7;
//         puVar7 = puVar7 + 1;
//         *puVar1 = uVar3;
//       } while (extraout_DX_02 != -1);
//     }
//     *puVar7 = 0x45;
//     uVar3 = 0x2b;
//     if (local_8 < 0) {
//       uVar3 = 0x2d;
//       local_8 = -local_8;
//     }
//     puVar7[1] = uVar3;
//     *(int *)(puVar7 + 2) = CONCAT11((char)(local_8 % 10),(char)(local_8 / 10)) + 0x3030;
//   }
//   else {
//     if ((local_6 & 0x80) != 0) {
//       puVar1 = unaff_DI;
//       unaff_DI = unaff_DI + 1;
//       *puVar1 = 0x2d;
//     }
//     iVar4 = local_8;
//     if (local_8 < 0) {
//       puVar1 = unaff_DI;
//       unaff_DI = unaff_DI + 1;
//       *puVar1 = 0x30;
//       iVar5 = local_4;
//     }
//     else {
//       do {
//         uVar3 = FUN_42b5_150b();
//         puVar1 = unaff_DI;
//         unaff_DI = unaff_DI + 1;
//         *puVar1 = uVar3;
//         iVar4 = iVar4 + -1;
//         iVar5 = extraout_DX;
//       } while (-1 < iVar4);
//     }
//     if (iVar5 != 0) {
//       puVar7 = unaff_DI + 1;
//       *unaff_DI = 0x2e;
//       do {
//         iVar4 = iVar4 + 1;
//         if (iVar4 == 0) break;
//         puVar1 = puVar7;
//         puVar7 = puVar7 + 1;
//         *puVar1 = 0x30;
//         iVar5 = iVar5 + -1;
//       } while (iVar5 != 0);
//       while (-1 < iVar5 + -1) {
//         uVar3 = FUN_42b5_150b();
//         puVar1 = puVar7;
//         puVar7 = puVar7 + 1;
//         *puVar1 = uVar3;
//         iVar5 = extraout_DX_00;
//       }
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_42b5_141f;
begin
  { TODO: translate from asm/FUN_42b5_141f.s — UNMATCHED until an oracle passes }
end;

