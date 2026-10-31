{ Oracle: isolated original-vs-host Pascal refill parity with a DOS-read adapter.
  Original entry 24DD:375E, RETF 4. Host pointers/callback are not the TP7 ABI.
  bufferPointer must resolve the object's far pointer at +0C/+0E. }
type
  TLieroDosRead = function(handle, count: Word; destination: Pointer;
                          var bytesRead: Word): Word;

function FUN_24dd_375e(objectPointer, bufferPointer: Pointer;
                       dosRead: TLieroDosRead): Word;
var
  objectWords: ^Word;
  handle, capacity, bytesRead, status: Word;
begin
  objectWords := objectPointer;
  handle := objectWords^;
  Inc(objectWords, 2);
  capacity := objectWords^;
  status := dosRead(handle, capacity, bufferPointer, bytesRead);
  Inc(objectWords, 2);
  objectWords^ := 0;
  Inc(objectWords);
  if status = 0 then
    objectWords^ := bytesRead
  else
    objectWords^ := 0;
  FUN_24dd_375e := status;
end;
