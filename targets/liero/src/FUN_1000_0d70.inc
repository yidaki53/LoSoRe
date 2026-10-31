{ liero::FUN_1000_0d70 — assembly-reviewed Pascal reconstruction
  (oracle: raw assembly review; host tests not run).
  Source: asm/FUN_1000_0d70.s; Ghidra reference is embedded below.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined1 FUN_1000_0d70(int param_1,int param_2,byte param_3,byte param_4)
// 
// {
//   byte bVar1;
//   int iVar2;
//   int iVar3;
//   int iVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   int local_b;
//   int local_9;
//   
//   FUN_24dd_0530();
//   if (*(char *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 0x9a) != '\0') {
//     iVar2 = (param_2 - *(int *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 6)) + 7;
//     iVar3 = (param_1 - *(int *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 10)) + 5;
//     if (*(char *)((int)*(undefined4 *)0x6670 + (uint)param_4 * 0xaa + 0x9b) == '\0') {
//       iVar2 = 0xe - iVar2;
//     }
//     local_9 = iVar2 - (uint)param_3;
//     if (local_9 <= (int)((uint)param_3 + iVar2)) {
//       while( true ) {
//         iVar4 = (uint)param_3 + iVar3;
//         local_b = iVar3 - (uint)param_3;
//         if (local_b <= iVar4) {
//           while( true ) {
//             if ((((0 < local_9) && (local_9 < 0xe)) && (-1 < local_b)) && (local_b < 10)) {
//               iVar5 = 0x20;
//               bVar1 = FUN_24dd_4161();
//               if ((*(byte *)(iVar5 + 0x28) & bVar1) != 0) {
//                 return 1;
//               }
//             }
//             if (local_b == iVar4) break;
//             local_b = local_b + 1;
//           }
//         }
//         if (local_9 == (uint)param_3 + iVar2) break;
//         local_9 = local_9 + 1;
//       }
//     }
//   }
//   return 0;
// }
// 
// --- end reference ---
function FUN_1000_0d70(param_1, param_2: Integer; param_3, param_4: Byte): Byte;
var
  playerBaseOffset: Word;
  playerBaseSegment: Word;
  playerRecordOffset: Word;
  relativeX: Word;
  relativeY: Word;
  scanXFirst: Word;
  scanXLast: Word;
  scanYFirst: Word;
  scanYLast: Word;
  scanX: Word;
  scanY: Word;
  spriteBaseOffset: Word;
  spriteBaseSegment: Word;
  spriteAddress: Longint;
  frameIndex: Byte;
  pixelByte: Byte;
  pixelMask: Byte;
  pixelRow: Word;
  maskValue: Byte;
  resultValue: Byte;

  function ReadPlayerByte(fieldOffset: Word): Byte;
  var
    address: Longint;
  begin
    address := ((Longint(playerBaseSegment) shl 4) +
      Word(playerRecordOffset + fieldOffset)) and $FFFFF;
    ReadPlayerByte := RealModeMemory[address];
  end;

  function ReadPlayerWord(fieldOffset: Word): Word;
  var
    firstAddress: Longint;
    secondAddress: Longint;
  begin
    firstAddress := ((Longint(playerBaseSegment) shl 4) +
      Word(playerRecordOffset + fieldOffset)) and $FFFFF;
    secondAddress := ((Longint(playerBaseSegment) shl 4) +
      Word(playerRecordOffset + fieldOffset + 1)) and $FFFFF;
    ReadPlayerWord := Word(RealModeMemory[firstAddress]) or
      (Word(RealModeMemory[secondAddress]) shl 8);
  end;

begin
  resultValue := 0;
  playerBaseOffset := Word(DosMemory[$6670]) or
    (Word(DosMemory[$6671]) shl 8);
  playerBaseSegment := Word(DosMemory[$6672]) or
    (Word(DosMemory[$6673]) shl 8);
  playerRecordOffset := Word(playerBaseOffset +
    Word(Word(param_4) * $00AA));

  if ReadPlayerByte($009A) = 0 then
  begin
    RegisterAX := RegisterAX and $FF00;
    FUN_1000_0d70 := resultValue;
    Exit;
  end;

  relativeX := Word(Word(Word(param_2) - ReadPlayerWord($0006)) + 7);
  relativeY := Word(Word(Word(param_1) - ReadPlayerWord($000A)) + 5);
  if ReadPlayerByte($009B) = 0 then
    relativeX := Word(14 - relativeX);

  scanXFirst := Word(relativeX - param_3);
  scanXLast := Word(relativeX + param_3);
  if SmallInt(scanXFirst) <= SmallInt(scanXLast) then
  begin
    scanX := scanXFirst;
    while True do
    begin
      scanYFirst := Word(relativeY - param_3);
      scanYLast := Word(relativeY + param_3);
      if SmallInt(scanYFirst) <= SmallInt(scanYLast) then
      begin
        scanY := scanYFirst;
        while True do
        begin
          if (SmallInt(scanX) > 0) and (SmallInt(scanX) < 14) and
             (SmallInt(scanY) > -1) and (SmallInt(scanY) < 10) then
          begin
            frameIndex := ReadPlayerByte($00A1);
            spriteBaseOffset := Word(DosMemory[$6678]) or
              (Word(DosMemory[$6679]) shl 8);
            spriteBaseSegment := Word(DosMemory[$667A]) or
              (Word(DosMemory[$667B]) shl 8);
            spriteAddress := ((Longint(spriteBaseSegment) shl 4) +
              Word(spriteBaseOffset + Word(Word(frameIndex) shl 8) +
                Word(scanY shl 4) + scanX)) and $FFFFF;
            pixelByte := RealModeMemory[spriteAddress];
            RegisterAX := $0100 or pixelByte;
            RegisterDX := $0020;
            RegisterAX := Word(FUN_24dd_4161);
            pixelMask := Byte(RegisterAX);
            pixelRow := RegisterDX;
            maskValue := DosMemory[Word($0028 + pixelRow)];
            if (maskValue and pixelMask) <> 0 then
            begin
              resultValue := 1;
              RegisterAX := (RegisterAX and $FF00) or resultValue;
              FUN_1000_0d70 := resultValue;
              Exit;
            end;
          end;
          if scanY = scanYLast then
            Break;
          scanY := Word(scanY + 1);
        end;
      end;
      if scanX = scanXLast then
        Break;
      scanX := Word(scanX + 1);
    end;
  end;

  RegisterAX := RegisterAX and $FF00;
  FUN_1000_0d70 := resultValue;
end;
