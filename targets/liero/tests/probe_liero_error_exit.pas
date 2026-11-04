program ErrorExitProbe;
uses LieroRuntime;
procedure FUN_24dd_0232(param_1: Word); forward;
procedure FUN_24dd_022a; forward;
procedure FUN_24dd_021f; forward;
{$I FUN_24dd_0232.inc}
{$I FUN_24dd_020a.inc}
{$I FUN_24dd_01fe.inc}
{$I FUN_24dd_022a.inc}
{$I FUN_24dd_021f.inc}
{$I FUN_24dd_0218.inc}
{$I FUN_24dd_01f0.inc}
{$I FUN_24dd_374d.inc}
{$I FUN_24dd_37b3.inc}
{$I FUN_24dd_37d3.inc}
procedure FUN_24dd_396c; forward;
procedure FUN_24dd_397a; forward;
{$I FUN_24dd_375e.inc}
{$I FUN_24dd_396c.inc}
{$I FUN_24dd_397a.inc}
{$I FUN_24dd_3899.inc}
{$I FUN_24dd_3930.inc}
{$I FUN_24dd_3711.inc}
{$I FUN_24dd_010f.inc}
{$I FUN_24dd_04f4.inc}
{$I FUN_249c_0013.inc}
{$I FUN_249c_0000.inc}
{$I FUN_249c_0037.inc}
var
  recordBytes: array[0..884] of Byte;
  f: file;
  segment, errorCode, callerOffset, entry, restoreCount, index, mode: Word;
  base: LongInt;
  openBytes: array[0..151] of Byte;
  scenario, used, outputHandle: Word;
  openOutput: Boolean;
  outputFile: file;
  textError: Boolean;
  textBytes: array[0..4261] of Byte;
  writeCalls: Word;
function WriteOutput(handle, count: Word; source: Pointer; var written: Word): Word;
begin
  if textError then begin
    if ((writeCalls = 0) and (count <> 2)) or
       ((writeCalls = 1) and (count <> 0)) or (writeCalls > 1) then Halt(2);
    if writeCalls = 0 then begin
      WriteWordLE(@textBytes, 0, count);
      WriteWordLE(@textBytes, 2, $D7B2);
      Move(RealModeMemory[$B8000], textBytes[6], 4000);
      Move(RealModeMemory[base + $8200], textBytes[4006], 256);
    end;
  end;
  if (handle <> outputHandle) or (not textError and (count <> used)) or
     (source <> @RealModeMemory[base + $7A70]) or
     (PWord(@RealModeMemory[base + $79F8])^ <> 0) then Halt(2);
  Inc(writeCalls);
  WriteWordLE(@openBytes, 2, writeCalls);
  WriteWordLE(@openBytes, 6, count);
  WriteWordLE(@openBytes, 8, $D7B2);
  WriteWordLE(@openBytes, 18, segment);
  WriteWordLE(@openBytes, 20, $7A70);
  WriteWordLE(@openBytes, 22, 1);
  if count <> 0 then Move(source^, openBytes[24], count);
  written := 0;
  if scenario = 1 then WriteOutput := 6
  else if (scenario = 2) or (scenario = 4) then WriteOutput := 5
  else begin
    if scenario = 0 then BlockWrite(outputFile, source^, count);
    written := count;
    WriteOutput := 0;
  end;
end;
function CloseOutput(handle: Word): Word;
begin
  if handle <= 4 then Halt(2);
  WriteWordLE(@openBytes, 4, 1);
  WriteWordLE(@openBytes, 12, $D7B2);
  WriteWordLE(@openBytes, 16, handle);
  WriteWordLE(@openBytes, 22, $12);
  if (scenario = 1) or (scenario >= 3) then CloseOutput := 6
  else CloseOutput := 0;
end;
function ResolveCleanup(slot, objectSegment, objectOffset: Word): Word;
var
  address: LongInt;
