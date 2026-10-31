{ liero::FUN_24dd_0642 — reviewed Pascal reconstruction (oracle: host-test).
  Host behavior passed; original-binary parity remains unverified.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C ---
// 
// void __cdecl16near FUN_24dd_0642(void)
// 
// {
//   undefined2 *puVar1;
//   undefined2 *puVar2;
//   int iVar3;
//   undefined2 *unaff_SI;
//   undefined2 *puVar4;
//   undefined2 unaff_DS;
//   
//   puVar4 = (undefined2 *)(*(int *)0xd8 + -0xc);
//   *(undefined2 *)0xd8 = puVar4;
//   for (iVar3 = 6; iVar3 != 0; iVar3 = iVar3 + -1) {
//     puVar2 = puVar4;
//     puVar4 = puVar4 + 1;
//     puVar1 = unaff_SI;
//     unaff_SI = unaff_SI + 1;
//     *puVar2 = *puVar1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_0642;
var
  sourceOffset: Word;
  destinationOffset: Word;
  byteIndex: Integer;
begin
  destinationOffset := (StackPointerD8 - 12) and $FFFF;
  StackPointerD8 := destinationOffset;
  for byteIndex := 0 to 11 do
  begin
    sourceOffset := (RegisterSI + byteIndex) and $FFFF;
    destinationOffset := (StackPointerD8 + byteIndex) and $FFFF;
    DosMemory[destinationOffset] := CodeMemory[sourceOffset];
  end;
  RegisterCX := 0;
end;
