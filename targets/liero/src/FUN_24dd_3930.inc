{ Oracle: original3930 CRLF source and checked3899/397a composition.
  Longint retains original far-pointer bits, not a native host pointer. }
procedure FUN_24dd_3930(param_1: Longint);
var
  bits, sourceAddress: LongInt;
begin
  bits := param_1;
  RegisterBX := bits and $FFFF;
  RegisterES := (bits shr 16) and $FFFF;
  sourceAddress := LongInt(RegisterDS) * 16 + $6424;
  if (RegisterDS <> LieroTextDataSegment) or
     (sourceAddress + 2 > $100000) or
     (RealModeMemory[sourceAddress] <> 13) or
     (RealModeMemory[sourceAddress + 1] <> 10) then RunError(211);
  RegisterAX := 2;
  RegisterSI := $6424;
  RegisterDX := RegisterDS;
  FUN_24dd_3899;
  if RegisterZeroFlag then begin
    RegisterZeroFlag := PWord(PByte(LieroBufferObject) + 26)^ = 0;
    if not RegisterZeroFlag then FUN_24dd_397a;
  end;
  RegisterSP := (LongInt(RegisterSP) + 8) and $FFFF;
end;
