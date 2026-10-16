{ liero::FUN_1ec2_155e — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_155e.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_155e.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_1ec2_155e(undefined4 param_1)
// 
// {
//   int iVar1;
//   undefined2 uVar2;
//   undefined1 local_3;
//   
//   local_3 = 0;
//   while( true ) {
//     uVar2 = (undefined2)((ulong)param_1 >> 0x10);
//     iVar1 = (int)param_1;
//     FUN_2971_65df(0x1ec2,CONCAT11((char)((uint)local_3 * 3 >> 8),
//                                   *(undefined1 *)(iVar1 + (uint)local_3 * 3 + 2)),
//                   CONCAT11((char)((uint)local_3 * 3 >> 8),
//                            *(undefined1 *)(iVar1 + (uint)local_3 * 3 + 1)),
//                   CONCAT11((char)((uint)local_3 * 3 >> 8),*(undefined1 *)(iVar1 + (uint)local_3 * 3)
//                           ),local_3);
//     if (local_3 == 0xff) break;
//     local_3 = local_3 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_155e;
begin
  { TODO: translate from asm/FUN_1ec2_155e.s — UNMATCHED until an oracle passes }
end;

