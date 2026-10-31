{ liero::FUN_1000_9e7a — partial assembly-reviewed Pascal reconstruction
  (oracle: raw assembly review; host tests not run; unsupported modes remain unknown).
  Source: asm/FUN_1000_9e7a.s; Ghidra reference is embedded below.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// undefined2 __cdecl16near FUN_1000_9e7a(void)
// 
// {
//   char cVar1;
//   int iVar2;
//   undefined1 extraout_AH;
//   uint uVar3;
//   int iVar4;
//   undefined2 uVar5;
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   local_3 = 0x10;
//   FUN_24dd_0530();
//   cVar1 = *(char *)0x66ac;
//   uVar3 = CONCAT11(extraout_AH,cVar1);
//   if (cVar1 != '\0') {
//     if (cVar1 != '\x01') {
//       if ((cVar1 != '\x02') && (cVar1 != '\x03')) goto LAB_1000_9f40;
//       uVar3 = *(uint *)0x66a3;
//       uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//       iVar4 = (int)*(undefined4 *)0x6670;
//       iVar2 = *(int *)(iVar4 + 0x42);
//       if (((int)uVar3 >> 0xf < iVar2) ||
//          (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0x40))))) {
// LAB_1000_9f3b:
//         uVar3 = CONCAT11((char)(uVar3 >> 8),1);
//       }
//       else {
//         uVar3 = *(uint *)0x66a3;
//         uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//         iVar4 = (int)*(undefined4 *)0x6670;
//         iVar2 = *(int *)(iVar4 + 0xec);
//         if (((int)uVar3 >> 0xf < iVar2) ||
//            (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0xea))))) goto LAB_1000_9f3b;
//         uVar3 = uVar3 & 0xff00;
//       }
//       local_3 = (undefined1)uVar3;
//       goto LAB_1000_9f40;
//     }
//     uVar3 = *(uint *)0x66a1;
//     uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//     iVar4 = (int)*(undefined4 *)0x6670;
//     iVar2 = *(int *)(iVar4 + 0x46);
//     if (((int)uVar3 >> 0xf < iVar2) ||
//        (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0x44))))) {
// LAB_1000_9efa:
//       uVar3 = CONCAT11((char)(uVar3 >> 8),1);
//     }
//     else {
//       uVar3 = *(uint *)0x66a1;
//       uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//       iVar4 = (int)*(undefined4 *)0x6670;
//       iVar2 = *(int *)(iVar4 + 0xf0);
//       if (((int)uVar3 >> 0xf < iVar2) ||
//          (((int)uVar3 >> 0xf <= iVar2 && (uVar3 <= *(uint *)(iVar4 + 0xee))))) goto LAB_1000_9efa;
//       uVar3 = uVar3 & 0xff00;
//     }
//     local_3 = (undefined1)uVar3;
//     goto LAB_1000_9f40;
//   }
//   uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//   iVar4 = (int)*(undefined4 *)0x6670;
//   iVar2 = *(int *)(iVar4 + 0x3a);
//   if ((iVar2 < 0) || ((iVar2 < 1 && (*(int *)(iVar4 + 0x38) == 0)))) {
// LAB_1000_9ebd:
//     local_3 = 1;
//   }
//   else {
//     uVar5 = (undefined2)((ulong)*(undefined4 *)0x6670 >> 0x10);
//     iVar4 = (int)*(undefined4 *)0x6670;
//     iVar2 = *(int *)(iVar4 + 0xe4);
//     if ((iVar2 < 0) || ((iVar2 < 1 && (*(int *)(iVar4 + 0xe2) == 0)))) goto LAB_1000_9ebd;
//     local_3 = 0;
//   }
//   uVar3 = CONCAT11(extraout_AH,local_3);
// LAB_1000_9f40:
//   return CONCAT11((char)(uVar3 >> 8),local_3);
// }
// 
// --- end reference ---
function FUN_1000_9e7a: Word;
var
  modeValue: Byte;
  resultValue: Byte;
  returnHighByte: Word;
  currentPosition: Longint;
  firstBound: Longint;
  secondBound: Longint;
  firstPlayerValue: Longint;
  secondPlayerValue: Longint;
  playerOffset: Word;
  playerSegment: Word;

  function ReadDosWord(address: Word): Word;
  begin
    ReadDosWord := Word(DosMemory[address]) or
      (Word(DosMemory[Word(address + 1)]) shl 8);
  end;

  function ReadDosLong(address: Word): Longint;
  var
    rawValue: LongWord;
  begin
    rawValue := LongWord(ReadDosWord(address)) or
      (LongWord(ReadDosWord(Word(address + 2))) shl 16);
    ReadDosLong := Longint(rawValue);
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

  function ReadPlayerLong(fieldOffset: Word): Longint;
  var
    rawValue: LongWord;
    lowWord: Word;
    highWord: Word;
  begin
    lowWord := ReadFarWord(playerSegment,
      Word(playerOffset + fieldOffset));
    highWord := ReadFarWord(playerSegment,
      Word(playerOffset + fieldOffset + 2));
    rawValue := LongWord(lowWord) or (LongWord(highWord) shl 16);
    ReadPlayerLong := Longint(rawValue);
  end;

begin
  modeValue := DosMemory[$66AC];
  returnHighByte := RegisterAX and $FF00;
  resultValue := 0;
  playerOffset := ReadDosWord($6670);
  playerSegment := ReadDosWord($6672);

  case modeValue of
    0:
      begin
        firstPlayerValue := ReadPlayerLong($0038);
        secondPlayerValue := ReadPlayerLong($00E2);
        if (firstPlayerValue < 1) or (secondPlayerValue < 1) then
          resultValue := 1;
      end;
    1:
      begin
        currentPosition := ReadDosLong($66A1);
        returnHighByte := Word(DosMemory[$66A2]) shl 8;
        firstBound := ReadPlayerLong($0044);
        secondBound := ReadPlayerLong($00EE);
        if (currentPosition <= firstBound) or
           (currentPosition <= secondBound) then
          resultValue := 1;
      end;
    2, 3:
      begin
        currentPosition := ReadDosLong($66A3);
        returnHighByte := Word(DosMemory[$66A4]) shl 8;
        firstBound := ReadPlayerLong($0040);
        secondBound := ReadPlayerLong($00EA);
        if (currentPosition <= firstBound) or
           (currentPosition <= secondBound) then
          resultValue := 1;
      end;
  else
    { The assembly reads an uninitialized stack byte for modes outside 0..3;
      the Ghidra initializer is not present in the machine code. }
    Exit;
  end;

  RegisterAX := returnHighByte or resultValue;
  FUN_1000_9e7a := RegisterAX;
end;
