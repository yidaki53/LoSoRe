{$IFNDEF LEMU_GENERATED_FORWARDS}
procedure FUN_235c_0aeb; forward;
{$ENDIF}
{$IFNDEF LEMU_RUNTIME_HELPERS}
function LEmuMemB(segmentWord, offsetWord: Word): Byte; forward;
function LEmuMemW(segmentWord, offsetWord: Word): Word; forward;
procedure LEmuSetB(segmentWord, offsetWord: Word; value: Byte); forward;
procedure LEmuSetW(segmentWord, offsetWord: Word; value: Word); forward;
procedure LEmuPush(value: Word); forward;
function LEmuPop: Word; forward;
function LEmuSigned16(valueWord: Word): LongInt; forward;
{$ENDIF}
procedure FUN_235c_0aeb;
var emuStep: LongInt;
begin
  LEmuPush(RegisterBP);
  RegisterBP := RegisterSP;
  RegisterDI := $6a58;
  LEmuPush(RegisterDS);
  LEmuPush(RegisterDI);
  LEmuPush($400);
  LEmuPush($0);
  RegisterSP := (RegisterSP - 4) and $ffff;
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

  RegisterSP := (RegisterSP + 4) and $ffff;
  RegisterSP := RegisterBP;
  RegisterBP := LEmuPop();
end;
{$IFNDEF LEMU_RUNTIME_HELPERS}
function LEmuMemB(segmentWord, offsetWord: Word): Byte;
begin
  LEmuMemB := RealModeMemory[((LongInt(segmentWord) shl 4) + offsetWord) and $fffff];
end;
function LEmuMemW(segmentWord, offsetWord: Word): Word;
var address: LongInt;
begin
  address := ((LongInt(segmentWord) shl 4) + offsetWord) and $fffff;
  LEmuMemW := RealModeMemory[address] or (RealModeMemory[address + 1] shl 8);
end;
procedure LEmuSetB(segmentWord, offsetWord: Word; value: Byte);
begin
  RealModeMemory[((LongInt(segmentWord) shl 4) + offsetWord) and $fffff] := value;
end;
procedure LEmuSetW(segmentWord, offsetWord: Word; value: Word);
var address: LongInt;
begin
  address := ((LongInt(segmentWord) shl 4) + offsetWord) and $fffff;
  RealModeMemory[address] := value and $ff;
  RealModeMemory[address + 1] := (value shr 8) and $ff;
end;
procedure LEmuPush(value: Word);
begin
  RegisterSP := (RegisterSP - 2) and $ffff;
  LEmuSetW(RegisterSS, RegisterSP, value);
end;
function LEmuPop: Word;
begin
  LEmuPop := LEmuMemW(RegisterSS, RegisterSP);
  RegisterSP := (RegisterSP + 2) and $ffff;
end;
function LEmuSigned16(valueWord: Word): LongInt;
var signedValue: LongInt;
begin
  signedValue := LongInt(valueWord);
  if (valueWord and $8000) <> 0 then signedValue := signedValue - $10000;
  LEmuSigned16 := signedValue;
end;
{$DEFINE LEMU_RUNTIME_HELPERS}
{$ENDIF}
