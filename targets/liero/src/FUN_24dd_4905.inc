{ liero::FUN_24dd_4905 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host behavior tests).
  Original assembly retained in asm/FUN_24dd_4905.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_4905(undefined1 param_1,int param_2,undefined1 *param_3)
//
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//
//   puVar2 = (undefined1 *)param_3;
//   for (; param_2 != 0; param_2 = param_2 + -1) {
//     puVar1 = puVar2;
//     puVar2 = puVar2 + 1;
//     *puVar1 = param_1;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_4905(param_1: Byte; param_2: Integer; param_3: Pointer);
var
  destination: ^Byte;
  remaining: Word;
begin
  destination := param_3;
  remaining := Word(param_2);
  while remaining <> 0 do
  begin
    destination^ := param_1;
    Inc(destination);
    Dec(remaining);
  end;
end;
