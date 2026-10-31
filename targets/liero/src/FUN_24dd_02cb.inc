{ liero::FUN_24dd_02cb — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_02cb.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_02cb.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __stdcall16far FUN_24dd_02cb(undefined4 *param_1)
// 
// {
//   undefined2 uVar1;
//   undefined2 uVar2;
//   undefined2 unaff_DS;
//   
//   uVar2 = (undefined2)((ulong)*param_1 >> 0x10);
//   uVar1 = (undefined2)*param_1;
//   *(undefined2 *)0x63ee = uVar1;
//   *(undefined2 *)0x63f0 = uVar2;
//   *(undefined2 *)0x63f6 = uVar1;
//   *(undefined2 *)0x63f8 = uVar2;
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_02cb(param_1: Pointer);
type
  PFarPointerValue = ^TFarPointerValue;
  TFarPointerValue = packed record
    Offset: Word;
    Segment: Word;
  end;
var
  farPointerValue: PFarPointerValue;
begin
  farPointerValue := PFarPointerValue(param_1);
  PointerOffset63EE := farPointerValue^.Offset;
  PointerSegment63F0 := farPointerValue^.Segment;
  PointerOffset63F6 := farPointerValue^.Offset;
  PointerSegment63F8 := farPointerValue^.Segment;
end;
