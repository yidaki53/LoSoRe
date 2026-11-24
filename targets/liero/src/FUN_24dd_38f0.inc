{ Oracle: original-byte/Pascal skip-wrapper parity through the checked buffer.
  The caller passes the object whose far argument the preceding reader retained.
  Optional method execution uses the explicit method resolver in FUN_24dd_397a. }
procedure FUN_24dd_38f0(objectPointer: Pointer);
type
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  words: PObjectWords;
begin
  if (objectPointer = nil) or (objectPointer <> LieroBufferObject) then
    RunError(211);
  words := objectPointer;
  RegisterAX := $390E;
  RegisterDX := 0;
  RegisterSI := words^[4];
  FUN_24dd_37ec;
  { In this fixture, remaining buffered bytes match the original ZF-clear path. }
  if (words^[4] < words^[5]) and (words^[13] <> 0) then
  begin
    RegisterES := LieroBufferCodeSegment;
    RegisterBX := LieroBufferObjectOffset;
    FUN_24dd_397a;
  end;
end;
