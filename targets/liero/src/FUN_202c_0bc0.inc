{ liero::FUN_202c_0bc0 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0bc0.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0bc0.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void FUN_202c_0bc0(void)
// 
// {
//   byte bVar1;
//   undefined2 uVar2;
//   undefined4 uVar3;
//   undefined4 uVar4;
//   undefined4 uVar5;
//   char cVar6;
//   int iVar7;
//   int iVar8;
//   int iVar9;
//   int iVar10;
//   undefined2 unaff_DS;
//   int local_e;
//   int local_c;
//   int local_6;
//   int local_4;
//   
//   uVar2 = *(undefined2 *)0x6602;
//   *(undefined2 *)0x6412 = *(undefined2 *)0x6600;
//   *(undefined2 *)0x6414 = uVar2;
//   cVar6 = FUN_24dd_4654(7);
//   **(char **)*(undefined4 *)0x6674 = cVar6 + '\f';
//   local_4 = 1;
//   while( true ) {
//     iVar7 = FUN_24dd_4654(7);
//     *(char *)*(undefined4 *)((int)*(undefined4 *)0x6674 + local_4 * 4) =
//          (char)((uint)*(byte *)*(undefined4 *)((int)*(undefined4 *)0x6674 + (local_4 + -1) * 4) +
//                 iVar7 + 0xc >> 1);
//     if (local_4 == 0x15d) break;
//     local_4 = local_4 + 1;
//   }
//   local_4 = 1;
//   while( true ) {
//     iVar7 = FUN_24dd_4654(7);
//     *(undefined1 *)((int)*(undefined4 *)*(undefined4 *)0x6674 + local_4) =
//          (char)((uint)*(byte *)((int)*(undefined4 *)*(undefined4 *)0x6674 + local_4 + -1) + iVar7 +
//                 0xc >> 1);
//     if (local_4 == 0x1f7) break;
//     local_4 = local_4 + 1;
//   }
//   local_4 = 1;
//   while( true ) {
//     local_6 = 1;
//     while( true ) {
//       iVar7 = FUN_24dd_4654(8);
//       uVar3 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_4 * 4);
//       uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + (local_4 + -1) * 4);
//       uVar5 = *(undefined4 *)((int)*(undefined4 *)0x6674 + local_4 * 4);
//       *(undefined1 *)((int)uVar5 + local_6) =
//            (char)((ulong)((uint)*(byte *)((int)uVar4 + local_6) +
//                          (uint)*(byte *)((int)uVar3 + local_6 + -1) + iVar7 + 0xc) / 3);
//       if (local_6 == 0x1f7) break;
//       local_6 = local_6 + 1;
//     }
//     if (local_4 == 0x15d) break;
//     local_4 = local_4 + 1;
//   }
//   iVar7 = FUN_24dd_4654(100);
//   if (0 < iVar7) {
//     local_4 = 1;
//     while( true ) {
//       iVar8 = FUN_24dd_4654(0x1f8);
//       iVar8 = iVar8 + -8;
//       iVar9 = FUN_24dd_4654(0x15e);
//       iVar9 = iVar9 + -8;
//       iVar10 = FUN_24dd_4654(4);
//       iVar10 = iVar10 + 0x45;
//       local_c = 0;
//       while( true ) {
//         local_e = 0;
//         while( true ) {
//           if ((((*(char *)((int)*(undefined4 *)0x6678 + iVar10 * 0x100 + local_e * 0x10 + local_c)
//                  != '\0') && ((uint)(iVar8 + local_c) < 0x8000)) && (iVar8 + local_c < 0x1f8)) &&
//              (((uint)(iVar9 + local_e) < 0x8000 && (iVar9 + local_e < 0x15e)))) {
//             uVar3 = *(undefined4 *)((int)*(undefined4 *)0x6674 + (iVar9 + local_e) * 4);
//             bVar1 = *(byte *)((int)uVar3 + iVar8 + local_c);
//             if ((bVar1 < 0xb0) || (0xb4 < bVar1)) {
//               uVar3 = *(undefined4 *)((int)*(undefined4 *)0x6674 + (iVar9 + local_e) * 4);
//               *(undefined1 *)((int)uVar3 + iVar8 + local_c) =
//                    *(undefined1 *)
//                     ((int)*(undefined4 *)0x6678 + iVar10 * 0x100 + local_e * 0x10 + local_c);
//             }
//             else {
//               uVar3 = *(undefined4 *)((int)*(undefined4 *)0x6674 + (iVar9 + local_e) * 4);
//               uVar4 = *(undefined4 *)((int)*(undefined4 *)0x6674 + (iVar9 + local_e) * 4);
//               *(undefined1 *)((int)uVar4 + iVar8 + local_c) =
//                    (char)((uint)*(byte *)((int)uVar3 + iVar8 + local_c) +
//                           (uint)*(byte *)((int)*(undefined4 *)0x6678 + iVar10 * 0x100 +
//                                           local_e * 0x10 + local_c) >> 1);
//             }
//           }
//           if (local_e == 0xf) break;
//           local_e = local_e + 1;
//         }
//         if (local_c == 0xf) break;
//         local_c = local_c + 1;
//       }
//       if (local_4 == iVar7) break;
//       local_4 = local_4 + 1;
//     }
//   }
//   iVar7 = FUN_24dd_4654(0xf);
//   if (0 < iVar7) {
//     local_4 = 1;
//     while( true ) {
//       iVar8 = FUN_24dd_4654(0x1f8);
//       iVar9 = FUN_24dd_4654(0x15e);
//       iVar10 = FUN_24dd_4654(4);
//       FUN_202c_032d(0,(int)*(undefined4 *)0x6678 + (iVar10 + 0x38) * 0x100,
//                     (int)((ulong)*(undefined4 *)0x6678 >> 0x10),iVar9 + -8,iVar8 + -8);
//       if (local_4 == iVar7) break;
//       local_4 = local_4 + 1;
//     }
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_202c_0bc0;
begin
  { TODO: translate from asm/FUN_202c_0bc0.s — UNMATCHED until an oracle passes }
end;

