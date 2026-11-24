{ Oracle: isolated original-vs-host Pascal close parity with a DOS-close adapter.
  Original entry 24DD:37D3, RETF 4. Host callback/pointer are not the TP7 ABI. }
type
  TLieroDosClose = function(handle: Word): Word;

function FUN_24dd_37d3(objectPointer: Pointer; dosClose: TLieroDosClose): Word;
var
  objectWords: ^Word;
  handle: Word;
begin
  objectWords := objectPointer;
  handle := objectWords^;
  if handle <= 4 then
    FUN_24dd_37d3 := 0
  else
    FUN_24dd_37d3 := dosClose(handle);
end;
