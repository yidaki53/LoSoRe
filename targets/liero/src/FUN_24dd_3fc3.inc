{ liero::FUN_24dd_3fc3 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer tests).
  Original assembly retained in asm/FUN_24dd_3fc3.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_3fc3(int param_1,undefined1 *param_2,undefined1 *param_3)
//
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined1 *puVar3;
//
//   puVar3 = (undefined1 *)param_3;
//   puVar2 = (undefined1 *)param_2;
//   *param_3 = (char)param_1;
//   for (; puVar3 = puVar3 + 1, param_1 != 0; param_1 = param_1 + -1) {
//     puVar1 = puVar2;
//     puVar2 = puVar2 + 1;
//     *puVar3 = *puVar1;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_3fc3(param_1: Integer; param_2, param_3: Pointer);
var
  sourceByte: PByte;
  destinationByte: PByte;
  remainingBytes: Word;
begin
  sourceByte := PByte(param_2);
  destinationByte := PByte(param_3);
  remainingBytes := Word(param_1);
  destinationByte^ := Byte(remainingBytes);
  Inc(destinationByte);
  while remainingBytes <> 0 do
  begin
    destinationByte^ := sourceByte^;
    Inc(sourceByte);
    Inc(destinationByte);
    Dec(remainingBytes);
  end;
end;
