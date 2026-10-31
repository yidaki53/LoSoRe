{ stickman::FUN_410e_0392 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_410e_0392.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_410e_0392.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_410e_0392(undefined4 param_1)
// 
// {
//   byte bVar1;
//   int iVar2;
//   uint uVar3;
//   uint extraout_DX;
//   uint extraout_DX_00;
//   uint extraout_DX_01;
//   uint uVar4;
//   uint uVar5;
//   int iVar6;
//   int iVar7;
//   undefined2 uVar8;
//   undefined2 uVar9;
//   undefined2 unaff_DS;
//   
//   uVar8 = (undefined2)((ulong)param_1 >> 0x10);
//   iVar6 = (int)param_1;
//   uVar3 = *(int *)(iVar6 + 4) - 2;
//   uVar9 = (undefined2)((ulong)*(undefined4 *)(iVar6 + 0xc) >> 0x10);
//   iVar7 = (int)*(undefined4 *)(iVar6 + 0xc);
//   uVar4 = 0;
//   uVar5 = *(uint *)(iVar6 + 8);
// LAB_410e_03a8:
//   do {
//     *(undefined1 *)0xeb13 = 0;
//     bVar1 = FUN_410e_030d();
//     iVar2 = 1;
//     if ((bVar1 == 8) || (bVar1 == 0x13)) {
// LAB_410e_03ec:
//       do {
//         if (uVar4 == 0) break;
//         FUN_410e_047c();
//         FUN_410e_047c();
//         FUN_410e_047c();
//         uVar4 = uVar4 - 1;
//         iVar2 = iVar2 + -1;
//         uVar3 = extraout_DX_00;
//       } while (iVar2 != 0);
//       goto LAB_410e_03a8;
//     }
//     if (bVar1 == 4) {
// LAB_410e_0404:
//       do {
//         if ((uVar4 == uVar5) || (*(byte *)(uVar4 + iVar7) < 0x20)) break;
//         FUN_410e_047c();
//         uVar4 = uVar4 + 1;
//         iVar2 = iVar2 + -1;
//         uVar3 = extraout_DX_01;
//       } while (iVar2 != 0);
//     }
//     else {
//       iVar2 = 0;
//       if ((bVar1 == 0x1b) || (bVar1 == 1)) goto LAB_410e_03ec;
//       if (bVar1 == 6) goto LAB_410e_0404;
//       if (bVar1 == 0x1a) {
//         if (*(char *)0xeb03 != '\0') {
//           *(undefined1 *)(uVar4 + iVar7) = 0x1a;
//           iVar7 = uVar4 + 1;
// LAB_410e_042e:
//           *(undefined2 *)(iVar6 + 8) = 0;
//           *(int *)(iVar6 + 10) = iVar7;
//           return;
//         }
//       }
//       else {
//         if (bVar1 == 0xd) {
//           FUN_410e_0475();
//           *(undefined2 *)(uVar4 + iVar7) = 0xa0d;
//           iVar7 = uVar4 + 2;
//           goto LAB_410e_042e;
//         }
//         if ((0x1f < bVar1) && (uVar4 != uVar3)) {
//           *(byte *)(uVar4 + iVar7) = bVar1;
//           uVar4 = uVar4 + 1;
//           FUN_410e_047c();
//           uVar3 = extraout_DX;
//           if (uVar5 < uVar4) {
//             uVar5 = uVar4;
//           }
//         }
//       }
//     }
//   } while( true );
// }
// 
// --- end reference ---
procedure FUN_410e_0392(param_1: Longint);
begin
  { TODO: translate from asm/FUN_410e_0392.s — UNMATCHED until an oracle passes }
end;

