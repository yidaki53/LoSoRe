program ProbeLieroConstructor;

{$MODE TP}

uses LieroRuntime;

{$I FUN_24dd_3639.inc}

type
  TCase = packed record
    Name: array[0..255] of Byte;
    Arena: array[0..287] of Byte;
  end;
var
  InputFile, OutputFile: File;
  TestCase: TCase;
  Count: Longint;
  SegmentValue: Word;
  ErrorCode: Integer;
begin
  { Oracle: actual reconstructed Pascal body; no independently rewritten constructor. }
  if ParamCount <> 3 then
    Halt(2);
  Val(ParamStr(3), SegmentValue, ErrorCode);
  if ErrorCode <> 0 then
    Halt(3);
  Assign(InputFile, ParamStr(1));
  Reset(InputFile, 1);
  Assign(OutputFile, ParamStr(2));
  Rewrite(OutputFile, 1);
  while not Eof(InputFile) do
  begin
    BlockRead(InputFile, TestCase, SizeOf(TestCase), Count);
    if Count <> SizeOf(TestCase) then
      Halt(4);
    RegisterES := SegmentValue;
    RegisterDI := $6910;
    FUN_24dd_3639(@TestCase.Name[0], @TestCase.Arena[16]);
    BlockWrite(OutputFile, TestCase, SizeOf(TestCase), Count);
    if Count <> SizeOf(TestCase) then
      Halt(5);
  end;
  Close(InputFile);
  Close(OutputFile);
end.
