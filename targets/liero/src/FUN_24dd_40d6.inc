{ liero::FUN_24dd_40d6 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host behavior test).
  Original assembly retained in asm/FUN_24dd_40d6.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_40d6(undefined2 param_1,undefined2 *param_2)
// 
// {
//   int iVar1;
//   undefined2 *puVar2;
//   
//   puVar2 = (undefined2 *)param_2;
//   *param_2 = param_1;
//   for (iVar1 = 0xf; puVar2 = puVar2 + 1, iVar1 != 0; iVar1 = iVar1 + -1) {
//     *puVar2 = 0;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_40d6(param_1: Word; param_2: Pointer);
var
  destination: ^Word;
  remaining: Word;
begin
  destination := param_2;
  destination^ := param_1;
  Inc(destination);
  remaining := 15;
  while remaining <> 0 do
  begin
    destination^ := 0;
    Inc(destination);
    Dec(remaining);
  end;
end;
