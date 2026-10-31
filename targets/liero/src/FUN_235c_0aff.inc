{ liero::FUN_235c_0aff — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0aff.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0aff.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 FUN_235c_0aff(uint param_1)
// 
// {
//   uint uVar1;
//   int iVar2;
//   
//   iVar2 = 0;
//   uVar1 = FUN_24dd_3d80();
//   return CONCAT22(iVar2 + (uint)CARRY2(param_1,uVar1),param_1 + uVar1);
// }
// 
// --- end reference ---
function FUN_235c_0aff(param_1: Longint): Longint;
var
  farPointer: LongWord;
  offsetValue: Word;
  segmentValue: Word;
  linearSegment: LongWord;
  resultBits: LongWord;
begin
  farPointer := LongWord(param_1);
  offsetValue := Word(farPointer);
  segmentValue := Word(farPointer shr 16);
  linearSegment := LongWord(segmentValue) shl 4;

  RegisterAX := Word(linearSegment);
  RegisterDX := Word(linearSegment shr 16);
  RegisterCX := RegisterAX;
  RegisterBX := RegisterDX;
  resultBits := LongWord(offsetValue) + RegisterCX;
  RegisterAX := Word(resultBits);
  RegisterDX := Word(RegisterBX + Word(resultBits shr 16));
  RegisterCarryFlag := False;
  RegisterZeroFlag := RegisterDX = 0;
  resultBits := (LongWord(RegisterDX) shl 16) or RegisterAX;
  FUN_235c_0aff := Longint(resultBits);
end;
