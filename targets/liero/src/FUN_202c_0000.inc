{ liero::FUN_202c_0000 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0000.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0000.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined4 __stdcall16far
// FUN_202c_0000(uint param_1,int param_2,uint param_3,int param_4,uint param_5,int param_6,
//              uint param_7,int param_8)
// 
// {
//   code *pcVar1;
//   uint uVar2;
//   uint uVar3;
//   undefined2 uVar4;
//   int iVar5;
//   int iVar6;
//   undefined2 extraout_DX;
//   undefined2 uVar7;
//   
//   iVar5 = (param_6 - param_2) - (uint)(param_5 < param_1);
//   uVar2 = FUN_24dd_3d80();
//   iVar6 = (param_8 - param_4) - (uint)(param_7 < param_3);
//   uVar3 = FUN_24dd_3d80(uVar2,iVar5);
//   pcVar1 = (code *)swi(0x37);
//   (*pcVar1)(iVar6 + iVar5 + (uint)CARRY2(uVar3,uVar2));
//   uVar7 = extraout_DX;
//   FUN_24dd_32a9();
//   uVar4 = FUN_24dd_3249();
//   return CONCAT22(uVar7,uVar4);
// }
// 
// --- end reference ---
function FUN_202c_0000(param_1: Word; param_2: Integer; param_3: Word; param_4: Integer; param_5: Word; param_6: Integer; param_7: Word; param_8: Integer): Longint;
var
  firstProductLow: Word;
  firstProductHigh: Word;
begin
  { The first two 32-bit differences and products are directly visible in
    the retained instructions. The following INT 37h supplies state used by
    the return path, so that part remains explicitly unrecovered. }
  RegisterAX := Word(param_5 - param_1);
  RegisterDX := Word(Word(param_6) - Word(param_2) -
    Ord(Word(param_5) < Word(param_1)));
  RegisterCX := RegisterAX;
  RegisterBX := RegisterDX;
  FUN_24dd_3d80;
  firstProductLow := RegisterAX;
  firstProductHigh := RegisterDX;

  RegisterAX := Word(param_7 - param_3);
  RegisterDX := Word(Word(param_8) - Word(param_4) -
    Ord(Word(param_7) < Word(param_3)));
  RegisterCX := RegisterAX;
  RegisterBX := RegisterDX;
  FUN_24dd_3d80;

  RegisterAX := RegisterAX + firstProductLow;
  RegisterDX := RegisterDX + firstProductHigh +
    Ord(RegisterAX < firstProductLow);
  { TODO: not recovered past INT 37h. Its effect on AX:DX (and subsequent
    helper calls) is unavailable, so no return value is fabricated. }
end;
