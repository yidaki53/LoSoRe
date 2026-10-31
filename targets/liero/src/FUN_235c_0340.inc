{ liero::FUN_235c_0340 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0340.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0340.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// bool __cdecl16far FUN_235c_0340(void)
// 
// {
//   char cVar1;
//   
//   cVar1 = FUN_235c_1380();
//   if (cVar1 != '\0') {
//     FUN_2494_0010();
//   }
//   return cVar1 != '\0';
// }
// 
// --- end reference ---
function FUN_235c_0340: Boolean;
var
  detected: Boolean;
begin
  detected := FUN_235c_1380;
  if detected then
    FUN_2494_0010;
  FUN_235c_0340 := detected;
  if detected then
    RegisterAX := (RegisterAX and $FF00) or 1
  else
    RegisterAX := RegisterAX and $FF00;
end;
