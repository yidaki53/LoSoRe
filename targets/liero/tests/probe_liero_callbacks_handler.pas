program ProbeLieroCallbacksHandler;
{$MODE TP}
{$I FUN_24dd_39ab.inc}
{$I FUN_24dd_390e.inc}
type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
const
  Limits: array[0..3] of Word = (0, 1, 7, 255);
var
  StateFile, OutputFile: File;
  Baseline, State: TState;
  Actual: Longint;
  Step: Integer;
  Status, SourceOffset, DestinationOffset, Remaining, BufferEnd: Word;
begin
  { Oracle: actual callbacks over captured original buffer, not duplicate adapters. }
  if ParamCount <> 4 then Halt(2);
  Assign(StateFile, ParamStr(1));
  Reset(StateFile, 1);
  if FileSize(StateFile) <> SizeOf(State) then Halt(3);
  BlockRead(StateFile, Baseline, SizeOf(State), Actual);
  Close(StateFile);
  if Actual <> SizeOf(State) then Halt(3);
  Move(Baseline.ObjectData[10], BufferEnd, 2);
  if (BufferEnd = 0) or (BufferEnd > 128) then Halt(4);
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 0 to 7 do
  begin
    State := Baseline;
    FillChar(State.Destination, SizeOf(State.Destination), $A5);
    SourceOffset := 0;
    DestinationOffset := 0;
    Remaining := Limits[Step div 2];
    if Step mod 2 = 0 then
      Status := FUN_24dd_39ab(@State.ObjectData[128], @State.Destination[0],
                            SourceOffset, DestinationOffset, Remaining, BufferEnd)
    else
      Status := FUN_24dd_390e(@State.ObjectData[128], SourceOffset, BufferEnd);
    Move(SourceOffset, State.Destination[248], 2);
    Move(DestinationOffset, State.Destination[250], 2);
    Move(Remaining, State.Destination[252], 2);
    Move(Status, State.Destination[254], 2);
    BlockWrite(OutputFile, Status, 2, Actual);
    if Actual <> 2 then Halt(5);
    BlockWrite(OutputFile, State, SizeOf(State), Actual);
    if Actual <> SizeOf(State) then Halt(5);
  end;
  Close(OutputFile);
end.
