{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_24dd_4905(param_1: Byte; param_2: Word; param_3: Pointer); forward;
{$ENDIF}
procedure FUN_24dd_4905(param_1: Byte; param_2: Word; param_3: Pointer);
var emuStep: LongInt;
begin
  RegisterBX := RegisterSP;
  RegisterDI := LEmuMemW(RegisterSS, (((RegisterBX) + ($8)) and $ffff));
  RegisterES := LEmuMemW(RegisterSS, ((((RegisterBX) + ($8)) and $ffff) + 2) and $ffff);
  RegisterCX := LEmuMemW(RegisterSS, (((RegisterBX) + ($6)) and $ffff));
  RegisterAX := (RegisterAX and $ff00) or (LEmuMemB(RegisterSS, (((RegisterBX) + ($4)) and $ffff)) and $ff);
  RegisterDirectionFlag := False;
  emuStep := 1;
  if RegisterDirectionFlag then emuStep := -1;
  while RegisterCX <> 0 do
  begin

      LEmuSetB(RegisterES, RegisterDI, (RegisterAX and $ff));
      RegisterDI := (LongInt(RegisterDI) + emuStep * 1) and $ffff;
      Dec(RegisterCX);
  end;

end;
