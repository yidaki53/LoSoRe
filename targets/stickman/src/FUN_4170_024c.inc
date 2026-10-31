{ stickman::FUN_4170_024c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_4170_024c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_4170_024c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __stdcall16far FUN_4170_024c(undefined2 param_1,undefined4 param_2,undefined2 param_3)
// 
// {
//   undefined2 local_18;
//   undefined2 local_16;
//   undefined2 local_14;
//   undefined2 local_12;
//   undefined2 local_a;
//   uint local_6;
//   undefined2 local_4;
//   
//   local_4 = 0x4170;
//   local_6 = 0x1957;
//   FUN_42b5_04df();
//   local_18 = CONCAT11(0x3f,(undefined1)local_18);
//   local_16 = param_3;
//   local_14 = param_1;
//   local_12 = (undefined2)param_2;
//   local_a = (undefined2)((ulong)param_2 >> 0x10);
//   FUN_428f_0000(0x42b5,&local_18);
//   if ((local_6 & 1) == 0) {
//     local_4 = local_18;
//   }
//   else {
//     local_4 = 0;
//   }
//   return local_4;
// }
// 
// --- end reference ---
function FUN_4170_024c(param_1: Word; param_2: Longint; param_3: Word): Word;
begin
  { TODO: translate from asm/FUN_4170_024c.s — UNMATCHED until an oracle passes }
end;

