var
  emuAbsState0: LongInt;
  emuAbsState0Mirror: LongInt;
  emuAbsState1: LongInt;
  emuAbsState1Mirror: LongInt;
procedure FUN_24dd_46b1;
var emuStep: LongInt;
    emuAdcZeroCarry: Boolean;
    emuAdcZeroResult: LongInt;
    emuTemp1: Int64;
    emuTemp2: LongInt;
    emuTemp3: Boolean;
    emuTemp4: LongInt;
    emuTemp5: LongInt;
    emuTemp6: Boolean;
    emuTemp7: LongInt;
    emuTemp8: LongInt;
    emuTemp9: Boolean;
    emuTemp10: LongInt;
    emuTemp11: LongInt;
    emuTemp12: Boolean;
    emuTemp13: LongInt;
    emuTemp14: Boolean;
    emuTemp15: LongInt;
    emuTemp16: Boolean;
    emuTemp17: LongInt;
    emuTemp18: Boolean;
    emuTemp19: LongInt;
    emuTemp20: LongInt;
    emuTemp21: Boolean;
    emuTemp22: LongInt;
    emuTemp23: LongInt;
    emuTemp24: Boolean;
    emuTemp25: LongInt;
    emuTemp26: Boolean;
    emuTemp27: LongInt;
    emuTemp28: Boolean;
    emuTemp29: LongInt;
    emuTemp30: LongInt;
    emuTemp31: Boolean;
    emuTemp32: LongInt;
    emuTemp33: Boolean;
