{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_24dd_0673; forward;
{$ENDIF}
procedure FUN_24dd_0673;
var emuStep: LongInt;
begin
  LEmuPush(RegisterSI);
  LEmuPush(RegisterDI);
  RegisterSI := LEmuMemW(RegisterDS, (((($d8)) and $ffff) and $0fff));
  RegisterDI := (((RegisterSI) - ($c)) and $ffff);
  LEmuSetW(RegisterDS, (((($d8)) and $ffff) and $0fff), RegisterDI);
  RegisterDirectionFlag := False;
  LEmuPush(RegisterES);
  LEmuPush(RegisterDS);
  RegisterES := LEmuPop();
  RegisterCX := $6;
  emuStep := 1;
  if RegisterDirectionFlag then emuStep := -1;
  while RegisterCX <> 0 do
  begin

      LEmuSetW(RegisterES, (LongInt(RegisterDI) + 0) and $ffff, LEmuMemW(RegisterDS, (LongInt(RegisterSI) + 0) and $ffff));
      RegisterSI := (LongInt(RegisterSI) + emuStep * 2) and $ffff;
      RegisterDI := (LongInt(RegisterDI) + emuStep * 2) and $ffff;
      Dec(RegisterCX);
  end;

  RegisterES := LEmuPop();
  RegisterDI := LEmuPop();
  RegisterSI := LEmuPop();
end;
