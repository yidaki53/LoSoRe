{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_24dd_24ba; forward;
{$ENDIF}
procedure FUN_24dd_24ba;
var emuStep: LongInt;
    emuTemp1: LongInt;
    emuTemp2: LongInt;
    emuTemp3: LongInt;
    emuTemp4: LongInt;
    emuTemp5: LongInt;
    emuTemp6: LongInt;
    emuTemp7: LongInt;
    emuTemp8: Boolean;
    emuTemp9: LongInt;
    emuTemp10: LongInt;
    emuTemp11: Boolean;
    emuTemp12: LongInt;
    emuTemp13: LongInt;
    emuTemp14: LongInt;
    emuTemp15: LongInt;
    emuTemp16: Boolean;
    emuTemp17: LongInt;
    emuTemp18: LongInt;
    emuTemp19: Boolean;
begin
  LEmuPush(RegisterAX);
  LEmuPush(RegisterCX);
  RegisterAX := (RegisterAX and $ff00) or ($64 and $ff);
  RegisterCX := (RegisterCX and $ff00) or ($4 and $ff);
  emuTemp1 := RegisterAX;
  RegisterAX := RegisterDX;
  RegisterDX := emuTemp1;
  emuTemp4 := LongInt(RegisterAX);
  emuTemp2 := emuTemp4 div LongInt((RegisterDX and $ff));
  emuTemp3 := emuTemp4 mod LongInt((RegisterDX and $ff));
  RegisterAX := (RegisterAX and $ff00) or (emuTemp2 and $ff);
  RegisterAX := (RegisterAX and $ff) or ((emuTemp3 and $ff) shl 8);
  RegisterCarryFlag := False;
  RegisterZeroFlag := (emuTemp2) = 0;
  RegisterDX := (RegisterDX and $ff00) or ((RegisterAX shr 8) and $ff and $ff);
  RegisterCarryFlag := False;
  emuTemp5 := (RegisterAX and $ff) div 10;
  emuTemp6 := (RegisterAX and $ff) mod 10;
  RegisterAX := (RegisterAX and $ff) or ((emuTemp5 and $ff) shl 8);
  RegisterAX := (RegisterAX and $ff00) or (emuTemp6 and $ff);
  RegisterZeroFlag := (RegisterAX and $ff) = 0;
  emuTemp9 := ((RegisterCX and $ff)) and $1f;
  emuTemp7 := ((RegisterAX shr 8) and $ff) and $ff;
  if emuTemp9 = 0 then begin
    emuTemp8 := RegisterCarryFlag;
  end else if emuTemp9 >= 8 then begin
    emuTemp7 := 0;
    emuTemp8 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp8 := ((emuTemp7) shr (8 - emuTemp9)) and 1 <> 0;
    emuTemp7 := (emuTemp7 shl emuTemp9) and $ff;
    RegisterZeroFlag := (emuTemp7) = 0;
  end;
  RegisterAX := (RegisterAX and $ff) or ((emuTemp7 and $ff) shl 8);
  emuTemp10 := ((RegisterAX shr 8) and $ff) and $ff;
  emuTemp11 := False;
  emuTemp10 := (LongInt(emuTemp10) or LongInt((((RegisterAX and $ff)) and $ff))) and $ff;
  RegisterCarryFlag := emuTemp11;
  RegisterZeroFlag := (emuTemp10) = 0;
  RegisterAX := (RegisterAX and $ff) or ((emuTemp10 and $ff) shl 8);
  emuTemp12 := RegisterAX;
  RegisterAX := RegisterDX;
  RegisterDX := emuTemp12;
  RegisterCarryFlag := False;
  emuTemp13 := (RegisterAX and $ff) div 10;
  emuTemp14 := (RegisterAX and $ff) mod 10;
  RegisterAX := (RegisterAX and $ff) or ((emuTemp13 and $ff) shl 8);
  RegisterAX := (RegisterAX and $ff00) or (emuTemp14 and $ff);
  RegisterZeroFlag := (RegisterAX and $ff) = 0;
  emuTemp17 := ((RegisterCX and $ff)) and $1f;
  emuTemp15 := ((RegisterAX shr 8) and $ff) and $ff;
  if emuTemp17 = 0 then begin
    emuTemp16 := RegisterCarryFlag;
  end else if emuTemp17 >= 8 then begin
    emuTemp15 := 0;
    emuTemp16 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp16 := ((emuTemp15) shr (8 - emuTemp17)) and 1 <> 0;
    emuTemp15 := (emuTemp15 shl emuTemp17) and $ff;
    RegisterZeroFlag := (emuTemp15) = 0;
  end;
  RegisterAX := (RegisterAX and $ff) or ((emuTemp15 and $ff) shl 8);
  emuTemp18 := ((RegisterAX and $ff)) and $ff;
  emuTemp19 := False;
  emuTemp18 := (LongInt(emuTemp18) or LongInt((((RegisterAX shr 8) and $ff) and $ff))) and $ff;
  RegisterCarryFlag := emuTemp19;
  RegisterZeroFlag := (emuTemp18) = 0;
  RegisterAX := (RegisterAX and $ff00) or (emuTemp18 and $ff);
  RegisterAX := (RegisterAX and $ff) or (((RegisterDX shr 8) and $ff and $ff) shl 8);
  emuStep := 1;
  if RegisterDirectionFlag then emuStep := -1;
  begin

      LEmuSetW(RegisterES, (LongInt(RegisterDI) + 0) and $ffff, ((RegisterAX shr 0) and $ffff));
      RegisterDI := (LongInt(RegisterDI) + emuStep * 2) and $ffff;
  end;

  RegisterCX := LEmuPop();
  RegisterAX := LEmuPop();
end;
