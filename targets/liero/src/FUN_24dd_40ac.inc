{ liero::FUN_24dd_40ac — assembly-derived Pascal reconstruction
  (oracle: raw assembly review; host pointer tests).
  Original assembly retained in asm/FUN_24dd_40ac.s.
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
//
// void __stdcall16far FUN_24dd_40ac(uint param_1,undefined1 *param_2,undefined1 *param_3)
//
// {
//   undefined1 *puVar1;
//   undefined1 *puVar2;
//   uint uVar3;
//   byte bVar4;
//   undefined1 *puVar5;
//   undefined1 *puVar6;
//   undefined2 uVar7;
//
//   uVar7 = (undefined2)((ulong)param_3 >> 0x10);
//   puVar6 = (undefined1 *)param_3;
//   puVar5 = (undefined1 *)param_2;
//   bVar4 = (byte)(param_1 >> 8);
//   for (uVar3 = (uint)bVar4; uVar3 != 0; uVar3 = uVar3 - 1) {
//     puVar1 = puVar6;
//     puVar6 = puVar6 + 1;
//     *puVar1 = 0;
//   }
//   for (uVar3 = param_1 & 0xff; uVar3 != 0; uVar3 = uVar3 - 1) {
//     puVar2 = puVar6;
//     puVar6 = puVar6 + 1;
//     puVar1 = puVar5;
//     puVar5 = puVar5 + 1;
//     *puVar2 = *puVar1;
//   }
//   for (uVar3 = (uint)(byte)((' ' - (char)param_1) - bVar4); uVar3 != 0; uVar3 = uVar3 - 1) {
//     puVar1 = puVar6;
//     puVar6 = puVar6 + 1;
//     *puVar1 = 0;
//   }
//   return;
// }
//
// --- end reference ---
procedure FUN_24dd_40ac(param_1: Word; param_2, param_3: Pointer);
var
  sourceByte: PByte;
  destinationByte: PByte;
  leadingZeroCount: Byte;
  copyCount: Byte;
  trailingZeroCount: Byte;
begin
  leadingZeroCount := param_1 shr 8;
  copyCount := param_1 and $00FF;
  trailingZeroCount := 32 - leadingZeroCount - copyCount;
  destinationByte := PByte(param_3);
  while leadingZeroCount <> 0 do
  begin
    destinationByte^ := 0;
    Inc(destinationByte);
    Dec(leadingZeroCount);
  end;
  sourceByte := PByte(param_2);
  while copyCount <> 0 do
  begin
    destinationByte^ := sourceByte^;
    Inc(sourceByte);
    Inc(destinationByte);
    Dec(copyCount);
  end;
  while trailingZeroCount <> 0 do
  begin
    destinationByte^ := 0;
    Inc(destinationByte);
    Dec(trailingZeroCount);
  end;
end;