begin
  if (objectSegment <> segment) or
     ((objectOffset <> $78F0) and (objectOffset <> $79F0)) or
     ((slot <> $14) and (slot <> $1C)) then RunError(211);
  address := base + objectOffset;
  if PWord(@RealModeMemory[address + slot + 2])^ <> segment then RunError(211);
  if (slot = $1C) and
     (PWord(@RealModeMemory[address + slot])^ = $37D3) then
    ResolveCleanup := FUN_24dd_37d3(@RealModeMemory[address], CloseOutput)
  else if (slot = $14) and (objectOffset = $79F0) and
          (PWord(@RealModeMemory[address + slot])^ = $37B3) then
    ResolveCleanup := FUN_24dd_37b3(@RealModeMemory[address],
      @RealModeMemory[base + $7A70], WriteOutput)
  else RunError(211);
end;
procedure RestoreVector(vector: Byte; offset, segment: Word);
begin
  if restoreCount >= 19 then Halt(2);
  recordBytes[662 + restoreCount] := vector;
  WriteWordLE(@recordBytes, 681 + restoreCount * 4, offset);
  WriteWordLE(@recordBytes, 683 + restoreCount * 4, segment);
  Inc(restoreCount);
end;
procedure Terminate(status: Byte);
begin
  WriteWordLE(@recordBytes, 0, segment);
  WriteWordLE(@recordBytes, 2, $4C00 or status);
  WriteWordLE(@recordBytes, 4, RegisterDS);
  WriteWordLE(@recordBytes, 6, RegisterSS);
  WriteWordLE(@recordBytes, 8, RegisterSP - 6);
  WriteWordLE(@recordBytes, 10, RegisterBP);
  WriteWordLE(@recordBytes, 12, restoreCount);
  WriteWordLE(@recordBytes, 14, DosOutputCount);
  WriteWordLE(@RealModeMemory[base], $6410, GlobalWord6410);
  Move(RealModeMemory[base + $63D8], recordBytes[16], 58);
  Move(RealModeMemory[base + $78F0], recordBytes[74], 588);
  if DosOutputCount > 128 then Halt(2);
  Move(DosOutputBuffer[0], recordBytes[757], DosOutputCount);
  Assign(f, 'PASCAL.BIN'); Rewrite(f, 1);
  BlockWrite(f, recordBytes, SizeOf(recordBytes));
  if openOutput then begin
    BlockWrite(f, openBytes, SizeOf(openBytes));
    if textError then BlockWrite(f, textBytes, SizeOf(textBytes));
    Close(outputFile);
  end;
  Close(f);
  Halt(status);
