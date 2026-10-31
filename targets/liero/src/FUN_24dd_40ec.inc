{ liero::FUN_24dd_40ec — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; real-mode host-memory tests).
  Original assembly retained in asm/FUN_24dd_40ec.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_40ec(byte param_1,undefined4 param_2)
//
// {
//   byte *pbVar1;
//
//   pbVar1 = (byte *)((uint)(param_1 >> 3) + (int)param_2);
//   *pbVar1 = *pbVar1 | '\x01' << (param_1 & 7);
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_40ec(param_1: Byte; param_2: Longint);
var
  pointerOffset: Word;
  pointerSegment: Word;
  byteOffset: Word;
  bitMask: Byte;
  physicalAddress: Longint;
begin
  pointerOffset := Word(param_2);
  pointerSegment := Word(param_2 shr 16);
  byteOffset := pointerOffset + (param_1 shr 3);
  byteOffset := byteOffset and $FFFF;
  physicalAddress := ((Longint(pointerSegment) shl 4) + byteOffset)
    and $FFFFF;
  bitMask := 1 shl (param_1 and 7);
  RealModeMemory[physicalAddress] :=
    RealModeMemory[physicalAddress] or bitMask;
end;
