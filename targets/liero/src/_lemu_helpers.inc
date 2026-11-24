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
procedure LEmuSetFlagBit(maskValue: LongInt; flagValue: Boolean);
begin
  if flagValue then
    RegisterFlagsWord := RegisterFlagsWord or Word(maskValue)
  else
    RegisterFlagsWord := RegisterFlagsWord and Word(maskValue xor $ffff);
end;
procedure LEmuSetCarryFlag(flagValue: Boolean);
begin
  RegisterCarryFlag := flagValue;
  LEmuSetFlagBit($1, flagValue);
end;
procedure LEmuSetParityFlag(flagValue: Boolean);
begin
  RegisterParityFlag := flagValue;
  LEmuSetFlagBit($4, flagValue);
end;
procedure LEmuSetZeroFlag(flagValue: Boolean);
begin
  RegisterZeroFlag := flagValue;
  LEmuSetFlagBit($40, flagValue);
end;
procedure LEmuSetSignFlag(flagValue: Boolean);
begin
  RegisterSignFlag := flagValue;
  LEmuSetFlagBit($80, flagValue);
end;
procedure LEmuSetDirectionFlag(flagValue: Boolean);
begin
  RegisterDirectionFlag := flagValue;
  LEmuSetFlagBit($400, flagValue);
end;
procedure LEmuSetOverflowFlag(flagValue: Boolean);
begin
  RegisterOverflowFlag := flagValue;
  LEmuSetFlagBit($800, flagValue);
end;
procedure LEmuSetResultFlags(valueWord: LongInt; carryValue, overflowValue: Boolean);
var bitIndex: LongInt; parityValue: Boolean;
begin
  RegisterFlagsWord := (RegisterFlagsWord or $2) and $ffc7;
  LEmuSetCarryFlag(carryValue);
  LEmuSetZeroFlag((valueWord and $ffff) = 0);
  LEmuSetSignFlag((valueWord and $8000) <> 0);
  LEmuSetOverflowFlag(overflowValue);
  parityValue := True;
  for bitIndex := 0 to 7 do
    if ((valueWord shr bitIndex) and 1) <> 0 then parityValue := not parityValue;
  LEmuSetParityFlag(parityValue);
end;
procedure LEmuSetFlagsWord(valueWord: Word);
begin
  RegisterFlagsWord := ((valueWord and $0fff) or $7002) and $ffd7;
  RegisterCarryFlag := (valueWord and $1) <> 0;
  RegisterParityFlag := (valueWord and $4) <> 0;
  RegisterZeroFlag := (valueWord and $40) <> 0;
  RegisterSignFlag := (valueWord and $80) <> 0;
  RegisterDirectionFlag := (valueWord and $400) <> 0;
  RegisterOverflowFlag := (valueWord and $800) <> 0;
end;
{$DEFINE LEMU_RUNTIME_HELPERS}
{$ENDIF}
