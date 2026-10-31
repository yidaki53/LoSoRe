{ liero::FUN_24dd_24ba — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_24ba.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_24ba.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 __cdecl16near FUN_24dd_24ba(void)
// 
// {
//   byte bVar1;
//   undefined2 in_AX;
//   byte bVar2;
//   byte bVar3;
//   uint in_DX;
//   undefined2 *unaff_DI;
//   undefined2 unaff_ES;
//   
//   bVar3 = (byte)(in_DX / 100);
//   bVar2 = (byte)(in_DX % 100);
//   bVar1 = bVar3 % 10;
//   bVar3 = bVar3 / 10 << 4 | bVar1;
//   *unaff_DI = CONCAT11(bVar3,bVar2 % 10 | bVar2 / 10 << 4);
//   return CONCAT22(CONCAT11(bVar3,bVar1),in_AX);
// }
// 
// --- end reference ---
function FUN_24dd_24ba: Longint;
var
  originalAX: Word;
  originalCX: Word;
  inputValue: Word;
  hundreds: Word;
  remainder: Word;
  hundredsPacked: Byte;
  remainderPacked: Byte;
  physicalAddress: Longint;
  returnedBits: LongWord;
begin
  originalAX := RegisterAX;
  originalCX := RegisterCX;
  inputValue := RegisterDX;
  hundreds := inputValue div 100;
  remainder := inputValue mod 100;
  if hundreds > 255 then
  begin
    RunError(200);
    Exit;
  end;
  hundredsPacked := Byte(((hundreds div 10) shl 4) or (hundreds mod 10));
  remainderPacked := Byte(((remainder div 10) shl 4) or (remainder mod 10));
  physicalAddress := ((Longint(RegisterES) shl 4) + RegisterDI) and $FFFFF;
  RealModeMemory[physicalAddress] := remainderPacked;
  RealModeMemory[(physicalAddress + 1) and $FFFFF] := hundredsPacked;
  Inc(RegisterDI, 2);
  RegisterDX := (Word(hundredsPacked) shl 8) or Word(hundreds mod 10);
  RegisterAX := originalAX;
  RegisterCX := originalCX;
  RegisterCarryFlag := False;
  RegisterZeroFlag := remainderPacked = 0;
  returnedBits := (LongWord(RegisterDX) shl 16) or RegisterAX;
  FUN_24dd_24ba := Longint(returnedBits);
end;
