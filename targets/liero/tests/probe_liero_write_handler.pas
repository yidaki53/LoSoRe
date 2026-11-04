program ProbeLieroWriteHandler;
{$MODE TP}
uses LieroRuntime;
{$I FUN_24dd_374d.inc}
{$I FUN_24dd_375e.inc}
{$I FUN_24dd_37b3.inc}
{$I FUN_24dd_396c.inc}
{$I FUN_24dd_397a.inc}
type
  TArena = array[0..4095] of Byte;
var
  arena: TArena;
  input: array[0..3] of Word;
  observed: array[0..5] of Word;
  casesFile, resultFile, targetFile: File;
  transferred: LongInt;
  handleValue, segmentValue, bufferSegment, bufferOffset: Word;
  calls, seenHandle, seenCount, seenUsed: Word;
  mode, error, dispatch: Integer;
  methodOffset: Word;

function WriteOutput(handle, count: Word; source: Pointer;
                     var bytesWritten: Word): Word;
begin
  { Oracle: actual host file write, observed NUL/error projection, or labeled
    injected service outcome. No emulation of other native DOS effects. }
  Inc(calls);
  seenHandle := handle;
  seenCount := count;
  Move(arena[8], seenUsed, 2);
  if (source <> @arena[256]) or (count <> input[0]) or (count > 128) or
     (seenUsed <> 0) or (handle <> handleValue) then Halt(10);
  bytesWritten := 0;
  case mode of
    0: begin
      BlockWrite(targetFile, arena[256], count, transferred);
      if transferred <> count then Halt(11);
      bytesWritten := transferred;
      WriteOutput := 0;
    end;
    1: begin bytesWritten := count; WriteOutput := 0 end;
    2: WriteOutput := 6;
    3: begin
      if input[1] = 0 then begin
        bytesWritten := input[2];
        WriteOutput := 0;
      end else WriteOutput := input[2];
    end;
  else Halt(12);
  end;
end;

begin
  { Oracle: installed leaf and exact owned arena, original handle/segment
    supplied as explicit resolved bindings, not native allocation/ABI parity. }
  if (ParamCount <> 5) and (ParamCount <> 6) then Halt(1);
  Val(ParamStr(1), mode, error); if error <> 0 then Halt(2);
  Val(ParamStr(2), handleValue, error); if error <> 0 then Halt(2);
  Val(ParamStr(3), segmentValue, error); if error <> 0 then Halt(2);
  Val(ParamStr(4), dispatch, error); if error <> 0 then Halt(2);
  Val(ParamStr(5), methodOffset, error); if error <> 0 then Halt(2);
  if (mode < 0) or (mode > 3) then Halt(2);
  if (dispatch < 0) or (dispatch > 2) then Halt(2);
  Assign(casesFile, 'CASES.BIN'); Reset(casesFile, 1);
  Assign(resultFile, 'PASCAL.BIN'); Rewrite(resultFile, 1);
  if mode = 0 then begin
    Assign(targetFile, 'OUTPUT.BIN'); Rewrite(targetFile, 1);
  end;
  while not Eof(casesFile) do begin
    BlockRead(casesFile, input, 8, transferred); if transferred <> 8 then Halt(3);
    BlockRead(casesFile, arena, 4096, transferred); if transferred <> 4096 then Halt(3);
    Move(handleValue, arena[0], 2);
    bufferSegment := segmentValue + input[3];
    bufferOffset := $8100 - LongInt(input[3]) * 16;
    Move(bufferOffset, arena[12], 2);
    Move(bufferSegment, arena[14], 2);
    GlobalWord6410 := 0;
    if input[3] <> 0 then GlobalWord6410 := $55AA;
    if dispatch <> 0 then begin
      Move(methodOffset, arena[20], 2);
      Move(segmentValue, arena[22], 2);
      Move(methodOffset, arena[24], 2);
      Move(segmentValue, arena[26], 2);
      { Oracle: original method offset is explicitly resolved to installed37b3,
        not a host-address comparison or native ABI claim. }
      LieroBufferObject := @arena[0];
      LieroBufferSource := @arena[256];
      LieroBufferObjectOffset := $8000;
      LieroBufferObjectSegment := segmentValue;
      LieroBufferSourceOffset := bufferOffset;
      LieroBufferSourceSegment := bufferSegment;
      LieroBufferCodeSegment := segmentValue;
      LieroBufferDosWrite := WriteOutput;
      RegisterES := segmentValue;
      RegisterBX := $8000;
      { The relocated fixture offset maps to original logical method37b3. }
      PWord(@arena[20])^ := $37B3;
      PWord(@arena[24])^ := $37B3;
      if ParamCount = 6 then begin
        if ParamStr(6) = 'nil-object' then LieroBufferObject := nil
        else if ParamStr(6) = 'nil-source' then LieroBufferSource := nil
        else if ParamStr(6) = 'missing-write' then LieroBufferDosWrite := nil
        else if ParamStr(6) = 'wrong-object' then RegisterBX := 0
        else if ParamStr(6) = 'wrong-object-segment' then RegisterES := 0
        else if ParamStr(6) = 'wrong-source' then LieroBufferSourceOffset := 0
        else if ParamStr(6) = 'wrong-source-segment' then LieroBufferSourceSegment := 0
        else if ParamStr(6) = 'wrong-code-segment' then LieroBufferCodeSegment := 0
        else if ParamStr(6) = 'bad-count' then PWord(@arena[8])^ := 129
        else if ParamStr(6) = 'unknown-method' then begin
          PWord(@arena[20])^ := $378E; PWord(@arena[24])^ := $378E;
        end else Halt(15);
      end;
    end;
    calls := 0; seenUsed := $ffff; seenHandle := 0; seenCount := 0;
    if dispatch = 0 then
      observed[0] := FUN_24dd_37b3(@arena[0], @arena[256], WriteOutput)
    else begin
      if dispatch = 1 then FUN_24dd_396c else FUN_24dd_397a;
      observed[0] := RegisterAX;
      if (RegisterBX <> handleValue) or (RegisterDI <> $8000) or
         (RegisterES <> segmentValue) or
         (RegisterZeroFlag <> (RegisterAX = 0)) then Halt(13);
      if (PWord(@arena[20])^ <> $37B3) or
         (PWord(@arena[24])^ <> $37B3) or
         (PWord(@arena[22])^ <> segmentValue) or
         (PWord(@arena[26])^ <> segmentValue) then Halt(14);
      Move(methodOffset, arena[20], 2);
      Move(methodOffset, arena[24], 2);
    end;
    observed[1] := calls; observed[2] := seenHandle; observed[3] := seenCount;
    observed[4] := seenUsed;
    observed[5] := 0;
    if dispatch <> 0 then observed[5] := GlobalWord6410;
    BlockWrite(resultFile, observed, 12, transferred); if transferred <> 12 then Halt(4);
    BlockWrite(resultFile, arena, 4096, transferred); if transferred <> 4096 then Halt(4);
  end;
  if mode = 0 then Close(targetFile);
  Close(casesFile); Close(resultFile);
end.
