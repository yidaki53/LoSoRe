program ProbeLieroText;
{$MODE TP}
uses LieroRuntime;
procedure FUN_24dd_396c; forward;
procedure FUN_24dd_397a; forward;
procedure FUN_24dd_0232(param_1: Word); forward;
function FUN_24dd_020a: Word; forward;
procedure FUN_24dd_021f; forward;
procedure FUN_24dd_022a; forward;
{$I FUN_24dd_374d.inc}
{$I FUN_24dd_375e.inc}
{$I FUN_24dd_37b3.inc}
{$I FUN_24dd_396c.inc}
{$I FUN_24dd_397a.inc}
{$I FUN_24dd_3899.inc}
{$I FUN_24dd_3930.inc}
{$I FUN_24dd_3711.inc}
{$I FUN_24dd_0232.inc}
{$I FUN_24dd_020a.inc}
{$I FUN_24dd_01fe.inc}
{$I FUN_24dd_022a.inc}
{$I FUN_24dd_021f.inc}
{$I FUN_24dd_0218.inc}
{$I FUN_24dd_01f0.inc}
{$I FUN_24dd_010f.inc}
{$I FUN_24dd_04f4.inc}
{$I FUN_249c_0013.inc}
{$I FUN_249c_0000.inc}
{$I FUN_249c_0037.inc}
type
  TCase = packed record
    Count, Row, Column, Capacity, Used, Sticky, Mode, Optional,
      SourceBias, Carry, Returned, InvalidHandle: Word;
    ObjectBytes, SourceBytes: array[0..255] of Byte;
  end;
var
  data: TCase;
  inputFile, resultFile, outputFile: File;
  actual: LongInt;
  fixtureSegment, fixtureHandle, currentHandle, calls: Word;
  observation: array[0..3] of Word;
  serviceCounts: array[0..255] of Word;
  serviceBytes: array[0..511] of Byte;
  sent: Word;
  entry, injected, parseError: Integer;
  objectAddress, bufferAddress, dataAddress, sourceAddress: LongInt;
  i: Word;

function WriteOutput(handle, count: Word; source: Pointer;
                     var bytesWritten: Word): Word;
var
  index: Word;
begin
  { Oracle: actual host file write or explicitly labeled service mechanism. }
  if calls >= 256 then Halt(13);
  serviceCounts[calls] := count;
  Inc(calls);
  if (handle <> currentHandle) or (count > 128) or
     (source <> @RealModeMemory[bufferAddress]) or
     (PWord(@RealModeMemory[objectAddress + 8])^ <> 0) then Halt(10);
  if LongInt(sent) + count > 512 then Halt(14);
  if count <> 0 then Move(source^, serviceBytes[sent], count);
  Inc(sent, count);
  bytesWritten := 0;
  if (injected = 2) or (injected = 3) then begin
    { Oracle: actual installed mode3 CR/LF service projection, including scroll. }
    if count <> 0 then
      for index := 0 to count - 1 do
        WriteConsoleCRLFByte(PByte(source)[index]);
    bytesWritten := count;
    WriteOutput := 0;
  end else if injected <> 0 then begin
    if data.Carry <> 0 then WriteOutput := data.Returned
    else begin bytesWritten := data.Returned; WriteOutput := 0 end;
  end else if data.InvalidHandle <> 0 then WriteOutput := 6
  else begin
    BlockWrite(outputFile, source^, count, actual);
    if actual <> count then Halt(11);
    bytesWritten := actual;
    WriteOutput := 0;
  end;
end;

