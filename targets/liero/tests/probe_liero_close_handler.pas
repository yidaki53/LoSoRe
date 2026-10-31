program ProbeLieroCloseHandler;

{$MODE TP}

{$I FUN_24dd_37d3.inc}

type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  Count: Longint;
  HandleValue, SelectedHandle, Status, AdapterCalls: Word;
  Step: Integer;
  InputOpen: Boolean;
  BoundaryProbe: Boolean;
const
  BoundaryHandles: array[0..4] of Word = (6, 7, 255, $8000, $FFFE);

function CloseInput(handle: Word): Word;
var
  error: Integer;
begin
  { Oracle: one live host file mapped to its observed DOS handle.
    Unsupported/reserved handles return 6 so illegal adapter calls are visible.
    Unexpected host close errors abort rather than being mapped speculatively. }
  Inc(AdapterCalls);
  if (handle <> HandleValue) or not InputOpen then
  begin
    CloseInput := 6;
    Exit;
  end;
  {$I-}
  Close(InputFile);
  error := IOResult;
  {$I+}
  if error <> 0 then
    Halt(8);
  InputOpen := False;
  CloseInput := 0;
end;

begin
  { Oracle: actual Pascal leaf seeded with original post-open memory;
    no Pascal reconstruction of open/setup is implied. }
  if ParamCount <> 4 then
    Halt(2);
  BoundaryProbe := ParamStr(4) = '129';
  if (ParamStr(4) <> '128') and not BoundaryProbe then
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
  if (HandleValue <= 4) or (HandleValue = $FFFF) then
    Halt(7);
  if BoundaryProbe then
    for Step := 0 to 4 do
      if HandleValue = BoundaryHandles[Step] then
        Halt(7);
  Assign(InputFile, ParamStr(2));
  Reset(InputFile, 1);
  InputOpen := True;
  AdapterCalls := 0;
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 3 to 10 do
  begin
    if Step <= 7 then
    begin
      if BoundaryProbe then
        SelectedHandle := BoundaryHandles[Step - 3]
      else
        SelectedHandle := Step - 3;
    end
    else if Step <= 9 then
      SelectedHandle := HandleValue
    else
      SelectedHandle := $FFFF;
    Move(SelectedHandle, State.ObjectData[0], 2);
    Status := FUN_24dd_37d3(@State.ObjectData[0], CloseInput);
    BlockWrite(OutputFile, Status, 2, Count);
    if Count <> 2 then
      Halt(5);
    BlockWrite(OutputFile, AdapterCalls, 2, Count);
    if Count <> 2 then
      Halt(5);
    BlockWrite(OutputFile, State, SizeOf(State), Count);
    if Count <> SizeOf(State) then
      Halt(5);
  end;
  Close(OutputFile);
  if InputOpen then
    Close(InputFile);
end.
