{ Oracle: original-byte DOS-write service boundary and scoped adapter parity.
  Alternate entry 24DD:37B3 inside the original file-service region, RETF 4.
  objectPointer resolves ES:DI; bufferPointer resolves its far pointer at +12.
  Owned nonaliasing object/buffer/stack and readable count bytes are required.
  The service sees used=0 before it runs, even on failure. Successful short
  writes return zero, unlike 378E. Host pointers/callback are not native TP7
  ABI; other DOS register/flag/device effects remain external obligations.
  Original bytes remain assembly residue; no whole-source promotion. }
type
  TLieroDosWrite = function(handle, count: Word; source: Pointer;
                           var bytesWritten: Word): Word;

function FUN_24dd_37b3(objectPointer, bufferPointer: Pointer;
                      dosWrite: TLieroDosWrite): Word;
var
  objectWords: ^Word;
  handle, count, bytesWritten: Word;
begin
  if (objectPointer = nil) or (bufferPointer = nil) or
     not Assigned(dosWrite) then
    RunError(211);
  objectWords := objectPointer;
  handle := objectWords^;
  Inc(objectWords, 4);
  count := objectWords^;
  objectWords^ := 0;
  FUN_24dd_37b3 := dosWrite(handle, count, bufferPointer, bytesWritten);
end;
