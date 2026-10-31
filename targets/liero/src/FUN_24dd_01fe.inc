{ liero::FUN_24dd_01fe — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_01fe.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_01fe.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16near FUN_24dd_01fe(void)
// 
// {
//   undefined2 uVar1;
//   undefined1 uVar2;
//   
//   FUN_24dd_020a();
//   uVar1 = FUN_24dd_020a();
//   uVar1 = CONCAT11((char)((uint)uVar1 >> 8),(char)uVar1 + '0');
//   FUN_24dd_0232(uVar1);
//   uVar2 = (undefined1)((uint)uVar1 >> 8);
//   return CONCAT11(uVar2,uVar2);
// }
// 
// --- end reference ---
function FUN_24dd_01fe: Word;
var
  resultWord: Word;
begin
  RegisterCX := (RegisterCX and $FF00) or 100;
  FUN_24dd_020a;
  RegisterCX := (RegisterCX and $FF00) or 10;
  resultWord := FUN_24dd_020a;
  FUN_24dd_01fe := resultWord;
  FUN_24dd_0232((resultWord and $FF00) or
    Word((Byte(resultWord) + Ord('0')) and $FF));
end;
