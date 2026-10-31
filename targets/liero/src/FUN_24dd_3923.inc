{ Oracle: original-byte/Pascal continuation composition, nonempty contiguous buffer.
  Logical SI is relative to the resolved buffer. INCLUDE_ASM residue remains. }
function FUN_24dd_3923(source: Pointer; var sourceOffset: Word;
                      bufferEnd: Word): Word;
type
  TContinuationBytes = array[0..65535] of Byte;
  PContinuationBytes = ^TContinuationBytes;
var
  character: Byte;
begin
  if (source = nil) or (sourceOffset >= bufferEnd) then
    RunError(211);
  character := PContinuationBytes(source)^[sourceOffset];
  Inc(sourceOffset);
  if character <> 10 then
    Dec(sourceOffset);
  FUN_24dd_3923 := 0;
end;