end;
begin
  Val(ParamStr(1), segment, mode);
  Val(ParamStr(2), errorCode, mode);
  Val(ParamStr(3), callerOffset, mode);
  Val(ParamStr(4), entry, mode);
  base := LongInt(segment) * 16;
  FillChar(RealModeMemory, SizeOf(RealModeMemory), 0);
  FillChar(RealModeMemory[base + $63D8], 58, $A5);
  WriteWordLE(@RealModeMemory[base], $63E4, 0);
  WriteWordLE(@RealModeMemory[base], $6402, 0);
  WriteWordLE(@RealModeMemory[base], $6404, 0);
  WriteWordLE(@RealModeMemory[base], $640C, segment - 16);
  WriteWordLE(@RealModeMemory[base], $6410, errorCode);
  WriteWordLE(@RealModeMemory[base], $78F2, $D7B0);
  WriteWordLE(@RealModeMemory[base], $79F2, $D7B0);
  Assign(f, 'VECTORS.BIN'); Reset(f, 1);
  BlockRead(f, RealModeMemory[base + $7AF0], 76); Close(f);
  Assign(f, 'CODE.BIN'); Reset(f, 1);
  BlockRead(f, CodeMemory, SizeOf(CodeMemory)); Close(f);
  WriteWordLE(@RealModeMemory[base], $EFF0, callerOffset);
  if callerOffset = 0 then index := 0 else index := segment + $200;
  WriteWordLE(@RealModeMemory[base], $EFF2, index);
  LieroErrorDataSegment := segment;
  LieroErrorCodeSegment := segment;
  LieroRestoreVector := RestoreVector;
  LieroTerminate := Terminate;
  RegisterSS := segment; RegisterSP := $EFF0; RegisterBP := $6789;
  GlobalWord6410 := errorCode; RegisterAX := errorCode;
  openOutput := ParamCount >= 7;
  textError := entry = 2;
  if openOutput then begin
    Val(ParamStr(5), scenario, mode);
    Val(ParamStr(6), used, mode);
    Val(ParamStr(7), outputHandle, mode);
    Assign(outputFile, 'OUTPUT.BIN'); Rewrite(outputFile, 1);
    WriteWordLE(@openBytes, 0, outputHandle);
    WriteWordLE(@RealModeMemory[base], $78F2, $D7B1);
    WriteWordLE(@RealModeMemory[base], $790C, $37D3);
    WriteWordLE(@RealModeMemory[base], $790E, segment);
    WriteWordLE(@RealModeMemory[base], $79F0, outputHandle);
    WriteWordLE(@RealModeMemory[base], $79F2, $D7B2);
    WriteWordLE(@RealModeMemory[base], $79F4, 128);
    WriteWordLE(@RealModeMemory[base], $79F8, used);
    WriteWordLE(@RealModeMemory[base], $79FC, $7A70);
    WriteWordLE(@RealModeMemory[base], $79FE, segment);
    WriteWordLE(@RealModeMemory[base], $7A04, $37B3);
    WriteWordLE(@RealModeMemory[base], $7A06, segment);
    WriteWordLE(@RealModeMemory[base], $7A0C, $37D3);
    WriteWordLE(@RealModeMemory[base], $7A0E, segment);
    FillChar(RealModeMemory[base + $7A70], 128, Ord('A'));
    LieroDispatchMethod := ResolveCleanup;
  end;
  if ParamCount = 8 then begin
    Val(ParamStr(8), mode, index);
    case mode of
      1: LieroDispatchMethod := nil;
      2: WriteWordLE(@RealModeMemory[base], $79FC, $6410);
      3: WriteWordLE(@RealModeMemory[base], $7A04, $378E);
      4: WriteWordLE(@RealModeMemory[base], $7A06, segment + 1);
      5: WriteWordLE(@RealModeMemory[base], $79F2, $D7B3);
      6: WriteWordLE(@RealModeMemory[base], $79F8, 129);
      7: WriteWordLE(@RealModeMemory[base], $790C, $37B3);
      8: RegisterSP := $7A70;
    else Halt(2);
    end;
  end;
  if textError then begin
    if not openOutput then Halt(2);
    GlobalWord6410 := 0;
    WriteWordLE(@RealModeMemory[base], $6410, 0);
    WriteWordLE(@RealModeMemory[base], $6424, $0A0D);
    WriteWordLE(@RealModeMemory[base], $7A08, $37B3);
    WriteWordLE(@RealModeMemory[base], $7A0A, segment);
    RealModeMemory[base + $8200] := 5;
    RealModeMemory[base + $8201] := Ord('A');
    RealModeMemory[base + $8202] := 0;
    RealModeMemory[base + $8203] := 2;
    RealModeMemory[base + $8204] := 3;
    RealModeMemory[base + $8205] := Ord('B');
    for index := 0 to 1999 do
      WriteWordLE(@RealModeMemory[$B8000], index * 2, $4F2E);
    BIOSVideoMode := 3;
    LieroTextDataSegment := segment;
    LieroTextCodeSegment := segment + $300;
    LieroBufferCodeSegment := segment;
    LieroBufferObjectSegment := segment;
    LieroBufferObjectOffset := $79F0;
    LieroBufferSourceSegment := segment;
    LieroBufferSourceOffset := $7A70;
    LieroBufferObject := @RealModeMemory[base + $79F0];
    LieroBufferSource := @RealModeMemory[base + $7A70];
    LieroBufferDosWrite := WriteOutput;
    RegisterDS := segment; RegisterSP := $DFE4;
    FUN_249c_0037(@RealModeMemory[base + $8200], 2, 3);
    Halt(99);
  end;
  if ParamCount = 5 then begin
    Val(ParamStr(5), mode, index);
    case mode of
      1: WriteWordLE(@RealModeMemory[base], $63E4, segment);
      2: WriteWordLE(@RealModeMemory[base], $6402, 1);
      3: WriteWordLE(@RealModeMemory[base], $79F2, $D7B2);
      4: RegisterSP := $6406;
      5: LieroTerminate := nil;
      6: LieroErrorDataSegment := $FFFF;
    else Halt(2);
    end;
  end;
  if entry = 0 then FUN_24dd_010f else FUN_24dd_04f4;
  Halt(99);
end.
