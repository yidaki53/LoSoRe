{ Oracle: input-mode-only original-vs-host Pascal setup parity.
  Original entry 24DD:420C, RETF 4. Output modes remain unresolved and abort.
  Empty filename skips DOS open and leaves the initially cleared handle zero. }
type
  TLieroDosOpenInput = function(filename: Pointer; var handle: Word): Word;

function FUN_24dd_420c(objectPointer: Pointer; codeSegment: Word;
                       dosOpen: TLieroDosOpenInput): Word;
var
  objectWords: ^Word;
  filename: PByte;
  handle, status: Word;
begin
  objectWords := objectPointer;
  Inc(objectWords);
  if objectWords^ <> $D7B1 then
    RunError(211);
  objectWords := objectPointer;
  objectWords^ := 0;
  filename := PByte(objectPointer) + $30;
  handle := 0;
  if filename^ <> 0 then
  begin
    status := dosOpen(filename, handle);
    if status <> 0 then
    begin
      FUN_24dd_420c := status;
      Exit;
    end;
  end;
  objectWords^ := handle;
  Inc(objectWords, 10);
  objectWords^ := $375E;
  Inc(objectWords);
  objectWords^ := codeSegment;
  Inc(objectWords);
  objectWords^ := 0;
  Inc(objectWords);
  objectWords^ := 0;
  Inc(objectWords);
  objectWords^ := $37D3;
  Inc(objectWords);
  objectWords^ := codeSegment;
  FUN_24dd_420c := 0;
end;
