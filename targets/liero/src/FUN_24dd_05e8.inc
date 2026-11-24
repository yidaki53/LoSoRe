{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_24dd_05e8; forward;
{$ENDIF}
procedure FUN_24dd_05e8;
var emuStep: LongInt;
    emuTemp1: LongInt;
    emuTemp2: LongInt;
    emuTemp3: Boolean;
    emuTemp4: LongInt;
begin
  RegisterAX := $5dc;
  LEmuPush(RegisterDS);
  RegisterCX := $191;
  RegisterDS := RegisterCX;
  emuTemp1 := RegisterAX;
  RegisterAX := RegisterSI;
  RegisterSI := emuTemp1;
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

  emuTemp2 := (RegisterDI) and $ffff;
  emuTemp3 := LongInt(emuTemp2) < LongInt((($c) and $ffff));
  emuTemp2 := (LongInt(emuTemp2) - LongInt((($c) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp3;
  RegisterZeroFlag := (emuTemp2) = 0;
  RegisterSignFlag := ((emuTemp2) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterDI) xor ($c)) and LongInt((RegisterDI) xor (emuTemp2)) and $8000) <> 0;
  RegisterDI := emuTemp2;
  emuTemp4 := RegisterAX;
  RegisterAX := RegisterSI;
  RegisterSI := emuTemp4;
  RegisterDS := LEmuPop();
end;
