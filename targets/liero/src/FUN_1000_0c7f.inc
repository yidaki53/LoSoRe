{ liero::FUN_1000_0c7f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1000_0c7f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1000_0c7f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_1000_0c7f(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6)
// 
// {
//   byte bVar1;
//   int iVar2;
//   int iVar3;
//   uint uVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   FUN_24dd_0530();
//   local_3 = 1;
//   uVar4 = param_4 - param_6 >> 0xf;
//   if ((((int)((param_4 - param_6 ^ uVar4) - uVar4) < 0xa1) &&
//       (uVar4 = param_3 - param_5 >> 0xf, (int)((param_3 - param_5 ^ uVar4) - uVar4) < 0xa1)) ||
//      ((uVar4 = param_2 - param_6 >> 0xf, (int)((param_2 - param_6 ^ uVar4) - uVar4) < 0xa1 &&
//       (uVar4 = param_1 - param_5 >> 0xf, (int)((param_1 - param_5 ^ uVar4) - uVar4) < 0xa1)))) {
//     local_3 = 0;
//   }
//   else {
//     iVar2 = param_6 + -3;
//     if (iVar2 <= param_6 + 3) {
//       while( true ) {
//         iVar3 = param_5 + -4;
//         if (iVar3 <= param_5 + 4) {
//           while( true ) {
//             iVar5 = 0x20;
//             bVar1 = FUN_24dd_4161();
//             if ((*(byte *)(iVar5 + 0x14a0) & bVar1) != 0) {
//               return 0;
//             }
//             if (iVar3 == param_5 + 4) break;
//             iVar3 = iVar3 + 1;
//           }
//         }
//         if (iVar2 == param_6 + 3) break;
//         iVar2 = iVar2 + 1;
//       }
//     }
//   }
//   return local_3;
// }
// 
// --- end reference ---
procedure FUN_1000_0c7f;
begin
  { TODO: translate from asm/FUN_1000_0c7f.s — UNMATCHED until an oracle passes }
end;

