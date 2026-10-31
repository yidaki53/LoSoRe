{ liero::FUN_1000_0c7f — assembly-reviewed Pascal reconstruction
  (oracle: raw assembly review; host tests not run).
  Source: asm/FUN_1000_0c7f.s; Ghidra reference is embedded below.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_1000_0c7f(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6)
// 
// {
//   byte bVar1;
//   int iVar2;
//   int iVar3;
//   uint uVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   FUN_24dd_0530();
//   local_3 = 1;
//   uVar4 = param_4 - param_6 >> 0xf;
//   if ((((int)((param_4 - param_6 ^ uVar4) - uVar4) < 0xa1) &&
//       (uVar4 = param_3 - param_5 >> 0xf, (int)((param_3 - param_5 ^ uVar4) - uVar4) < 0xa1)) ||
//      ((uVar4 = param_2 - param_6 >> 0xf, (int)((param_2 - param_6 ^ uVar4) - uVar4) < 0xa1 &&
//       (uVar4 = param_1 - param_5 >> 0xf, (int)((param_1 - param_5 ^ uVar4) - uVar4) < 0xa1)))) {
//     local_3 = 0;
//   }
//   else {
//     iVar2 = param_6 + -3;
//     if (iVar2 <= param_6 + 3) {
//       while( true ) {
//         iVar3 = param_5 + -4;
//         if (iVar3 <= param_5 + 4) {
//           while( true ) {
//             iVar5 = 0x20;
//             bVar1 = FUN_24dd_4161();
//             if ((*(byte *)(iVar5 + 0x14a0) & bVar1) != 0) {
//               return 0;
//             }
//             if (iVar3 == param_5 + 4) break;
//             iVar3 = iVar3 + 1;
//           }
//         }
//         if (iVar2 == param_6 + 3) break;
//         iVar2 = iVar2 + 1;
//       }
//     }
//   }
//   return local_3;
// }
// 
// --- end reference ---
function FUN_1000_0c7f(param_1, param_2, param_3, param_4, param_5, param_6: Integer): Byte;
var
  difference: Word;
  scanColumnFirst: Word;
  scanColumnLast: Word;
  scanRowFirst: Word;
  scanRowLast: Word;
  scanColumn: Word;
  scanRow: Word;
  pixelMask: Byte;
  pixelRow: Word;
  mapValue: Byte;
  resultValue: Byte;

  function AbsoluteDifference(leftValue, rightValue: Integer): Word;
  var
    rawDifference: Word;
    mask: Word;
  begin
    rawDifference := Word(Word(leftValue) - Word(rightValue));
    if SmallInt(rawDifference) < 0 then
      mask := $FFFF
    else
      mask := 0;
    AbsoluteDifference := Word((rawDifference xor mask) - mask);
  end;

  function ReadDosWord(address: Word): Word;
  begin
    ReadDosWord := Word(DosMemory[address]) or
      (Word(DosMemory[Word(address + 1)]) shl 8);
  end;

  function ReadFarWord(segment, offset: Word): Word;
  var
    firstAddress: Longint;
    secondAddress: Longint;
  begin
    firstAddress := ((Longint(segment) shl 4) + offset) and $FFFFF;
    secondAddress := ((Longint(segment) shl 4) + Word(offset + 1)) and
      $FFFFF;
    ReadFarWord := Word(RealModeMemory[firstAddress]) or
      (Word(RealModeMemory[secondAddress]) shl 8);
  end;

  function ReadGridCell(column, row: Word): Byte;
  var
    rootOffset: Word;
    rootSegment: Word;
    entryOffset: Word;
    rowOffset: Word;
    rowSegment: Word;
    cellAddress: Longint;
  begin
    rootOffset := ReadDosWord($6674);
    rootSegment := ReadDosWord($6676);
    entryOffset := Word(rootOffset + Word(column shl 2));
    rowOffset := ReadFarWord(rootSegment, entryOffset);
    rowSegment := ReadFarWord(rootSegment, Word(entryOffset + 2));
    cellAddress := ((Longint(rowSegment) shl 4) +
      Word(rowOffset + row)) and $FFFFF;
    ReadGridCell := RealModeMemory[cellAddress];
  end;

  function BitmapContains(column, row: Word): Boolean;
  begin
    RegisterAX := $0100 or ReadGridCell(column, row);
    RegisterDX := $0020;
    RegisterAX := Word(FUN_24dd_4161);
    pixelMask := Byte(RegisterAX);
    pixelRow := RegisterDX;
    mapValue := DosMemory[Word($14A0 + pixelRow)];
    BitmapContains := (mapValue and pixelMask) <> 0;
  end;

begin
  resultValue := 1;
  difference := AbsoluteDifference(param_4, param_6);
  if SmallInt(difference) <= $00A0 then
  begin
    difference := AbsoluteDifference(param_3, param_5);
    if SmallInt(difference) <= $00A0 then
      resultValue := 0;
  end;
  if resultValue <> 0 then
  begin
    difference := AbsoluteDifference(param_2, param_6);
    if SmallInt(difference) <= $00A0 then
    begin
      difference := AbsoluteDifference(param_1, param_5);
      if SmallInt(difference) <= $00A0 then
        resultValue := 0;
    end;
  end;

  if resultValue <> 0 then
  begin
    scanColumnFirst := Word(Word(param_6) + 3);
    scanColumnLast := Word(Word(param_6) - 3);
    if SmallInt(scanColumnLast) <= SmallInt(scanColumnFirst) then
    begin
      scanColumn := scanColumnLast;
      while True do
      begin
        scanRowFirst := Word(Word(param_5) + 4);
        scanRowLast := Word(Word(param_5) - 4);
        if SmallInt(scanRowLast) <= SmallInt(scanRowFirst) then
        begin
          scanRow := scanRowLast;
          while True do
          begin
            if BitmapContains(scanRow, scanColumn) then
            begin
              resultValue := 0;
              RegisterAX := RegisterAX and $FF00;
              FUN_1000_0c7f := resultValue;
              Exit;
            end;
            if scanRow = scanRowFirst then
              Break;
            scanRow := Word(scanRow + 1);
          end;
        end;
        if scanColumn = scanColumnFirst then
          Break;
        scanColumn := Word(scanColumn + 1);
      end;
    end;
  end;

  RegisterAX := (RegisterAX and $FF00) or resultValue;
  FUN_1000_0c7f := resultValue;
end;
