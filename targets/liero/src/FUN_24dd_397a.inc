{ Oracle: isolated optional-method invocation, object identity and sticky AX error.
  The host resolver must validate the exact slot and original logical far pointer. }
procedure FUN_24dd_397a;
var
  savedSegment, savedObjectOffset, returned: Word;
begin
  if not Assigned(LieroDispatchMethod) then
    RunError(211);
  if (RegisterBX <> LieroBufferObjectOffset) or
     (RegisterES <> LieroBufferCodeSegment) then
    RunError(211);
  if (PWord(PByte(LieroBufferObject) + 24)^ <> $0400) or
     (PWord(PByte(LieroBufferObject) + 26)^ <> RegisterES) then
    RunError(211);
  savedSegment := RegisterES;
  savedObjectOffset := RegisterBX;
  returned := LieroDispatchMethod($18, savedSegment, savedObjectOffset);
  RegisterAX := returned;
  if returned <> 0 then
    GlobalWord6410 := returned;
  RegisterBX := savedObjectOffset;
  RegisterES := savedSegment;
end;
