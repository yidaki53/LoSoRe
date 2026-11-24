{ Oracle: original-byte/Pascal reader-wrapper parity through the checked buffer.
  Host pointers replace far-pointer parameters; they do not prove TP7 ABI.
  The caller-owned four-byte object argument remains for FUN_24dd_38f0. }
procedure FUN_24dd_3988(count: Word; destination, objectPointer: Pointer);
type
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  words: PObjectWords;
  stringLength: Word;
begin
  if (objectPointer = nil) or (destination = nil) or
     (objectPointer <> LieroBufferObject) then
    RunError(211);
  words := objectPointer;
  if words^[1] <> $D7B1 then
    RunError(211);
  RegisterAX := $39AB;
  RegisterCX := count;
  RegisterDI := 1;
  RegisterSI := words^[4];
  LieroBufferDestination := destination;
  FUN_24dd_37ec;
  stringLength := RegisterDI - 1;
  PByte(destination)^ := Byte(stringLength and $FF);
  RegisterAX := stringLength;
end;
