program ProbeLieroBufferHandler;
{$MODE TP}
uses LieroRuntime;
{$I FUN_24dd_375e.inc}
{$I FUN_24dd_39ab.inc}
{$I FUN_24dd_390e.inc}
{$I FUN_24dd_3923.inc}
{$I FUN_24dd_396c.inc}
{$I FUN_24dd_37ec.inc}
type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
const
  Limits: array[0..3] of Word = (7, 111, 1, 111);
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  Actual: Longint;
  Step, ParseError: Integer;
  Kind, HandleValue, InstrumentFlag: Word;

function ReadInput(handle, count: Word; destination: Pointer;
                   var received: Word): Word;
var
  actual: Longint;
  error: Integer;
begin
  { Oracle: actual read service boundary, invalid handle6 only; unknown I/O aborts. }
  received := 0;
  if handle = $FFFF then
  begin
    ReadInput := 6;
    Exit;
  end;
  if handle <> HandleValue then Halt(7);
  {$I-}
  BlockRead(InputFile, destination^, count, actual);
  error := IOResult;
  {$I+}
  if error <> 0 then Halt(8);
  received := actual;
  ReadInput := 0;
end;

begin
  { Oracle: actual dispatcher/bridge/leaves, original open seeds all512 bytes. }
  if (ParamCount <> 4) and (ParamCount <> 5) then Halt(2);
  Val(ParamStr(4), Kind, ParseError);
  if (ParseError <> 0) or (Kind > 1) then Halt(3);
  Assign(StateFile, ParamStr(1));
  Reset(StateFile, 1);
  if FileSize(StateFile) <> SizeOf(State) then Halt(4);
  BlockRead(StateFile, State, SizeOf(State), Actual);
  Close(StateFile);
  if Actual <> SizeOf(State) then Halt(4);
  Move(State.ObjectData[0], HandleValue, 2);
  Assign(InputFile, ParamStr(2));
  Reset(InputFile, 1);
  LieroBufferObject := @State.ObjectData[0];
  LieroBufferSource := @State.ObjectData[128];
  LieroBufferDestination := @State.Destination[0];
  LieroBufferDosRead := ReadInput;
  Move(State.ObjectData[22], LieroBufferCodeSegment, 2);
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 0 to 7 do
  begin
    FillChar(State.Destination, SizeOf(State.Destination), $A5);
    RegisterSI := $BEEF;
    RegisterDI := 0;
    RegisterCX := Limits[Step div 2];
    RegisterAX := $39AB;
    if Step mod 2 <> 0 then RegisterAX := $390E;
    if (Kind = 1) and (Step = 0) then
      FillChar(State.ObjectData[0], 2, $FF);
    if Step = 6 then GlobalWord6410 := $55AA;
    if Step = 7 then
    begin
      GlobalWord6410 := 0;
      FillChar(State.ObjectData[2], 2, $12);
    end;
    if (ParamCount = 5) and (Step = 0) then
    begin
      if ParamStr(5) = 'unknown-callback' then RegisterAX := $1234
      else if ParamStr(5) = 'unknown-method' then
        FillChar(State.ObjectData[22], 2, $12)
      else if ParamStr(5) = 'nil-source' then LieroBufferSource := nil
      else if ParamStr(5) = 'bad-count' then
        FillChar(State.ObjectData[10], 2, $FF)
      else if ParamStr(5) = 'missing-adapter' then LieroBufferDosRead := nil
      else
        Halt(9);
    end;
    FUN_24dd_37ec;
    Move(RegisterSI, State.ObjectData[32], 2);
    Move(RegisterDI, State.ObjectData[34], 2);
    Move(RegisterCX, State.ObjectData[36], 2);
    Move(RegisterAX, State.ObjectData[38], 2);
    InstrumentFlag := Ord(RegisterZeroFlag);
    Move(InstrumentFlag, State.ObjectData[40], 2);
    BlockWrite(OutputFile, GlobalWord6410, 2, Actual);
    if Actual <> 2 then Halt(5);
    BlockWrite(OutputFile, State, SizeOf(State), Actual);
    if Actual <> SizeOf(State) then Halt(5);
  end;
  Close(OutputFile);
  Close(InputFile);
end.
