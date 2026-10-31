{ liero::FUN_1ec2_13c5 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_1ec2_13c5.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_1ec2_13c5.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16far FUN_1ec2_13c5(void)
// 
// {
//   byte bVar1;
//   
//   do {
//     bVar1 = in(0x3da);
//   } while ((bVar1 & 8) != 0);
//   do {
//     bVar1 = in(0x3da);
//   } while ((bVar1 & 8) == 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_1ec2_13c5;
var
  status: Byte;
begin
  repeat
    status := ReadVideoStatusPort;
  until (status and $08) = 0;
  repeat
    status := ReadVideoStatusPort;
  until (status and $08) <> 0;
end;
