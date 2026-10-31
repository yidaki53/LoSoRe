{ liero-dos::FUN_235c_001a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_001a.s via c->pascal+llm(http://localhost:8080,Ghidra); UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_001a.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __cdecl16near FUN_235c_001a(void)
// 
// {
//   byte bVar1;
//   undefined1 uVar2;
//   undefined2 unaff_DS;
//   
//   do {
//     bVar1 = in(*(undefined2 *)0x67d6);
//   } while ((bVar1 & 0x80) == 0);
//   uVar2 = in(*(undefined2 *)0x67d2);
//   return uVar2;
// }
// 
// --- end reference ---
function FUN_235c_001a: Byte;
var
  bVar1: Byte;
  uVar2: Byte;
  p: ^Byte;
begin
  repeat
    p := Pointer($67d6);
    bVar1 := p^;
  until (bVar1 and $80) <> 0;
  p := Pointer($67d2);
  uVar2 := p^;
  FUN_235c_001a := uVar2;
end;