begin
  { Oracle: installed full bodies and logical segmented/video observations;
    native allocation, ABI and original stack scratch are not modeled. }
  if ParamCount <> 4 then Halt(1);
  Val(ParamStr(1), entry, parseError); if parseError <> 0 then Halt(2);
  Val(ParamStr(2), injected, parseError); if parseError <> 0 then Halt(2);
  Val(ParamStr(3), fixtureSegment, parseError); if parseError <> 0 then Halt(2);
  Val(ParamStr(4), fixtureHandle, parseError); if parseError <> 0 then Halt(2);
  if (entry < 0) or (entry > 2) or (injected < 0) or
     (injected > 3) then Halt(2);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(resultFile, 'PASCAL.BIN'); Rewrite(resultFile, 1);
  Assign(outputFile, 'OUTPUT.BIN'); Rewrite(outputFile, 1);
  dataAddress := LongInt(fixtureSegment) * 16;
  objectAddress := dataAddress + $79F0;
  bufferAddress := dataAddress + $7A70;
  sourceAddress := dataAddress + $8200;
  while not Eof(inputFile) do begin
    BlockRead(inputFile, data, SizeOf(data), actual);
    if actual <> SizeOf(data) then Halt(3);
    FillChar(RealModeMemory, SizeOf(RealModeMemory), 0);
    Move(data.ObjectBytes, RealModeMemory[objectAddress], 256);
    Move(data.SourceBytes, RealModeMemory[sourceAddress], 256);
    for i := 0 to 1999 do begin
      RealModeMemory[$B8000 + LongInt(i) * 2] := $2E;
      RealModeMemory[$B8001 + LongInt(i) * 2] := $4F;
    end;
    currentHandle := fixtureHandle;
    if data.InvalidHandle <> 0 then currentHandle := $FFFF;
    WriteWordLE(@RealModeMemory[objectAddress], 0, currentHandle);
    WriteWordLE(@RealModeMemory[objectAddress], 2, data.Mode);
    WriteWordLE(@RealModeMemory[objectAddress], 4, data.Capacity);
    WriteWordLE(@RealModeMemory[objectAddress], 8, data.Used);
    LieroBufferSourceOffset := $7A70 - LongInt(data.SourceBias) * 16;
    LieroBufferSourceSegment := fixtureSegment + data.SourceBias;
    WriteWordLE(@RealModeMemory[objectAddress], 12, LieroBufferSourceOffset);
    WriteWordLE(@RealModeMemory[objectAddress], 14, LieroBufferSourceSegment);
    WriteWordLE(@RealModeMemory[objectAddress], 20, $37B3);
    WriteWordLE(@RealModeMemory[objectAddress], 22, fixtureSegment);
    WriteWordLE(@RealModeMemory[objectAddress], 24, $37B3);
    if data.Optional <> 0 then i := fixtureSegment else i := 0;
    WriteWordLE(@RealModeMemory[objectAddress], 26, i);
    RealModeMemory[dataAddress + $6424] := 13;
    RealModeMemory[dataAddress + $6425] := 10;
    LieroBufferObject := @RealModeMemory[objectAddress];
    LieroBufferSource := @RealModeMemory[bufferAddress];
    LieroBufferObjectOffset := $79F0;
    LieroBufferObjectSegment := fixtureSegment;
    LieroBufferCodeSegment := fixtureSegment;
    LieroBufferDosWrite := WriteOutput;
    LieroTextDataSegment := fixtureSegment;
    RegisterDS := fixtureSegment; RegisterES := fixtureSegment;
    RegisterSS := fixtureSegment; RegisterBP := $6789;
    RegisterSP := $DFF0;
    BIOSVideoMode := 3; BIOSCursorRow := 0; BIOSCursorColumn := 0;
    GlobalWord6410 := data.Sticky;
    RegisterBX := $79F0; RegisterSI := $8200;
    RegisterDX := fixtureSegment; RegisterAX := data.Count;
    FillChar(serviceCounts, SizeOf(serviceCounts), $FF);
    FillChar(serviceBytes, SizeOf(serviceBytes), $FF);
    sent := 0;
    calls := 0;
    case entry of
      0: begin RegisterSP := $DFEE; FUN_24dd_3899; RegisterSP := $DFF0 end;
      1: begin
        RegisterSP := $DFE8;
        FUN_24dd_3930((LongInt(fixtureSegment) shl 16) or $79F0);
      end;
      2: begin
        RegisterSP := $DFE4;
        FUN_249c_0037(@RealModeMemory[sourceAddress], data.Row, data.Column);
      end;
    else Halt(4);
    end;
    if (RegisterSP <> $DFF0) or (RegisterBP <> $6789) or
       (RegisterDS <> fixtureSegment) then Halt(12);
    observation[0] := GlobalWord6410;
    observation[1] := calls;
    observation[2] := Word(BIOSCursorRow) * 256 + BIOSCursorColumn;
    observation[3] := Ord(RegisterZeroFlag);
    BlockWrite(resultFile, observation, 8, actual); if actual <> 8 then Halt(5);
    BlockWrite(resultFile, RealModeMemory[objectAddress], 256, actual);
    if actual <> 256 then Halt(5);
    BlockWrite(resultFile, RealModeMemory[sourceAddress], 256, actual);
    if actual <> 256 then Halt(5);
    BlockWrite(resultFile, RealModeMemory[$B8000], 4000, actual);
    if actual <> 4000 then Halt(5);
    BlockWrite(resultFile, serviceCounts, SizeOf(serviceCounts), actual);
    if actual <> SizeOf(serviceCounts) then Halt(5);
    BlockWrite(resultFile, serviceBytes, SizeOf(serviceBytes), actual);
    if actual <> SizeOf(serviceBytes) then Halt(5);
  end;
  Close(inputFile); Close(resultFile); Close(outputFile);
end.
