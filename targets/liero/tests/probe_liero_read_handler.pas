program ProbeLieroReadHandler;

{$MODE TP}

{$I FUN_24dd_375e.inc}

type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  Count: Longint;
  HandleValue, Capacity, Status, BytesRead: Word;
  Step: Integer;

function ReadInput(handle, count: Word; destination: Pointer;
                   var received: Word): Word;
var
  actual: Longint;
  error: Integer;
begin
  { Oracle: host adapter for a valid read or DOS invalid-handle error 6.
    Unexpected host I/O errors abort instead of masquerading as DOS results. }
  received := 0;
  if count > 128 then
    Halt(9);
  if handle = $FFFF then
  begin
    ReadInput := 6;
    Exit;
  end;
  if handle <> HandleValue then
    Halt(7);
  {$I-}
  BlockRead(InputFile, destination^, count, actual);
  error := IOResult;
  {$I+}
  if error <> 0 then
    Halt(8);
  received := actual;
  ReadInput := 0;
end;

begin
  { Oracle: actual candidate body, seeded with original post-open memory.
    No host reconstruction of open/setup is substituted for the original. }
  if ParamCount <> 4 then
    Halt(2);
  Val(ParamStr(4), Capacity, Step);
  if (Step <> 0) or (Capacity > 128) then
    Halt(3);
  Assign(StateFile, ParamStr(1));
  Reset(StateFile, 1);
  if FileSize(StateFile) <> SizeOf(State) then
    Halt(4);
  BlockRead(StateFile, State, SizeOf(State), Count);
  Close(StateFile);
  if Count <> SizeOf(State) then
    Halt(4);
  Move(State.ObjectData[0], HandleValue, 2);
  Move(Capacity, State.ObjectData[4], 2);
  Assign(InputFile, ParamStr(2));
  Reset(InputFile, 1);
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 3 to 10 do
  begin
    if Step = 10 then
      FillChar(State.ObjectData[0], 2, $FF);
    BytesRead := $55AA;
    Move(BytesRead, State.ObjectData[8], 2);
    FillChar(State.ObjectData[10], 2, $FF);
    Status := FUN_24dd_375e(@State.ObjectData[0], @State.ObjectData[128], ReadInput);
    BlockWrite(OutputFile, Status, 2, Count);
    if Count <> 2 then
      Halt(5);
    BlockWrite(OutputFile, State, SizeOf(State), Count);
    if Count <> SizeOf(State) then
      Halt(5);
  end;
  Close(OutputFile);
  Close(InputFile);
end.
