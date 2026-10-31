{ liero::FUN_235c_09eb — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_09eb.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_09eb.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_235c_09eb(char param_1)
// 
// {
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   local_3 = 0;
//   while( true ) {
//     if (*(char *)((uint)local_3 * 10 + 0x6808) == param_1) {
//       FUN_235c_091d(local_3);
//       *(char *)0x67ce = *(char *)0x67ce + -1;
//     }
//     if (local_3 == 7) break;
//     local_3 = local_3 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_09eb(param_1: Char);
var
  recordIndex: Byte;
  entryOffset: Word;
begin
  for recordIndex := 0 to 7 do
  begin
    entryOffset := $6808 + Word(recordIndex) * 10;
    if DosMemory[entryOffset] = Byte(param_1) then
    begin
      FUN_235c_091d(recordIndex);
      Dec(DosMemory[$67CE]);
    end;
  end;
end;
