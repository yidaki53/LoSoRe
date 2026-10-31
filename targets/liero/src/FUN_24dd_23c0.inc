{ liero::FUN_24dd_23c0 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_23c0.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_23c0.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 __cdecl16near FUN_24dd_23c0(void)
// 
// {
//   uint uVar1;
//   undefined2 in_DX;
//   byte bVar2;
//   uint *unaff_SI;
//   undefined2 unaff_ES;
//   
//   uVar1 = *unaff_SI;
//   bVar2 = (byte)(uVar1 >> 8);
//   return CONCAT22(in_DX,((uint)(byte)((bVar2 >> 4) * '\n' + (bVar2 & 0xf)) * 10 + (uVar1 >> 4 & 0xf)
//                         ) * 10 + (uVar1 & 0xf));
// }
// 
// --- end reference ---
function FUN_24dd_23c0: Longint;
var
  packedValue: Word;
  highByte: Byte;
  lowByte: Byte;
  decimalValue: Word;
  returnedBits: LongWord;
begin
  packedValue := Word(RealModeMemory[
    ((Longint(RegisterES) shl 4) + RegisterSI) and $FFFFF]) or
    (Word(RealModeMemory[
      ((Longint(RegisterES) shl 4) + Word(RegisterSI + 1)) and $FFFFF]) shl 8);
  highByte := Byte(packedValue shr 8);
  lowByte := Byte(packedValue);
  decimalValue := Word(((highByte shr 4) * 10 + (highByte and $0F)) * 10 +
    ((lowByte shr 4) and $0F));
  decimalValue := Word(decimalValue * 10 + (lowByte and $0F));
  RegisterAX := decimalValue;
  RegisterZeroFlag := RegisterAX = 0;
  RegisterCarryFlag := False;
  returnedBits := (LongWord(RegisterDX) shl 16) or RegisterAX;
  FUN_24dd_23c0 := Longint(returnedBits);
end;
