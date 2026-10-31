program ProbeLieroDispatchHandler;

{$MODE TP}

uses LieroRuntime;

{$I FUN_24dd_375e.inc}
{$I FUN_24dd_37d3.inc}
procedure FUN_24dd_374d; forward;
{$I FUN_24dd_374d.inc}

type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  Count: Longint;
  HandleValue, SegmentValue, SyntheticReturn, Marker: Word;
  Step: Integer;
  InputOpen: Boolean;

function ReadInput(handle, count: Word; destination: Pointer;
                   var received: Word): Word;
var
  actual: Longint;
  error: Integer;
begin
  { Oracle: scoped host read adapter; closed/unmapped handles return DOS error 6. }
  received := 0;
  if (handle <> HandleValue) or not InputOpen then
  begin
    ReadInput := 6;
    Exit;
  end;
  {$I-}
  BlockRead(InputFile, destination^, count, actual);
  error := IOResult;
  {$I+}
  if error <> 0 then
    Halt(8);
  received := actual;
  ReadInput := 0;
end;

function CloseInput(handle: Word): Word;
var
  error: Integer;
begin
  { Oracle: scoped host close adapter for one observed DOS handle. }
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

function InvokeMethod(slotOffset, objectSegment, objectOffset: Word): Word;
var
  methodOffset, methodSegment: Word;
begin
  { Oracle: bounded resolver for checked leaves plus the labeled synthetic callback.
    No unknown far pointer or setup/output method receives a guessed result. }
  if (objectSegment <> SegmentValue) or (objectOffset <> $FEFA) then
    Halt(9);
  if (slotOffset <> $14) and (slotOffset <> $18) and (slotOffset <> $1C) then
    Halt(10);
  Move(State.ObjectData[slotOffset], methodOffset, 2);
  Move(State.ObjectData[slotOffset + 2], methodSegment, 2);
  if methodSegment <> SegmentValue then
    Halt(11);
  if (slotOffset = $14) and (methodOffset = $375E) then
    InvokeMethod := FUN_24dd_375e(@State.ObjectData[0], @State.ObjectData[128], ReadInput)
  else if (slotOffset = $1C) and (methodOffset = $37D3) then
    InvokeMethod := FUN_24dd_37d3(@State.ObjectData[0], CloseInput)
  else if (slotOffset = $18) and (methodOffset = $0400) then
  begin
    Move(State.ObjectData[6], Marker, 2);
    Marker := (Longint(Marker) + 1) and $FFFF;
    Move(Marker, State.ObjectData[6], 2);
    RegisterES := $1234;
    RegisterDI := $BEEF;
    InvokeMethod := SyntheticReturn;
  end
  else
    Halt(12);
end;

begin
  { Oracle: actual dispatcher composed with actual Pascal leaves; original open fixture. }
  if ParamCount <> 4 then
    Halt(2);
  if ParamStr(4) <> '128' then
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
  Move(State.ObjectData[14], SegmentValue, 2);
  Assign(InputFile, ParamStr(2));
  Reset(InputFile, 1);
  InputOpen := True;
  LieroDispatchMethod := InvokeMethod;
  GlobalWord6410 := $55AA;
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 3 to 10 do
  begin
    RegisterBX := $1C;
    if (Step = 3) or (Step = 7) then
      RegisterBX := $14;
    if Step = 6 then
    begin
      Marker := 4;
      Move(Marker, State.ObjectData[0], 2);
    end;
    if Step = 7 then
      FillChar(State.ObjectData[0], 2, $FF);
    if Step >= 8 then
    begin
      RegisterBX := $18;
      if Step = 8 then
        SyntheticReturn := $1234
      else if Step = 9 then
        SyntheticReturn := 0
      else
        SyntheticReturn := $FFFF;
    end;
    RegisterES := SegmentValue;
    RegisterDI := $FEFA;
    FUN_24dd_374d;
    Move(RegisterAX, State.Destination[0], 2);
    Move(RegisterES, State.Destination[2], 2);
    Move(RegisterDI, State.Destination[4], 2);
    Marker := Ord(RegisterZeroFlag);
    Move(Marker, State.Destination[6], 2);
    BlockWrite(OutputFile, GlobalWord6410, 2, Count);
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
