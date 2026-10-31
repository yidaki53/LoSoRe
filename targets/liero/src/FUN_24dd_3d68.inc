{ liero::FUN_24dd_3d68 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host behavior tests).
  Original assembly retained in asm/FUN_24dd_3d68.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_3d68(int param_1,undefined1 *param_2,undefined1 *param_3)
// 
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   undefined1 *puVar3;
//   undefined1 *puVar4;
//   
//   puVar3 = (undefined1 *)param_3;
//   puVar4 = (undefined1 *)param_2;
//   for (; param_1 != 0; param_1 = param_1 + -1) {
//     puVar2 = puVar4;
//     puVar4 = puVar4 + 1;
//     puVar1 = puVar3;
//     puVar3 = puVar3 + 1;
//     *puVar2 = *puVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_3d68(param_1: Integer; param_2, param_3: Pointer);
var
  destination: ^Byte;
  source: ^Byte;
  remaining: Word;
begin
  destination := param_2;
  source := param_3;
  remaining := Word(param_1);
  while remaining <> 0 do
  begin
    destination^ := source^;
    Inc(destination);
    Inc(source);
    Dec(remaining);
  end;
end;
