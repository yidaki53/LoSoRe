program LieroCompareCandidate;

{$MODE TP}

uses LieroRuntime;

const
  StringSize = 256;

type
  TCompareCase = packed record
    DestinationOffset: Word;
    SourceOffset: Word;
    Destination: array[0..StringSize - 1] of Byte;
    Source: array[0..StringSize - 1] of Byte;
  end;
  TCompareSnapshot = packed record
    Flags: Word;
    Destination: array[0..StringSize - 1] of Byte;
    Source: array[0..StringSize - 1] of Byte;
  end;

var
  InputFile: File;
  OutputFile: File;
  Fixture: TCompareCase;
  Snapshot: TCompareSnapshot;
  Segment: Word;
  ParseError: Integer;
  BytesRead: Integer;
  Index: Integer;
  Address: Longint;
  DestinationPointer: Longint;
  SourcePointer: Longint;
  DestinationArgument: Longint;
  SourceArgument: Longint;

{$I FUN_24dd_3f86.inc}

function PhysicalAddress(SegmentValue, OffsetValue: Word): Longint;
begin
  PhysicalAddress :=
    ((Longint(SegmentValue) shl 4) + OffsetValue) and $FFFFF;
end;

begin
  if ParamCount <> 3 then
    Halt(2);
  Val('$' + ParamStr(3), Segment, ParseError);
  if (ParseError <> 0) or (Segment = 0) then
    Halt(3);

  Assign(InputFile, ParamStr(1));
  Reset(InputFile, 1);
  Assign(OutputFile, ParamStr(2));
  Rewrite(OutputFile, 1);
  while True do
  begin
    BlockRead(InputFile, Fixture, SizeOf(Fixture), BytesRead);
    if BytesRead = 0 then
      Break;
    if BytesRead <> SizeOf(Fixture) then
      Halt(4);

    for Index := 0 to StringSize - 1 do
    begin
      Address := PhysicalAddress(Segment, Fixture.DestinationOffset + Index);
      RealModeMemory[Address] := Fixture.Destination[Index];
      Address := PhysicalAddress(Segment, Fixture.SourceOffset + Index);
      RealModeMemory[Address] := Fixture.Source[Index];
    end;

    DestinationPointer :=
      (Longint(Segment) shl 16) or Fixture.DestinationOffset;
    SourcePointer := (Longint(Segment) shl 16) or Fixture.SourceOffset;
    RegisterZeroFlag := False;
    RegisterCarryFlag := False;
    FUN_24dd_3f86(DestinationPointer, SourcePointer);

    Snapshot.Flags := 0;
    if RegisterZeroFlag then
      Snapshot.Flags := Snapshot.Flags or $0040;
    if RegisterCarryFlag then
      Snapshot.Flags := Snapshot.Flags or $0001;
    for Index := 0 to StringSize - 1 do
    begin
      DestinationPointer :=
        PhysicalAddress(Segment, Fixture.DestinationOffset + Index);
      SourcePointer := PhysicalAddress(Segment, Fixture.SourceOffset + Index);
      Snapshot.Destination[Index] := RealModeMemory[DestinationPointer];
      Snapshot.Source[Index] := RealModeMemory[SourcePointer];
    end;
    BlockWrite(OutputFile, Snapshot, SizeOf(Snapshot));
  end;
  Close(InputFile);
  Close(OutputFile);
end.
