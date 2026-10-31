{ liero::FUN_24dd_492c — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; exhaustive range host test).
  Original assembly retained in asm/FUN_24dd_492c.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __cdecl16near FUN_24dd_492c(void)
//
// {
//   undefined2 *puVar1;
//   int iVar2;
//   undefined2 *puVar3;
//   undefined2 unaff_DS;
//
//   puVar3 = (undefined2 *)0x6426;
//   for (iVar2 = 0xb96; iVar2 != 0; iVar2 = iVar2 + -1) {
//     puVar1 = puVar3;
//     puVar3 = puVar3 + 1;
//     *puVar1 = 0;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_492c;
var
  destinationOffset: Word;
begin
  destinationOffset := $6426;
  while destinationOffset < $7B52 do
  begin
    DosMemory[destinationOffset] := 0;
    DosMemory[destinationOffset + 1] := 0;
    Inc(destinationOffset, 2);
  end;
end;
