{ Oracle: scoped original-byte/Pascal buffer refill composition.
  Resolved host buffers and service adapter are explicit bindings, not TP7 ABI.
  INCLUDE_ASM residue remains. Only the checked input read method is supported. }
var
  LieroBufferObject, LieroBufferSource, LieroBufferDestination: Pointer;
  LieroBufferDosRead: TLieroDosRead;
  LieroBufferCodeSegment, LieroBufferObjectOffset: Word;

procedure FUN_24dd_396c;
type
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  words: PObjectWords;
begin
  if (LieroBufferObject = nil) or (LieroBufferSource = nil) or
     not Assigned(LieroBufferDosRead) then
    RunError(211);
  words := LieroBufferObject;
  if (words^[10] <> $375E) or (LieroBufferCodeSegment = 0) or
     (words^[11] <> LieroBufferCodeSegment) or
     (words^[2] > 128) then
    RunError(211);
  RegisterAX := FUN_24dd_375e(LieroBufferObject, LieroBufferSource,
                             LieroBufferDosRead);
  RegisterZeroFlag := RegisterAX = 0;
  if RegisterAX <> 0 then
    GlobalWord6410 := RegisterAX;
end;
