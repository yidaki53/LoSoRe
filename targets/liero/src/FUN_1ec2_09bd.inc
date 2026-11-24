{$IFNDEF LEMU_GENERATED_FORWARDS}
function FUN_1ec2_09bd(param_1: Word; param_2: Integer): Word; forward;
{$ENDIF}
function FUN_1ec2_09bd(param_1: Word; param_2: Integer): Word;
label emuL5, emuL9, emuL11;
var emuStep: LongInt;
    emuTemp1: LongInt;
    emuTemp2: Boolean;
    emuTemp3: LongInt;
    emuTemp4: Boolean;
    emuTemp5: LongInt;
    emuTemp6: Boolean;
begin
  RegisterAX := Word(param_1);
  RegisterBX := Word(param_2);
  LEmuSetW(RegisterSS, ((RegisterSP + 2) and $ffff), Word(param_1));
  LEmuSetW(RegisterSS, ((RegisterSP + 4) and $ffff), Word(param_2));
  LEmuPush(RegisterBP);
  RegisterBP := RegisterSP;
  RegisterSP := (RegisterSP - 2) and $ffff;
  emuTemp1 := (LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) and $ffff;
  emuTemp2 := LongInt(emuTemp1) < LongInt((($0) and $ffff));
  emuTemp1 := (LongInt(emuTemp1) - LongInt((($0) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp2;
  RegisterZeroFlag := (emuTemp1) = 0;
  RegisterSignFlag := ((emuTemp1) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) xor ($0)) and LongInt((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) xor (emuTemp1)) and $8000) <> 0;
  if RegisterSignFlag = RegisterOverflowFlag then goto emuL5;
  LEmuSetW(RegisterSS, (((RegisterBP) - ($2)) and $ffff), $ffff);
  goto emuL11;
  emuL5:
  emuTemp3 := (LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) and $ffff;
  emuTemp4 := LongInt(emuTemp3) < LongInt((($0) and $ffff));
  emuTemp3 := (LongInt(emuTemp3) - LongInt((($0) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp4;
  RegisterZeroFlag := (emuTemp3) = 0;
  RegisterSignFlag := ((emuTemp3) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) xor ($0)) and LongInt((LEmuMemW(RegisterSS, (((RegisterBP) + ($6)) and $ffff))) xor (emuTemp3)) and $8000) <> 0;
  if RegisterZeroFlag or (RegisterSignFlag <> RegisterOverflowFlag) then goto emuL9;
  LEmuSetW(RegisterSS, (((RegisterBP) - ($2)) and $ffff), $1);
  goto emuL11;
  emuL9:
  emuTemp5 := (RegisterAX) and $ffff;
  emuTemp6 := False;
  emuTemp5 := (LongInt(emuTemp5) xor LongInt(((RegisterAX) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp6;
  RegisterZeroFlag := (emuTemp5) = 0;
  RegisterSignFlag := ((emuTemp5) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterAX := emuTemp5;
  LEmuSetW(RegisterSS, (((RegisterBP) - ($2)) and $ffff), RegisterAX);
  emuL11:
  RegisterAX := LEmuMemW(RegisterSS, (((RegisterBP) - ($2)) and $ffff));
  RegisterSP := RegisterBP;
  RegisterBP := LEmuPop();
  FUN_1ec2_09bd := RegisterAX;
end;
