{ Oracle: original010f terminating error path with empty descriptor/callback
  chains and closed or checked default input/output objects. External vector restoration and
  process termination are explicit ports, never returning success fallbacks.
  Other cleanup targets and native ABI remain unresolved.
  Original assembly retained. }
procedure FUN_24dd_010f;
var
  dataAddress, stackAddress: LongInt;
  errorCode, callerOffset, callerSegment, index, vectorOffset,
    vectorSegment: Word;
  procedure CheckObject(offset: Word; openMode: Word);
  var
    address: LongInt;
    mode: Word;
  begin
    address := dataAddress + offset;
    mode := PWord(@RealModeMemory[address + 2])^;
    if mode = $D7B0 then Exit;
    if (mode <> openMode) or not Assigned(LieroDispatchMethod) or
       (PWord(@RealModeMemory[address + 28])^ <> $37D3) or
       (PWord(@RealModeMemory[address + 30])^ <> LieroErrorCodeSegment) then
      RunError(211);
    if mode = $D7B2 then
      if (PWord(@RealModeMemory[address + 20])^ <> $37B3) or
         (PWord(@RealModeMemory[address + 22])^ <> LieroErrorCodeSegment) or
         (PWord(@RealModeMemory[address + 4])^ <> 128) or
         (PWord(@RealModeMemory[address + 8])^ > 128) or
         (PWord(@RealModeMemory[address + 12])^ <> offset + 128) or
         (PWord(@RealModeMemory[address + 14])^ <> LieroErrorDataSegment) then
        RunError(211);
  end;
begin
  if (LieroErrorDataSegment = 0) or (LieroErrorCodeSegment = 0) or
     not Assigned(LieroRestoreVector) or not Assigned(LieroTerminate) or
     (RegisterSP > $FFFA) then RunError(211);
  dataAddress := LongInt(LieroErrorDataSegment) * 16;
  stackAddress := LongInt(RegisterSS) * 16 + RegisterSP;
  if (dataAddress + $7B3C > $A0000) or
     (stackAddress + 4 > $100000) or
     ((stackAddress < dataAddress + $7B3C) and
      (stackAddress + 4 > dataAddress + $63D8)) or
     (PWord(@RealModeMemory[dataAddress + $63E4])^ <> 0) or
     (PWord(@RealModeMemory[dataAddress + $6402])^ <> 0) or
     (PWord(@RealModeMemory[dataAddress + $6404])^ <> 0) then
    RunError(211);
  CheckObject($78F0, $D7B1);
  CheckObject($79F0, $D7B2);
  errorCode := RegisterAX;
  callerOffset := PWord(@RealModeMemory[stackAddress])^;
  callerSegment := PWord(@RealModeMemory[stackAddress + 2])^;
  RegisterSP := RegisterSP + 4;
  RegisterDS := LieroErrorDataSegment;
  WriteWordLE(@RealModeMemory[dataAddress], $6406, errorCode);
  if (callerOffset <> 0) or (callerSegment <> 0) then
    callerSegment := (LongInt(callerSegment) -
      PWord(@RealModeMemory[dataAddress + $640C])^ - 16) and $FFFF;
  WriteWordLE(@RealModeMemory[dataAddress], $6408, callerOffset);
  WriteWordLE(@RealModeMemory[dataAddress], $640A, callerSegment);
  RegisterES := LieroErrorDataSegment;
  RegisterDI := $78F0;
  FUN_24dd_3711(@RealModeMemory[dataAddress + $78F0]);
  RegisterES := LieroErrorDataSegment;
  RegisterDI := $79F0;
  FUN_24dd_3711(@RealModeMemory[dataAddress + $79F0]);
  for index := 0 to 18 do begin
    vectorOffset := PWord(@RealModeMemory[dataAddress + $7AF0 + index * 4])^;
    vectorSegment := PWord(@RealModeMemory[dataAddress + $7AF2 + index * 4])^;
    LieroRestoreVector(CodeMemory[$239 + index], vectorOffset, vectorSegment);
  end;
  if (callerOffset <> 0) or (callerSegment <> 0) then begin
    RegisterBX := $24C;
    FUN_24dd_01f0;
    RegisterAX := errorCode;
    RegisterAX := FUN_24dd_01fe;
    RegisterBX := $25B;
    FUN_24dd_01f0;
    RegisterAX := callerSegment;
    FUN_24dd_0218;
    FUN_24dd_0232(Ord(':'));
    RegisterAX := callerOffset;
    FUN_24dd_0218;
    RegisterBX := $260;
    FUN_24dd_01f0;
  end;
  RegisterAX := $4C00 or (errorCode and $FF);
  LieroTerminate(errorCode and $FF);
  RunError(211);
end;
