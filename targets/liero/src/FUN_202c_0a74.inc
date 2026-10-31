{ liero::FUN_202c_0a74 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_202c_0a74.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_202c_0a74.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_202c_0a74(int param_1,int param_2,int param_3)
// 
// {
//   byte bVar1;
//   int iVar2;
//   undefined2 unaff_DS;
//   int local_8;
//   int local_6;
//   
//   if (param_3 <= param_3 + param_1) {
//     local_6 = param_3;
//     while( true ) {
//       if (param_2 <= param_2 + param_1) {
//         local_8 = param_2;
//         while( true ) {
//           iVar2 = 0x20;
//           bVar1 = FUN_24dd_4161();
//           if (((((*(byte *)(iVar2 + 0x14a0) & bVar1) != 0) && (-1 < local_8)) && (local_8 < 0x15e))
//              && ((-1 < local_6 && (local_6 < 0x1f8)))) {
//             return 0;
//           }
//           if (local_8 == param_2 + param_1) break;
//           local_8 = local_8 + 1;
//         }
//       }
//       if (local_6 == param_3 + param_1) break;
//       local_6 = local_6 + 1;
//     }
//   }
//   return 1;
// }
// 
// --- end reference ---
function FUN_202c_0a74(param_1, param_2, param_3: Integer): Byte;
var
  xValue: Word;
  yValue: Word;
  xLimit: Word;
  yLimit: Word;
  rowTableOffset: Word;
  rowTableSegment: Word;
  rowEntryOffset: Word;
  rowEntryAddress: Longint;
  rowByteAddress: Longint;
  rowOffset: Word;
  rowSegment: Word;
  pixelOffset: Word;
  pixelAddress: Longint;
  bitAddress: Word;
  mapPixel: Byte;
begin
  { The loops use signed JG bounds and 16-bit arithmetic, then read the
    packed map bit before applying the screen-coordinate bounds checks. }
  { At the raw stack offsets, [BP+8] is the outer coordinate/x and [BP+6]
    is the inner coordinate/y. }
  xValue := Word(param_3);
  yValue := Word(param_2);
  xLimit := Word(Word(param_3) + Word(param_1));
  yLimit := Word(Word(param_2) + Word(param_1));

  if SmallInt(yValue) <= SmallInt(yLimit) then
  begin
    while True do
    begin
      if SmallInt(xValue) <= SmallInt(xLimit) then
      begin
        while True do
        begin
          rowTableOffset := Word(DosMemory[$6674]) or
            (Word(DosMemory[$6675]) shl 8);
          rowTableSegment := Word(DosMemory[$6676]) or
            (Word(DosMemory[$6677]) shl 8);
          RegisterES := rowTableSegment;
          rowEntryOffset := Word(rowTableOffset + Word(yValue shl 2));
          rowEntryAddress := ((Longint(rowTableSegment) shl 4) +
            rowEntryOffset) and $FFFFF;
          rowOffset := RealModeMemory[rowEntryAddress];
          rowByteAddress := ((Longint(rowTableSegment) shl 4) +
            Word(rowEntryOffset + 1)) and $FFFFF;
          rowOffset := rowOffset or
            (Word(RealModeMemory[rowByteAddress]) shl 8);
          rowByteAddress := ((Longint(rowTableSegment) shl 4) +
            Word(rowEntryOffset + 2)) and $FFFFF;
          rowSegment := RealModeMemory[rowByteAddress];
          rowByteAddress := ((Longint(rowTableSegment) shl 4) +
            Word(rowEntryOffset + 3)) and $FFFFF;
          rowSegment := rowSegment or
            (Word(RealModeMemory[rowByteAddress]) shl 8);
          RegisterES := rowSegment;
          RegisterDI := rowOffset;
          pixelOffset := Word(rowOffset + xValue);
          RegisterDI := pixelOffset;
          pixelAddress := ((Longint(rowSegment) shl 4) + pixelOffset) and
            $FFFFF;
          mapPixel := RealModeMemory[pixelAddress];

          RegisterAX := $0100 or mapPixel;
          RegisterDX := $0020;
          FUN_24dd_4161;
          RegisterDI := RegisterDX;
          bitAddress := Word($14A0 + RegisterDX);
          if (DosMemory[bitAddress] and Byte(RegisterAX)) <> 0 then
          begin
            RegisterZeroFlag := False;
            RegisterCarryFlag := False;
            if (SmallInt(xValue) >= 0) and
              (SmallInt(xValue) < $15E) and
              (SmallInt(yValue) >= 0) and
              (SmallInt(yValue) < $1F8) then
            begin
              RegisterAX := (RegisterAX and $FF00);
              FUN_202c_0a74 := 0;
              Exit;
            end;
          end
          else
          begin
            RegisterZeroFlag := True;
            RegisterCarryFlag := False;
          end;

          if xValue = xLimit then
            Break;
          Inc(xValue);
        end;
      end;

      if yValue = yLimit then
        Break;
      Inc(yValue);
    end;
  end;

  RegisterAX := (RegisterAX and $FF00) or 1;
  FUN_202c_0a74 := 1;
end;
