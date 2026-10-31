{ Oracle: scoped original-byte/Pascal input buffer dispatcher composition.
  Logical SI/DI are buffer-relative offsets; resolved bindings come from 396C.
  Supported callbacks are 39AB/390E/3923; unknown callbacks abort explicitly.
  INCLUDE_ASM residue remains; register mirrors are not TP7 code generation. }
procedure FUN_24dd_37ec;
type
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  words: PObjectWords;
  savedCallback, savedCount, savedDestination: Word;
begin
  RegisterZeroFlag := GlobalWord6410 = 0;
  if GlobalWord6410 <> 0 then
    Exit;
  if LieroBufferObject = nil then
    RunError(211);
  words := LieroBufferObject;
  RegisterZeroFlag := words^[1] = $D7B1;
  if not RegisterZeroFlag then
  begin
    GlobalWord6410 := $68;
    Exit;
  end;
  repeat
    RegisterSI := words^[4];
    if (RegisterSI > words^[5]) or (words^[5] > 128) then
      RunError(211);
    if RegisterSI <> words^[5] then
    begin
      case RegisterAX of
        $39AB:
          RegisterAX := FUN_24dd_39ab(LieroBufferSource, LieroBufferDestination,
                                     RegisterSI, RegisterDI, RegisterCX, words^[5]);
        $390E:
          RegisterAX := FUN_24dd_390e(LieroBufferSource, RegisterSI, words^[5]);
        $3923:
          RegisterAX := FUN_24dd_3923(LieroBufferSource, RegisterSI, words^[5]);
      else
        RunError(211);
      end;
      RegisterDirectionFlag := False;
      words^[4] := RegisterSI;
      RegisterZeroFlag := RegisterAX = 0;
      if RegisterZeroFlag then
        Exit;
    end;
    savedCallback := RegisterAX;
    savedCount := RegisterCX;
    savedDestination := RegisterDI;
    FUN_24dd_396c;
    RegisterAX := savedCallback;
    RegisterCX := savedCount;
    RegisterDI := savedDestination;
    RegisterSI := words^[4];
    RegisterZeroFlag := RegisterSI = words^[5];
  until RegisterZeroFlag;
end;
