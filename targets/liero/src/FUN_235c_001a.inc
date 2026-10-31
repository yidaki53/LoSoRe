{ liero::FUN_235c_001a — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_001a.s via skeleton; UNMATCHED until verify passes.
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
begin
  { TODO: not recovered. Assembly busy-waits for bit 7 at DS:$67d6 before
    reading the device data port at DS:$67d2; the hardware port values are
    not modeled by this runtime. }
end;
