{ liero::FUN_24ba_00d8 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24ba_00d8.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24ba_00d8.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 __cdecl16far FUN_24ba_00d8(void)
// 
// {
//   undefined2 unaff_DS;
//   byte local_4;
//   
//   local_4 = 0xab;
//   while( true ) {
//     if (*(char *)(local_4 + 0x783b) != '\0') {
//       return 1;
//     }
//     if (local_4 == 1) break;
//     local_4 = local_4 - 1;
//   }
//   return 0;
// }
// 
// --- end reference ---
function FUN_24ba_00d8: Byte;
var
  index: Word;
begin
  for index := $AA downto 1 do
  begin
    if DosMemory[$783B + index] <> 0 then
    begin
      RegisterAX := (RegisterAX and $FF00) or 1;
      RegisterZeroFlag := False;
      RegisterCarryFlag := False;
      FUN_24ba_00d8 := 1;
      Exit;
    end;
  end;
  RegisterAX := RegisterAX and $FF00;
  RegisterZeroFlag := True;
  RegisterCarryFlag := False;
  FUN_24ba_00d8 := 0;
end;
