{ liero::FUN_235c_095c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_095c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_095c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far
// FUN_235c_095c(undefined1 param_1,undefined1 param_2,undefined2 param_3,undefined2 param_4)
// 
// {
//   undefined2 unaff_DS;
//   undefined1 local_4;
//   undefined1 local_3;
//   
//   local_4 = 0xff;
//   local_3 = 0;
//   do {
//     if (*(char *)(local_3 + 0x67fc) == '\0') {
//       local_4 = local_3;
//     }
//     local_3 = local_3 + 1;
//   } while ((local_4 == 0xff) && (local_3 != 8));
//   if (local_4 != 0xff) {
//     *(char *)0x67ce = *(char *)0x67ce + '\x01';
//     *(undefined2 *)((uint)local_4 * 10 + 0x6804) = param_3;
//     *(undefined2 *)((uint)local_4 * 10 + 0x6806) = param_4;
//     *(undefined1 *)((uint)local_4 * 10 + 0x6808) = param_2;
//     *(undefined2 *)((uint)local_4 * 10 + 0x6809) = 0;
//     *(undefined2 *)((uint)local_4 * 10 + 0x680b) = 0;
//     *(undefined1 *)((uint)local_4 * 10 + 0x680d) = param_1;
//     *(undefined1 *)(local_4 + 0x67fc) = 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_095c(param_1, param_2: Byte; param_3, param_4: Word);
var
  recordIndex: Byte;
  recordOffset: Word;
begin
  recordIndex := 0;
  while (recordIndex < 8) and (DosMemory[$67FC + recordIndex] <> 0) do
    Inc(recordIndex);
  if recordIndex = 8 then
    Exit;

  recordOffset := $6804 + Word(recordIndex) * 10;
  Inc(DosMemory[$67CE]);
  DosMemory[recordOffset] := Byte(param_3);
  DosMemory[recordOffset + 1] := Byte(param_3 shr 8);
  DosMemory[recordOffset + 2] := Byte(param_4);
  DosMemory[recordOffset + 3] := Byte(param_4 shr 8);
  DosMemory[recordOffset + 4] := param_2;
  DosMemory[recordOffset + 5] := 0;
  DosMemory[recordOffset + 6] := 0;
  DosMemory[recordOffset + 7] := 0;
  DosMemory[recordOffset + 8] := 0;
  DosMemory[recordOffset + 9] := param_1;
  DosMemory[$67FC + recordIndex] := 1;
end;
