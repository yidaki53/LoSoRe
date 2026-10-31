{ liero::FUN_24dd_3fb1 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer test).
  Original assembly retained in asm/FUN_24dd_3fb1.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_3fb1(undefined1 param_1,undefined1 *param_2)
//
// {
//   *param_2 = 1;
//   ((undefined1 *)param_2)[1] = param_1;
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3fb1(param_1: Byte; param_2: Pointer);
var
  destinationByte: PByte;
begin
  destinationByte := PByte(param_2);
  destinationByte^ := 1;
  Inc(destinationByte);
  destinationByte^ := param_1;
end;
