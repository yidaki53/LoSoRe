{ Oracle: scoped original-byte/Pascal callback parity, nonempty contiguous buffer.
  Logical SI/DI are offsets in supplied buffers; not a TP7 ABI translation.
  INCLUDE_ASM residue remains. A zero count wraps on the first ordinary byte. }
function FUN_24dd_39ab(source, destination: Pointer;
                      var sourceOffset, destinationOffset, count: Word;
                      bufferEnd: Word): Word;
type
  TCallbackBytes = array[0..65535] of Byte;
  PCallbackBytes = ^TCallbackBytes;
var
  character: Byte;
begin
  if (source = nil) or (destination = nil) or
     (sourceOffset >= bufferEnd) then
    RunError(211);
  repeat
    character := PCallbackBytes(source)^[sourceOffset];
    Inc(sourceOffset);
    if (character = 13) or (character = 26) then
      Break;
    PCallbackBytes(destination)^[destinationOffset] := character;
    Inc(destinationOffset);
    if count = 0 then
      count := $FFFF
    else
      Dec(count);
    if count = 0 then
    begin
      FUN_24dd_39ab := 0;
      Exit;
    end;
    if sourceOffset = bufferEnd then
    begin
      FUN_24dd_39ab := $39AB;
      Exit;
    end;
  until False;
  Dec(sourceOffset);
  FUN_24dd_39ab := 0;
end;
