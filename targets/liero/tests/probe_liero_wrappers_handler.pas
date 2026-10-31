program ProbeLieroWrappersHandler;
{$MODE TP}
uses LieroRuntime;
{$I FUN_24dd_374d.inc}
{$I FUN_24dd_375e.inc}
{$I FUN_24dd_39ab.inc}
{$I FUN_24dd_390e.inc}
{$I FUN_24dd_3923.inc}
{$I FUN_24dd_396c.inc}
{$I FUN_24dd_37ec.inc}
{$I FUN_24dd_397a.inc}
{$I FUN_24dd_3988.inc}
{$I FUN_24dd_38f0.inc}
type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
  TLogicalRetainedArgument = packed record
    ObjectOffset, ObjectSegment, Active: Word;
  end;
  TObjectWords = array[0..127] of Word;
  PObjectWords = ^TObjectWords;
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  RetainedArgument: TLogicalRetainedArgument;
  RetainedObject: Pointer;
  Actual: Longint;
  Step, ParseError: Integer;
  Kind, OptionalReturn, HandleValue: Word;

function ReadInput(handle, count: Word; destination: Pointer;
                   var received: Word): Word;
var
  actual: Longint;
  error: Integer;
begin
  received := 0;
  if handle <> HandleValue then
  begin
    ReadInput := 6;
    Exit;
  end;
  {$I-}
  BlockRead(InputFile, destination^, count, actual);
  error := IOResult;
  {$I+}
  if error <> 0 then Halt(8);
  received := actual;
  ReadInput := 0;
end;

function ResolveOptionalMethod(slotOffset, objectSegment, objectOffset: Word): Word;
var
  words: PObjectWords;
begin
  words := LieroBufferObject;
  if (slotOffset <> $18) or (objectSegment <> LieroBufferCodeSegment) or
     (objectOffset <> LieroBufferObjectOffset) or (words^[12] <> $0400) or
     (words^[13] <> LieroBufferCodeSegment) then
    RunError(211);
  ResolveOptionalMethod := OptionalReturn;
end;

procedure CaptureWrapperState;
begin
  BlockWrite(OutputFile, GlobalWord6410, 2, Actual);
  if Actual <> 2 then Halt(5);
  BlockWrite(OutputFile, State, SizeOf(State), Actual);
  if Actual <> SizeOf(State) then Halt(5);
  BlockWrite(OutputFile, RetainedArgument, SizeOf(RetainedArgument), Actual);
  if Actual <> SizeOf(RetainedArgument) then Halt(5);
end;

begin
  { Oracle: actual wrappers; retained far argument is modeled, not native TP ABI. }
  if ParamCount <> 4 then Halt(2);
  Val(ParamStr(4), Kind, ParseError);
  if (ParseError <> 0) or (Kind > 1) then Halt(3);
  Assign(StateFile, ParamStr(1));
  Reset(StateFile, 1);
  if FileSize(StateFile) <> SizeOf(State) then Halt(4);
  BlockRead(StateFile, State, SizeOf(State), Actual);
  Close(StateFile);
  if Actual <> SizeOf(State) then Halt(4);
  Move(State.ObjectData[0], HandleValue, 2);
  Move(State.ObjectData[22], LieroBufferCodeSegment, 2);
  Assign(InputFile, ParamStr(2));
  Reset(InputFile, 1);
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  LieroBufferObject := @State.ObjectData[0];
  LieroBufferSource := @State.ObjectData[128];
  LieroBufferDestination := @State.Destination[0];
  LieroBufferDosRead := ReadInput;
  LieroBufferObjectOffset := $FEFA;
  RegisterES := LieroBufferCodeSegment;
  RegisterBX := LieroBufferObjectOffset;
  GlobalWord6410 := 0;
  OptionalReturn := 0;
  if Kind = 1 then OptionalReturn := $1234;
  LieroDispatchMethod := ResolveOptionalMethod;
  RetainedArgument.ObjectOffset := LieroBufferObjectOffset;
  RetainedArgument.ObjectSegment := LieroBufferCodeSegment;
  RetainedArgument.Active := 0;
  for Step := 0 to 3 do
  begin
    if Step mod 2 = 0 then
    begin
      if RetainedArgument.Active <> 0 then Halt(9);
      RetainedArgument.Active := 1;
      FUN_24dd_3988(255, @State.Destination[0], LieroBufferObject);
    end
    else
    begin
      if (RetainedArgument.Active <> 1) or
         (RetainedObject <> LieroBufferObject) then Halt(10);
      FUN_24dd_38f0(RetainedObject);
      RetainedArgument.Active := 0;
    end;
    CaptureWrapperState;
    if Step mod 2 = 0 then RetainedObject := LieroBufferObject;
  end;
  Close(OutputFile);
  Close(InputFile);
end.
