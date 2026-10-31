{ liero::FUN_24dd_3d2f — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host command-line memory tests).
  Original assembly retained in asm/FUN_24dd_3d2f.s.
  The Ghidra decompiler reference is embedded below.
}
// --- reference: Ghidra decompiler C ---
// 
// undefined2 __cdecl16far FUN_24dd_3d2f(void)
// 
// {
//   undefined2 in_BX;
//   
//   FUN_24dd_3d36();
//   return in_BX;
// }
// 
// --- end reference ---
function FUN_24dd_3d2f: Word;
var
  previousAX: Word;
begin
  RegisterDX := 0;
  FUN_24dd_3d36;
  previousAX := RegisterAX;
  RegisterAX := RegisterBX;
  RegisterBX := previousAX;
  FUN_24dd_3d2f := RegisterAX;
end;