begin
  if (Word(DosMemory[$6412]) or (Word(DosMemory[$6413]) shl 8)) <> emuAbsState0Mirror then begin
    emuAbsState0 := (Word(DosMemory[$6412]) or (Word(DosMemory[$6413]) shl 8));
    emuAbsState0Mirror := (Word(DosMemory[$6412]) or (Word(DosMemory[$6413]) shl 8));
  end;
  RegisterAX := emuAbsState0;
  if (Word(DosMemory[$6414]) or (Word(DosMemory[$6415]) shl 8)) <> emuAbsState1Mirror then begin
    emuAbsState1 := (Word(DosMemory[$6414]) or (Word(DosMemory[$6415]) shl 8));
    emuAbsState1Mirror := (Word(DosMemory[$6414]) or (Word(DosMemory[$6415]) shl 8));
  end;
  RegisterBX := emuAbsState1;
  RegisterCX := RegisterAX;
  emuTemp1 := Int64(RegisterAX) * Int64((Word(CodeMemory[$46e7]) or (Word(CodeMemory[$46e8]) shl 8)));
  RegisterAX := Word(emuTemp1 and $ffff);
  RegisterDX := Word((emuTemp1 shr 16) and $ffff);
  RegisterCarryFlag := RegisterDX <> 0;
  RegisterZeroFlag := RegisterAX = 0;
  RegisterSignFlag := (RegisterAX and $8000) <> 0;
  RegisterOverflowFlag := False;
  emuTemp4 := ($1) and $1f;
  emuTemp2 := (RegisterCX) and $ffff;
  if emuTemp4 = 0 then begin
    emuTemp3 := RegisterCarryFlag;
  end else if emuTemp4 >= 16 then begin
    emuTemp2 := 0;
    emuTemp3 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp3 := ((emuTemp2) shr (16 - emuTemp4)) and 1 <> 0;
    emuTemp2 := (emuTemp2 shl emuTemp4) and $ffff;
    RegisterZeroFlag := (emuTemp2) = 0;
  end;
  RegisterSignFlag := ((emuTemp2) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterCX := emuTemp2;
  emuTemp7 := ($1) and $1f;
  emuTemp5 := (RegisterCX) and $ffff;
  if emuTemp7 = 0 then begin
    emuTemp6 := RegisterCarryFlag;
  end else if emuTemp7 >= 16 then begin
    emuTemp5 := 0;
    emuTemp6 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp6 := ((emuTemp5) shr (16 - emuTemp7)) and 1 <> 0;
    emuTemp5 := (emuTemp5 shl emuTemp7) and $ffff;
    RegisterZeroFlag := (emuTemp5) = 0;
  end;
  RegisterSignFlag := ((emuTemp5) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterCX := emuTemp5;
  emuTemp10 := ($1) and $1f;
  emuTemp8 := (RegisterCX) and $ffff;
  if emuTemp10 = 0 then begin
    emuTemp9 := RegisterCarryFlag;
  end else if emuTemp10 >= 16 then begin
    emuTemp8 := 0;
    emuTemp9 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp9 := ((emuTemp8) shr (16 - emuTemp10)) and 1 <> 0;
    emuTemp8 := (emuTemp8 shl emuTemp10) and $ffff;
    RegisterZeroFlag := (emuTemp8) = 0;
  end;
  RegisterSignFlag := ((emuTemp8) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterCX := emuTemp8;
  emuTemp11 := ((RegisterCX shr 8) and $ff) and $ff;
  emuTemp12 := LongInt(emuTemp11) + LongInt((((RegisterCX and $ff)) and $ff)) > $ff;
  emuTemp11 := (LongInt(emuTemp11) + LongInt((((RegisterCX and $ff)) and $ff))) and $ff;
  RegisterCarryFlag := emuTemp12;
  RegisterZeroFlag := (emuTemp11) = 0;
  RegisterSignFlag := ((emuTemp11) and $80) <> 0;
  RegisterOverflowFlag := (LongInt(((RegisterCX shr 8) and $ff) xor (emuTemp11)) and LongInt(((RegisterCX and $ff)) xor (emuTemp11)) and $80) <> 0;
  RegisterCX := (RegisterCX and $ff) or ((emuTemp11 and $ff) shl 8);
  emuTemp13 := (RegisterDX) and $ffff;
  emuTemp14 := LongInt(emuTemp13) + LongInt(((RegisterCX) and $ffff)) > $ffff;
  emuTemp13 := (LongInt(emuTemp13) + LongInt(((RegisterCX) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp14;
  RegisterZeroFlag := (emuTemp13) = 0;
  RegisterSignFlag := ((emuTemp13) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterDX) xor (emuTemp13)) and LongInt((RegisterCX) xor (emuTemp13)) and $8000) <> 0;
  RegisterDX := emuTemp13;
  emuTemp15 := (RegisterDX) and $ffff;
  emuTemp16 := LongInt(emuTemp15) + LongInt(((RegisterBX) and $ffff)) > $ffff;
  emuTemp15 := (LongInt(emuTemp15) + LongInt(((RegisterBX) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp16;
  RegisterZeroFlag := (emuTemp15) = 0;
  RegisterSignFlag := ((emuTemp15) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterDX) xor (emuTemp15)) and LongInt((RegisterBX) xor (emuTemp15)) and $8000) <> 0;
  RegisterDX := emuTemp15;
  emuTemp19 := ($1) and $1f;
  emuTemp17 := (RegisterBX) and $ffff;
  if emuTemp19 = 0 then begin
    emuTemp18 := RegisterCarryFlag;
  end else if emuTemp19 >= 16 then begin
    emuTemp17 := 0;
    emuTemp18 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp18 := ((emuTemp17) shr (16 - emuTemp19)) and 1 <> 0;
    emuTemp17 := (emuTemp17 shl emuTemp19) and $ffff;
    RegisterZeroFlag := (emuTemp17) = 0;
  end;
  RegisterSignFlag := ((emuTemp17) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterBX := emuTemp17;
  emuTemp22 := ($1) and $1f;
  emuTemp20 := (RegisterBX) and $ffff;
  if emuTemp22 = 0 then begin
    emuTemp21 := RegisterCarryFlag;
  end else if emuTemp22 >= 16 then begin
    emuTemp20 := 0;
    emuTemp21 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp21 := ((emuTemp20) shr (16 - emuTemp22)) and 1 <> 0;
    emuTemp20 := (emuTemp20 shl emuTemp22) and $ffff;
    RegisterZeroFlag := (emuTemp20) = 0;
  end;
  RegisterSignFlag := ((emuTemp20) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterBX := emuTemp20;
  emuTemp23 := (RegisterDX) and $ffff;
  emuTemp24 := LongInt(emuTemp23) + LongInt(((RegisterBX) and $ffff)) > $ffff;
  emuTemp23 := (LongInt(emuTemp23) + LongInt(((RegisterBX) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp24;
  RegisterZeroFlag := (emuTemp23) = 0;
  RegisterSignFlag := ((emuTemp23) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterDX) xor (emuTemp23)) and LongInt((RegisterBX) xor (emuTemp23)) and $8000) <> 0;
  RegisterDX := emuTemp23;
  emuTemp25 := ((RegisterDX shr 8) and $ff) and $ff;
  emuTemp26 := LongInt(emuTemp25) + LongInt((((RegisterBX and $ff)) and $ff)) > $ff;
  emuTemp25 := (LongInt(emuTemp25) + LongInt((((RegisterBX and $ff)) and $ff))) and $ff;
  RegisterCarryFlag := emuTemp26;
  RegisterZeroFlag := (emuTemp25) = 0;
  RegisterSignFlag := ((emuTemp25) and $80) <> 0;
  RegisterOverflowFlag := (LongInt(((RegisterDX shr 8) and $ff) xor (emuTemp25)) and LongInt(((RegisterBX and $ff)) xor (emuTemp25)) and $80) <> 0;
  RegisterDX := (RegisterDX and $ff) or ((emuTemp25 and $ff) shl 8);
  RegisterCX := (RegisterCX and $ff00) or ($5 and $ff);
  emuTemp29 := ((RegisterCX and $ff)) and $1f;
  emuTemp27 := (RegisterBX) and $ffff;
  if emuTemp29 = 0 then begin
    emuTemp28 := RegisterCarryFlag;
  end else if emuTemp29 >= 16 then begin
    emuTemp27 := 0;
    emuTemp28 := False;
    RegisterZeroFlag := True;
  end else begin
    emuTemp28 := ((emuTemp27) shr (16 - emuTemp29)) and 1 <> 0;
    emuTemp27 := (emuTemp27 shl emuTemp29) and $ffff;
    RegisterZeroFlag := (emuTemp27) = 0;
  end;
  RegisterSignFlag := ((emuTemp27) and $8000) <> 0;
  RegisterOverflowFlag := False;
  RegisterBX := emuTemp27;
  emuTemp30 := ((RegisterDX shr 8) and $ff) and $ff;
  emuTemp31 := LongInt(emuTemp30) + LongInt((((RegisterBX and $ff)) and $ff)) > $ff;
  emuTemp30 := (LongInt(emuTemp30) + LongInt((((RegisterBX and $ff)) and $ff))) and $ff;
  RegisterCarryFlag := emuTemp31;
  RegisterZeroFlag := (emuTemp30) = 0;
  RegisterSignFlag := ((emuTemp30) and $80) <> 0;
  RegisterOverflowFlag := (LongInt(((RegisterDX shr 8) and $ff) xor (emuTemp30)) and LongInt(((RegisterBX and $ff)) xor (emuTemp30)) and $80) <> 0;
  RegisterDX := (RegisterDX and $ff) or ((emuTemp30 and $ff) shl 8);
  emuTemp32 := (RegisterAX) and $ffff;
  emuTemp33 := LongInt(emuTemp32) + LongInt((($1) and $ffff)) > $ffff;
  emuTemp32 := (LongInt(emuTemp32) + LongInt((($1) and $ffff))) and $ffff;
  RegisterCarryFlag := emuTemp33;
  RegisterZeroFlag := (emuTemp32) = 0;
  RegisterSignFlag := ((emuTemp32) and $8000) <> 0;
  RegisterOverflowFlag := (LongInt((RegisterAX) xor (emuTemp32)) and LongInt(($1) xor (emuTemp32)) and $8000) <> 0;
  RegisterAX := emuTemp32;
  emuAdcZeroCarry := LongInt(RegisterDX) + LongInt(RegisterCarryFlag) > $ffff;
  emuAdcZeroResult := (LongInt(RegisterDX) + LongInt(RegisterCarryFlag)) and $ffff;
  RegisterDX := emuAdcZeroResult;
  RegisterCarryFlag := emuAdcZeroCarry;
  RegisterSignFlag := ((emuAdcZeroResult) and $8000) <> 0;
  RegisterOverflowFlag := False;
  emuAbsState0 := RegisterAX;
  emuAbsState0Mirror := RegisterAX;
  DosMemory[$6412] := Byte(RegisterAX);
  DosMemory[$6413] := Byte((RegisterAX shr 8) and $ff);
  emuAbsState1 := RegisterDX;
  emuAbsState1Mirror := RegisterDX;
  DosMemory[$6414] := Byte(RegisterDX);
  DosMemory[$6415] := Byte((RegisterDX shr 8) and $ff);
end;
