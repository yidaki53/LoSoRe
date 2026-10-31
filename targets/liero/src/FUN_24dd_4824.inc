{ liero::FUN_24dd_4824 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_4824.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_4824.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __stdcall16far FUN_24dd_4824(int *param_1,byte *param_2)
// 
// {
//   undefined2 uVar1;
//   uint uVar2;
//   int iVar3;
//   byte *pbVar4;
//   bool bVar5;
//   
//   bVar5 = false;
//   uVar2 = (uint)*param_2;
//   pbVar4 = (byte *)param_2;
//   while ((pbVar4 = pbVar4 + 1, uVar2 != 0 && (bVar5 = *pbVar4 < 0x20, *pbVar4 == 0x20))) {
//     uVar2 = uVar2 - 1;
//   }
//   uVar1 = FUN_24dd_4732();
//   if ((bVar5) || (iVar3 = 0, uVar2 != 0)) {
//     iVar3 = (int)pbVar4 - (int)(byte *)param_2;
//     uVar1 = 0;
//   }
//   *param_1 = iVar3;
//   return uVar1;
// }
// 
// --- end reference ---
function FUN_24dd_4824(param_1, param_2: Pointer): Word;
var
  source: PByte;
  consumedOutput: PByte;
  stringLength: Byte;
  skippedSpaces: Word;
  copiedIndex: Word;
  parsedValue: Longint;
  consumedCharacters: Word;
begin
  source := PByte(param_2);
  consumedOutput := PByte(param_1);
  stringLength := source^;
  Inc(source);

  if stringLength <> 0 then
    for copiedIndex := 0 to stringLength - 1 do
    begin
      DosMemory[$7001 + copiedIndex] := source^;
      Inc(source);
    end;

  skippedSpaces := 0;
  while (skippedSpaces < stringLength) and
    (DosMemory[$7001 + skippedSpaces] = Ord(' ')) do
    Inc(skippedSpaces);

  RegisterES := 0;
  RegisterDI := $7001 + skippedSpaces;
  RegisterCX := stringLength - skippedSpaces;
  parsedValue := FUN_24dd_4732;
  if RegisterCX = 0 then
  begin
    consumedCharacters := 0;
    FUN_24dd_4824 := Word(parsedValue);
  end
  else
  begin
    consumedCharacters := 1 + skippedSpaces +
      (stringLength - skippedSpaces - RegisterCX);
    FUN_24dd_4824 := 0;
  end;
  consumedOutput^ := Byte(consumedCharacters);
  Inc(consumedOutput);
  consumedOutput^ := Byte(consumedCharacters shr 8);
end;
