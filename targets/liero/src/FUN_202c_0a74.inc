{ liero::FUN_202c_0a74 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0a74.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0a74.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_202c_0a74(int param_1,int param_2,int param_3)
// 
// {
//   byte bVar1;
//   int iVar2;
//   undefined2 unaff_DS;
//   int local_8;
//   int local_6;
//   
//   if (param_3 <= param_3 + param_1) {
//     local_6 = param_3;
//     while( true ) {
//       if (param_2 <= param_2 + param_1) {
//         local_8 = param_2;
//         while( true ) {
//           iVar2 = 0x20;
//           bVar1 = FUN_24dd_4161();
//           if (((((*(byte *)(iVar2 + 0x14a0) & bVar1) != 0) && (-1 < local_8)) && (local_8 < 0x15e))
//              && ((-1 < local_6 && (local_6 < 0x1f8)))) {
//             return 0;
//           }
//           if (local_8 == param_2 + param_1) break;
//           local_8 = local_8 + 1;
//         }
//       }
//       if (local_6 == param_3 + param_1) break;
//       local_6 = local_6 + 1;
//     }
//   }
//   return 1;
// }
// 
// --- end reference ---
procedure FUN_202c_0a74;
begin
  { TODO: translate from asm/FUN_202c_0a74.s — UNMATCHED until an oracle passes }
end;

