{ liero::FUN_24dd_3d80 — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host register tests).
  Original assembly retained in asm/FUN_24dd_3d80.s.
  The Ghidra decompiler reference is embedded below.
}
// --- reference: Ghidra decompiler C ---
// 
// int __cdecl16far FUN_24dd_3d80(void)
// 
// {
//   int in_AX;
//   int in_CX;
//   undefined2 unaff_DS;
//   
//   if (1 < *(byte *)0x6420) {
//     return in_AX * in_CX;
//   }
//   return in_AX * in_CX;
// }
// 
// --- end reference ---
function FUN_24dd_3d80: Integer;
var
  leftValue: QWord;
  rightValue: QWord;
  product: QWord;
begin
  leftValue := (QWord(RegisterDX) shl 16) or RegisterAX;
  rightValue := (QWord(RegisterBX) shl 16) or RegisterCX;
  product := leftValue * rightValue;
  RegisterAX := Word(product);
  RegisterDX := Word(product shr 16);
  FUN_24dd_3d80 := Integer(RegisterAX);
end;
