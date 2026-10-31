program ProbeLieroSetupHandler;

{$MODE TP}

uses SysUtils
{$IFDEF OPEN_WRAPPER_PROBE}
  , LieroRuntime
{$ENDIF}
  ;

{$I FUN_24dd_420c.inc}
{$IFDEF OPEN_WRAPPER_PROBE}
{$I FUN_24dd_37d3.inc}
procedure FUN_24dd_374d; forward;
procedure FUN_24dd_3711(objectPointer: Pointer); forward;
procedure FUN_24dd_36c4(objectPointer: Pointer); forward;
procedure FUN_24dd_36b7(objectPointer: Pointer); forward;
procedure FUN_24dd_36bc(objectPointer: Pointer); forward;
{$I FUN_24dd_374d.inc}
{$I FUN_24dd_3711.inc}
{$I FUN_24dd_36c4.inc}
{$I FUN_24dd_36b7.inc}
{$I FUN_24dd_36bc.inc}
{$ENDIF}

type
  TState = packed record
    ObjectData: array[0..255] of Byte;
    Destination: array[0..255] of Byte;
  end;
var
  InputFile, StateFile, OutputFile: File;
  State: TState;
  Count: Longint;
  HandleValue, SegmentValue, Status, Marker, Kind, OpenCalls: Word;
  Step, Error: Integer;
  InputOpen: Boolean;
  BaseDirectory: String;

function OpenInput(filename: Pointer; var handle: Word): Word;
var
  name, path: String;
  cursor: PByte;
  error, savedFileMode: Integer;
begin
  { Oracle: actual host open, with missing-file/path mapped to observed DOSBox 2.
    A captured reusable DOS handle labels a successful host descriptor.
    Unexpected host I/O errors abort; this is not full DOS emulation. }
  Inc(OpenCalls);
  if InputOpen then
    Halt(7);
  name := '';
  cursor := filename;
  while (cursor^ <> 0) and (Length(name) < 79) do
  begin
    name := name + Chr(cursor^);
    Inc(cursor);
  end;
  path := BaseDirectory + '/' + name;
  if not DirectoryExists(ExtractFileDir(path)) then
  begin
    OpenInput := 2;
    Exit;
  end;
  if not FileExists(path) then
  begin
    OpenInput := 2;
    Exit;
  end;
  Assign(InputFile, path);
  savedFileMode := FileMode;
  FileMode := 0;
  {$I-}
  Reset(InputFile, 1);
  error := IOResult;
  {$I+}
  FileMode := savedFileMode;
  if error <> 0 then
    Halt(8);
  InputOpen := True;
  handle := HandleValue;
  OpenInput := 0;
end;

{$IFDEF OPEN_WRAPPER_PROBE}
function CloseInput(handle: Word): Word;
var
  error: Integer;
begin
  { Oracle: one captured DOS identity backed by a real host read-only file. }
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
  { Oracle: actual input setup/close bodies only; no guessed method outcomes. }
  if (objectSegment <> SegmentValue) or (objectOffset <> $FEFA) then
    Halt(9);
  if (slotOffset <> $10) and (slotOffset <> $1C) then
    Halt(10);
  Move(State.ObjectData[slotOffset], methodOffset, 2);
  Move(State.ObjectData[slotOffset + 2], methodSegment, 2);
  if methodSegment <> SegmentValue then
    Halt(11);
  if (slotOffset = $10) and (methodOffset = $420C) then
    InvokeMethod := FUN_24dd_420c(@State.ObjectData[0], SegmentValue, OpenInput)
  else if (slotOffset = $1C) and (methodOffset = $37D3) then
  begin
    Move(State.ObjectData[0], Marker, 2);
    InvokeMethod := FUN_24dd_37d3(@State.ObjectData[0], CloseInput);
    RegisterDX := $DEAD;
  end
  else
    Halt(12);
end;

procedure SetFilename(name: String);
var
  index: Integer;
begin
  { Oracle: match the explicit probe-only filename mutation, including unchanged tail. }
  FillChar(State.ObjectData[48], 80, 0);
  for index := 1 to Length(name) do
    State.ObjectData[47 + index] := Ord(name[index]);
end;
{$ENDIF}

begin
  { Oracle: scoped input setup body; original post-open state is fixture identity. }
  if ParamCount <> 4 then
    Halt(2);
  Val(ParamStr(4), Kind, Error);
  if (Error <> 0) or not (Kind in [0, 1, 2, 128]) then
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
  BaseDirectory := ExtractFileDir(ParamStr(2));
  InputOpen := False;
  OpenCalls := 0;
{$IFDEF OPEN_WRAPPER_PROBE}
  if OpenInput(@State.ObjectData[48], Marker) <> 0 then
    Halt(8);
  LieroDispatchMethod := InvokeMethod;
  GlobalWord6410 := $55AA;
{$ENDIF}
  Assign(OutputFile, ParamStr(3));
  Rewrite(OutputFile, 1);
  for Step := 3 to 10 do
  begin
{$IFDEF OPEN_WRAPPER_PROBE}
    if (Step = 4) or (Step = 7) then
    begin
      if CloseInput(HandleValue) <> 0 then
        Halt(8);
      FillChar(State.ObjectData[0], 2, $FF);
    end;
    if Step = 5 then
      SetFilename('MISSING.TXT');
    if Step = 6 then
      SetFilename('INPUT.TXT');
    if Step = 9 then
    begin
      Marker := $1234;
      Move(Marker, State.ObjectData[2], 2);
    end;
    if Step = 10 then
    begin
      Marker := $D7B0;
      Move(Marker, State.ObjectData[2], 2);
      SetFilename('');
    end;
    Marker := $55AA;
    Move(Marker, State.ObjectData[8], 2);
    FillChar(State.ObjectData[10], 2, $FF);
    RegisterES := SegmentValue;
    RegisterDI := $FEFA;
    if (Step = 7) or (Step = 8) then
      FUN_24dd_3711(@State.ObjectData[0])
    else
      FUN_24dd_36b7(@State.ObjectData[0]);
    Status := GlobalWord6410;
{$ELSE}
    Marker := $BEEF;
    Move(Marker, State.ObjectData[0], 2);
    Marker := $55AA;
    Move(Marker, State.ObjectData[8], 2);
    FillChar(State.ObjectData[10], 2, $FF);
    FillChar(State.ObjectData[20], 12, $A5);
    Status := FUN_24dd_420c(@State.ObjectData[0], SegmentValue, OpenInput);
    Move(OpenCalls, State.Destination[0], 2);
{$ENDIF}
    BlockWrite(OutputFile, Status, 2, Count);
    if Count <> 2 then
      Halt(5);
    BlockWrite(OutputFile, State, SizeOf(State), Count);
    if Count <> SizeOf(State) then
      Halt(5);
{$IFNDEF OPEN_WRAPPER_PROBE}
    if InputOpen then
    begin
      {$I-}
      Close(InputFile);
      Error := IOResult;
      {$I+}
      if Error <> 0 then
        Halt(8);
      InputOpen := False;
    end;
{$ENDIF}
  end;
  Close(OutputFile);
{$IFDEF OPEN_WRAPPER_PROBE}
  if InputOpen then
    if CloseInput(HandleValue) <> 0 then
      Halt(8);
{$ENDIF}
end.
