{ Oracle: scoped original-byte/Pascal buffer refill composition.
  Resolved host buffers and service adapter are explicit bindings, not TP7 ABI.
  INCLUDE_ASM residue remains. Checked methods: input375e and output37b3. }
var
  LieroBufferObject, LieroBufferSource, LieroBufferDestination: Pointer;
  LieroBufferDosRead: TLieroDosRead;
  LieroBufferCodeSegment, LieroBufferObjectOffset: Word;
  LieroBufferObjectSegment, LieroBufferSourceOffset,
    LieroBufferSourceSegment: Word;
  LieroBufferDosWrite: TLieroDosWrite;

function LieroInvokeBufferWrite(slotOffset: Word): Word;
begin
  { Oracle: original396c/397a to37b3 composition, explicit far-pointer bindings.
    Other DOS clobbers and native ABI are not represented by these mirrors. }
  if (LieroBufferObject = nil) or (LieroBufferSource = nil) or
     not Assigned(LieroBufferDosWrite) then
    RunError(211);
  if ((slotOffset <> $14) and (slotOffset <> $18)) or
     (LieroBufferObjectSegment = 0) or (LieroBufferCodeSegment = 0) or
     (RegisterES <> LieroBufferObjectSegment) or
     (RegisterBX <> LieroBufferObjectOffset) or
     (PWord(PByte(LieroBufferObject) + slotOffset)^ <> $37B3) or
     (PWord(PByte(LieroBufferObject) + slotOffset + 2)^ <>
       LieroBufferCodeSegment) or
     (PWord(PByte(LieroBufferObject) + 12)^ <> LieroBufferSourceOffset) or
     (PWord(PByte(LieroBufferObject) + 14)^ <> LieroBufferSourceSegment) or
     (PWord(PByte(LieroBufferObject) + 8)^ > 128) then
    RunError(211);
  RegisterBX := PWord(LieroBufferObject)^;
  RegisterDI := LieroBufferObjectOffset;
  LieroInvokeBufferWrite := FUN_24dd_37b3(LieroBufferObject,
                                        LieroBufferSource, LieroBufferDosWrite);
end;

procedure FUN_24dd_396c;
type
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  words: PObjectWords;
begin
  if LieroBufferObject = nil then
    RunError(211);
  words := LieroBufferObject;
  if words^[10] = $37B3 then
    RegisterAX := LieroInvokeBufferWrite($14)
  else begin
    if (LieroBufferSource = nil) or not Assigned(LieroBufferDosRead) or
       (words^[10] <> $375E) or (LieroBufferCodeSegment = 0) or
       (words^[11] <> LieroBufferCodeSegment) or
       (words^[2] > 128) then
      RunError(211);
    RegisterAX := FUN_24dd_375e(LieroBufferObject, LieroBufferSource,
                               LieroBufferDosRead);
  end;
  RegisterZeroFlag := RegisterAX = 0;
  if RegisterAX <> 0 then
    GlobalWord6410 := RegisterAX;
end;
