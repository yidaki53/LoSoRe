{ Oracle: original3899 buffered output composed with checked37b3 dispatch.
  Explicit segmented-memory bindings, not native TP7 ABI. Original assembly
  retained. Unsupported pointers, wrap and nonprogress abort, never succeed. }
var
  LieroTextDataSegment: Word;

procedure FUN_24dd_3899;
var
  capacity, used, chunk, remaining, objectOffset, objectSegment: Word;
  sourceAddress, bufferAddress, objectAddress, dataAddress, stackAddress,
    codeAddress: LongInt;
begin
  if (LieroTextDataSegment = 0) or (RegisterDS <> LieroTextDataSegment) then
    RunError(211);
  RegisterZeroFlag := GlobalWord6410 = 0;
  if GlobalWord6410 <> 0 then Exit;
  if (LieroBufferObject = nil) or
     (RegisterBX <> LieroBufferObjectOffset) or
     (RegisterES <> LieroBufferObjectSegment) then RunError(211);
  RegisterZeroFlag := PWord(PByte(LieroBufferObject) + 2)^ = $D7B2;
  if not RegisterZeroFlag then begin
    GlobalWord6410 := 105;
    Exit;
  end;
  capacity := PWord(PByte(LieroBufferObject) + 4)^;
  used := PWord(PByte(LieroBufferObject) + 8)^;
  sourceAddress := LongInt(RegisterDX) * 16 + RegisterSI;
  bufferAddress := LongInt(LieroBufferSourceSegment) * 16 +
                   LieroBufferSourceOffset;
  objectAddress := LongInt(LieroBufferObjectSegment) * 16 +
                   LieroBufferObjectOffset;
  dataAddress := LongInt(RegisterDS) * 16 + $6410;
  stackAddress := LongInt(RegisterSS) * 16 + RegisterSP;
  codeAddress := LongInt(LieroBufferCodeSegment) * 16;
  if (capacity = 0) or (capacity > 128) or (used > capacity) or
     (LongInt(RegisterSI) + RegisterAX > $10000) or
     (LongInt(LieroBufferSourceOffset) + capacity > $10000) or
     (sourceAddress + RegisterAX > $100000) or
     (bufferAddress + capacity > $100000) or
     (objectAddress + 28 > $100000) or
     (LieroBufferObject <> @RealModeMemory[objectAddress]) or
     (LieroBufferSource <> @RealModeMemory[bufferAddress]) or
     ((bufferAddress < objectAddress + 28) and
      (bufferAddress + capacity > objectAddress)) or
     ((sourceAddress < bufferAddress + capacity) and
      (sourceAddress + RegisterAX > bufferAddress)) or
     ((sourceAddress < objectAddress + 28) and
      (sourceAddress + RegisterAX > objectAddress)) or
     ((sourceAddress < dataAddress + 2) and
      (sourceAddress + RegisterAX > dataAddress)) or
     ((bufferAddress < dataAddress + $16) and
      (bufferAddress + capacity > dataAddress)) or
     ((objectAddress < dataAddress + $16) and
      (objectAddress + 28 > dataAddress)) or
     (LieroBufferCodeSegment = 0) or
     ((bufferAddress < codeAddress + $6500) and
      (bufferAddress + capacity > codeAddress)) or
     ((objectAddress < codeAddress + $6500) and
      (objectAddress + 28 > codeAddress)) or
     (RegisterSP < 64) or
     ((bufferAddress < stackAddress + 16) and
      (bufferAddress + capacity > stackAddress - 64)) or
     ((objectAddress < stackAddress + 16) and
      (objectAddress + 28 > stackAddress - 64)) or
     ((sourceAddress < stackAddress + 16) and
      (sourceAddress + RegisterAX > stackAddress - 64)) then RunError(211);
  repeat
    used := PWord(PByte(LieroBufferObject) + 8)^;
    if used > capacity then RunError(211);
    chunk := capacity - used;
    remaining := RegisterAX;
    if chunk > remaining then chunk := remaining;
    RegisterAX := remaining - chunk;
    if chunk <> 0 then
      Move(RealModeMemory[sourceAddress], PByte(LieroBufferSource)[used], chunk);
    Inc(sourceAddress, chunk);
    RegisterSI := (LongInt(RegisterSI) + chunk) and $FFFF;
    RegisterCX := 0;
    RegisterDirectionFlag := False;
    Inc(used, chunk);
    RegisterDI := used;
    PWord(PByte(LieroBufferObject) + 8)^ := used;
    if used = capacity then begin
      remaining := RegisterAX;
      objectOffset := RegisterBX;
      objectSegment := RegisterES;
      FUN_24dd_396c;
      RegisterAX := remaining;
      RegisterBX := objectOffset;
      RegisterES := objectSegment;
      if PWord(PByte(LieroBufferObject) + 8)^ <> 0 then RunError(211);
    end;
    { Original continues after a flush error; remaining AX, not sticky error,
      controls this loop. Each checked37b3 call resets used, guaranteeing progress. }
    RegisterZeroFlag := RegisterAX = 0;
  until RegisterZeroFlag;
end;
