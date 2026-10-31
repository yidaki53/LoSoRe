{ liero::FUN_1000_0961 — assembly-reviewed Pascal reconstruction
  (oracle: raw assembly review; host tests not run).
  Source: asm/FUN_1000_0961.s; Ghidra reference is embedded below.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_1000_0961(uint param_1,int param_2,int param_3)
// 
// {
//   uint uVar1;
//   byte bVar2;
//   int iVar3;
//   int iVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   
//   FUN_24dd_0530();
//   iVar3 = param_3 + -2;
//   if (iVar3 <= param_3 + 2) {
//     while( true ) {
//       iVar4 = param_2 + -2;
//       if (iVar4 <= param_2 + 2) {
//         while( true ) {
//           iVar5 = 0x20;
//           bVar2 = FUN_24dd_4161();
//           if ((*(byte *)(iVar5 + 0x6604) & bVar2) != 0) {
//             return 0;
//           }
//           if (iVar4 == param_2 + 2) break;
//           iVar4 = iVar4 + 1;
//         }
//       }
//       if (iVar3 == param_3 + 2) break;
//       iVar3 = iVar3 + 1;
//     }
//   }
//   while( true ) {
//     iVar3 = 0x20;
//     bVar2 = FUN_24dd_4161();
//     if ((*(byte *)(iVar3 + 0x14c0) & bVar2) == 0) break;
//     param_2 = param_2 + 1;
//   }
//   if (*(byte *)0x669c != 0) {
//     uVar1 = 1;
//     while( true ) {
//       if ((((uVar1 != param_1) && (*(char *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -2) != '\0')
//            ) && (param_3 + -0x1e < *(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -0xe))) &&
//          (((*(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -0xe) < param_3 + -0x1e &&
//            (param_2 + -0x1e < *(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -10))) &&
//           (*(int *)((int)*(undefined4 *)0x6698 + uVar1 * 0xe + -10) < param_2 + -0x1e)))) {
//         return 0;
//       }
//       if (uVar1 == *(byte *)0x669c) break;
//       uVar1 = uVar1 + 1;
//     }
//   }
//   return 1;
// }
// 
// --- end reference ---
function FUN_1000_0961(param_1: Word; param_2, param_3: Integer): Byte;
var
  gridColumn: Word;
  gridRow: Word;
  scanColumnFirst: Word;
  scanColumnLast: Word;
  scanRowFirst: Word;
  scanRowLast: Word;
  entityIndex: Word;
  entityCount: Byte;
  entityRecordOffset: Word;
  aliveAddress: Longint;
  resultValue: Byte;
  entityRootOffset: Word;
  entityRootSegment: Word;
  aliveFlag: Byte;
  testValue: Byte;
  bitMask: Byte;
  bitRow: Word;

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

  function ReadEntityWord(index: Word; fieldOffset: Word): Word;
  var
    rootOffset: Word;
    rootSegment: Word;
    recordOffset: Word;
  begin
    rootOffset := ReadDosWord($6698);
    rootSegment := ReadDosWord($669A);
    recordOffset := Word(rootOffset + Word(index * $0E) - $000E +
      fieldOffset);
    ReadEntityWord := ReadFarWord(rootSegment, recordOffset);
  end;

  function BitmapContains(column, row: Word; baseAddress: Word): Boolean;
  begin
    RegisterAX := $0100 or ReadGridCell(column, row);
    RegisterDX := $0020;
    RegisterAX := Word(FUN_24dd_4161);
    bitMask := Byte(RegisterAX);
    bitRow := RegisterDX;
    testValue := DosMemory[Word(baseAddress + bitRow)];
    BitmapContains := (testValue and bitMask) <> 0;
  end;

begin
  resultValue := 0;

  scanColumnFirst := Word(Word(param_2) + 2);
  scanColumnLast := Word(Word(param_2) - 2);
  if SmallInt(scanColumnLast) <= SmallInt(scanColumnFirst) then
  begin
    gridColumn := scanColumnLast;
    while True do
    begin
      scanRowFirst := Word(Word(param_3) + 2);
      scanRowLast := Word(Word(param_3) - 2);
      if SmallInt(scanRowLast) <= SmallInt(scanRowFirst) then
      begin
        gridRow := scanRowLast;
        while True do
        begin
          if BitmapContains(gridColumn, gridRow, $6604) then
          begin
            RegisterAX := (RegisterAX and $FF00);
            FUN_1000_0961 := 0;
            Exit;
          end;
          if gridRow = scanRowFirst then
            Break;
          gridRow := Word(gridRow + 1);
        end;
      end;
      if gridColumn = scanColumnFirst then
        Break;
      gridColumn := Word(gridColumn + 1);
    end;
  end;

  while BitmapContains(Word(param_2), Word(param_3), $14C0) do
    param_2 := SmallInt(Word(param_2) + 1);

  entityCount := DosMemory[$669C];
  if entityCount <> 0 then
  begin
    entityRootOffset := ReadDosWord($6698);
    entityRootSegment := ReadDosWord($669A);
    entityIndex := 1;
    while True do
    begin
      if entityIndex <> param_1 then
      begin
        entityRecordOffset := Word(entityRootOffset +
          Word(entityIndex * $0E));
        aliveAddress := ((Longint(entityRootSegment) shl 4) +
          Word(entityRecordOffset - 2)) and $FFFFF;
        aliveFlag := RealModeMemory[aliveAddress];
        if aliveFlag <> 0 then
        begin
          { The assembly compares each coordinate against the same
            param-0x1e threshold in opposite strict directions. }
          if SmallInt(Word(param_3 - $1E)) <
             SmallInt(ReadEntityWord(entityIndex, $0000)) then
          begin
            if SmallInt(ReadEntityWord(entityIndex, $0000)) <
               SmallInt(Word(param_3 - $1E)) then
            begin
              if SmallInt(Word(param_2 - $1E)) <
                 SmallInt(ReadEntityWord(entityIndex, $0004)) then
              begin
                if SmallInt(ReadEntityWord(entityIndex, $0004)) <
                   SmallInt(Word(param_2 - $1E)) then
                begin
                  RegisterAX := RegisterAX and $FF00;
                  FUN_1000_0961 := 0;
                  Exit;
                end;
              end;
            end;
          end;
        end;
      end;
      if entityIndex = entityCount then
        Break;
      entityIndex := Word(entityIndex + 1);
    end;
  end;

  resultValue := 1;
  RegisterAX := (RegisterAX and $FF00) or resultValue;
  FUN_1000_0961 := resultValue;
end;
