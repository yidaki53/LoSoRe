{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_24dd_0628; forward;
{$ENDIF}
procedure FUN_24dd_0628;
var emuStep: LongInt;
    emuTemp1: LongInt;
    emuTemp2: Boolean;
begin
  LEmuPush(RegisterSI);
  LEmuPush(RegisterDI);
  RegisterDI := LEmuMemW(RegisterDS, (((($d8)) and $ffff) and $0fff));
  emuTemp1 := (RegisterDI) and $ffff;
  emuTemp2 := LongInt(emuTemp1) < LongInt((($c) and $ffff));
  emuTemp1 := (LongInt(emuTemp1) - LongInt((($c) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp2;
  RegisterZeroFlag := (emuTemp1) = 0;
  RegisterDI := emuTemp1;
  LEmuSetW(RegisterDS, (((($d8)) and $ffff) and $0fff), RegisterDI);
  LEmuPush(RegisterES);
  LEmuPush(RegisterDS);
  RegisterES := LEmuPop();
  RegisterDirectionFlag := False;
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
