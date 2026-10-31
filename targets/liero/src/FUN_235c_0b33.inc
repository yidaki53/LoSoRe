{ liero::FUN_235c_0b33 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0b33.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0b33.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 FUN_235c_0b33(undefined2 param_1,undefined2 param_2)
// 
// {
//   undefined2 uVar1;
//   undefined2 uVar2;
//   undefined4 uVar3;
//   
//   uVar3 = FUN_235c_0aff(param_1,param_2);
//   uVar1 = FUN_24dd_3dbd(uVar3);
//   uVar2 = 0x10;
//   FUN_24dd_3dbd();
//   return CONCAT22(uVar1,uVar2);
// }
// 
// --- end reference ---
function FUN_235c_0b33(param_1, param_2: Word): Longint;
begin
  { TODO: Not recovered. The call enters the middle of FUN_24dd_40ac, so its
    buffer effects depend on incoming ES:DI, DS:SI, BX and stack state; the
    skipped CLD also makes REP direction depend on an unmodeled direction flag. }
end;
