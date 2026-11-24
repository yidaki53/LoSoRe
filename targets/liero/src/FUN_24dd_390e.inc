{ Oracle: scoped original-byte/Pascal skip callback parity.
  Nonempty contiguous buffer, logical SI offset; INCLUDE_ASM residue remains.
  3923 is a continuation token, not a call to an invented host routine. }
function FUN_24dd_390e(source: Pointer; var sourceOffset: Word;
                      bufferEnd: Word): Word;
type
  TSkipBytes = array[0..65535] of Byte;
  PSkipBytes = ^TSkipBytes;
var
  character: Byte;
begin
  if (source = nil) or (sourceOffset >= bufferEnd) then
    RunError(211);
  repeat
    character := PSkipBytes(source)^[sourceOffset];
    Inc(sourceOffset);
    if character = 26 then
    begin
      Dec(sourceOffset);
      FUN_24dd_390e := 0;
      Exit;
    end;
    if character = 13 then
    begin
      if sourceOffset = bufferEnd then
      begin
        FUN_24dd_390e := $3923;
        Exit;
      end;
      character := PSkipBytes(source)^[sourceOffset];
      Inc(sourceOffset);
      if character <> 10 then
        Dec(sourceOffset);
      FUN_24dd_390e := 0;
      Exit;
    end;
  until sourceOffset = bufferEnd;
  FUN_24dd_390e := $390E;
end;
