{ liero::FUN_24dd_4161 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host register-state tests).
  Original assembly retained in asm/FUN_24dd_4161.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// int __cdecl16far FUN_24dd_4161(void)
//
// {
//   sbyte sVar1;
//   uint in_AX;
//   byte bVar2;
//   undefined2 in_DX;
//   byte bVar3;
//
//   bVar2 = (byte)in_AX >> 3;
//   bVar3 = (byte)((uint)in_DX >> 8);
//   if ((bVar3 <= bVar2) && ((byte)(bVar2 - bVar3) < (byte)in_DX)) {
//     sVar1 = (sbyte)(in_AX & 0xff07);
//     bVar2 = (byte)((in_AX & 0xff07) >> 8);
//     return CONCAT11(bVar2,bVar2 << sVar1 | bVar2 >> 8 - sVar1);
//   }
//   return (int)in_AX >> 0xf;
// }
//
// --- end reference ---
function FUN_24dd_4161: Integer;
var
  inputAX: Word;
  inputDX: Word;
  rowIndex: Byte;
  rowBase: Byte;
  rowOffset: Byte;
  rotationCount: Byte;
  rotatedByte: Byte;
begin
  inputAX := RegisterAX;
  inputDX := RegisterDX;
  rowIndex := Byte(inputAX) shr 3;
  rowBase := inputDX shr 8;
  rowOffset := rowIndex - rowBase;
  RegisterCX := (Word(rowOffset) shl 8) or 3;

  if (rowIndex < rowBase) or (rowOffset >= Byte(inputDX)) then
  begin
    RegisterDX := 0;
    if SmallInt(inputAX) < 0 then
      RegisterAX := $FFFF
    else
      RegisterAX := 0;
    FUN_24dd_4161 := SmallInt(RegisterAX);
    Exit;
  end;

  rotationCount := Byte(inputAX) and 7;
  RegisterCX := (Word(rowOffset) shl 8) or rotationCount;
  RegisterDX := rowOffset;
  rotatedByte := inputAX shr 8;
  while rotationCount <> 0 do
  begin
    rotatedByte := (rotatedByte shl 1) or (rotatedByte shr 7);
    Dec(rotationCount);
  end;
  RegisterAX := (inputAX and $FF00) or rotatedByte;
  FUN_24dd_4161 := SmallInt(RegisterAX);
end;
