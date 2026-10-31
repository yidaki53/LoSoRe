{ liero::FUN_1ec2_00a5 — copies rows of bytes with a 320-byte stride.
  Oracle: none; not compared with the DOS executable. }
procedure FUN_1ec2_00a5(param_1, param_2: Integer; param_3, param_4: Pointer);
var
  destinationRow: PByte;
  sourceRow: PByte;
  rowWidth: Word;
  remainingRows: Word;
begin
  destinationRow := PByte(param_3);
  sourceRow := PByte(param_4);
  rowWidth := Word(param_2);
  remainingRows := Word(param_1);
  repeat
    CopyBytesForward(sourceRow, destinationRow, rowWidth);
    Inc(destinationRow, rowWidth);
    Inc(sourceRow, rowWidth);
    Inc(destinationRow, 320 - rowWidth);
    Inc(sourceRow, 320 - rowWidth);
    Dec(remainingRows);
  until remainingRows = 0;
end;
