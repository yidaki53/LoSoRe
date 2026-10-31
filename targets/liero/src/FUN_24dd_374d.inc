{ Oracle: isolated original-vs-host Pascal dispatch composition.
  The callback resolves a far method and object explicitly; it is not TP7 ABI.
  Unknown methods must be rejected by the resolver, never treated as success. }
type
  TLieroDispatchMethod = function(slotOffset, objectSegment, objectOffset: Word): Word;
var
  LieroDispatchMethod: TLieroDispatchMethod;

procedure FUN_24dd_374d;
var
  savedSegment, savedOffset: Word;
begin
  if not Assigned(LieroDispatchMethod) then
    RunError(211);
  savedSegment := RegisterES;
  savedOffset := RegisterDI;
  RegisterAX := LieroDispatchMethod(RegisterBX, savedSegment, savedOffset);
  RegisterZeroFlag := RegisterAX = 0;
  if RegisterAX <> 0 then
    GlobalWord6410 := RegisterAX;
  RegisterDI := savedOffset;
  RegisterES := savedSegment;
end;
