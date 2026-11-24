{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_235c_06d7(param_1: Word; param_2: Word; param_3: Word; param_4: Word); forward;
{$ENDIF}
procedure FUN_235c_06d7(param_1: Word; param_2: Word; param_3: Word; param_4: Word);
label emuL8, emuL13, emuL17;
var emuStep: LongInt;
    emuTemp1: LongInt;
    emuTemp2: Boolean;
    emuTemp3: LongInt;
    emuTemp4: Boolean;
begin
  LEmuPush(RegisterBP);
  RegisterBP := RegisterSP;
  RegisterSP := (RegisterSP - 4) and $ffff;
  RegisterAX := LEmuMemW(RegisterSS, (((RegisterBP) + ($8)) and $ffff));
  RegisterDX := LEmuMemW(RegisterSS, (((RegisterBP) + ($a)) and $ffff));
  emuTemp1 := (RegisterDX) and $ffff;
  emuTemp2 := LongInt(emuTemp1) < LongInt(((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) and $ffff));
  emuTemp1 := (LongInt(emuTemp1) - LongInt(((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp2;
  RegisterZeroFlag := (emuTemp1) = 0;
  RegisterSignFlag := ((emuTemp1) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterDX) xor (LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff)))) and LongInt((RegisterDX) xor (emuTemp1)) and $8000) <> 0;
  if RegisterSignFlag <> RegisterOverflowFlag then goto emuL8;
  if (not RegisterZeroFlag) and (RegisterSignFlag = RegisterOverflowFlag) then goto emuL13;
  emuTemp3 := (RegisterAX) and $ffff;
  emuTemp4 := LongInt(emuTemp3) < LongInt(((LEmuMemW(RegisterSS, (((RegisterBP) + ($4)) and $ffff))) and $ffff));
  emuTemp3 := (LongInt(emuTemp3) - LongInt(((LEmuMemW(RegisterSS, (((RegisterBP) + ($4)) and $ffff))) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp4;
  RegisterZeroFlag := (emuTemp3) = 0;
  RegisterSignFlag := ((emuTemp3) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterAX) xor (LEmuMemW(RegisterSS, (((RegisterBP) + ($4)) and $ffff)))) and LongInt((RegisterAX) xor (emuTemp3)) and $8000) <> 0;
  if not RegisterCarryFlag then goto emuL13;
  emuL8:
  RegisterAX := LEmuMemW(RegisterSS, (((RegisterBP) + ($8)) and $ffff));
  RegisterDX := LEmuMemW(RegisterSS, (((RegisterBP) + ($a)) and $ffff));
  LEmuSetW(RegisterSS, (((RegisterBP) - ($4)) and $ffff), RegisterAX);
  LEmuSetW(RegisterSS, (((RegisterBP) - ($2)) and $ffff), RegisterDX);
  goto emuL17;
  emuL13:
  RegisterAX := LEmuMemW(RegisterSS, (((RegisterBP) + ($4)) and $ffff));
  RegisterDX := LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff));
  LEmuSetW(RegisterSS, (((RegisterBP) - ($4)) and $ffff), RegisterAX);
  LEmuSetW(RegisterSS, (((RegisterBP) - ($2)) and $ffff), RegisterDX);
  emuL17:
  RegisterAX := LEmuMemW(RegisterSS, (((RegisterBP) - ($4)) and $ffff));
  RegisterDX := LEmuMemW(RegisterSS, (((RegisterBP) - ($2)) and $ffff));
  RegisterSP := RegisterBP;
  RegisterBP := LEmuPop();
end;
