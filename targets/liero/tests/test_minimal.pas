program TestOneFunc;

{$MODE TP}

uses LieroRuntime;

{$I ../src/FUN_24dd_04dc.inc}

var
  result_val: LongInt;

begin
  { Test FUN_24dd_04dc - 16-bit AX/DX arithmetic helper }
  { This function takes no parameters and returns a Longint }
  result_val := FUN_24dd_04dc;
  { If we get here, the function compiled and returned a value }
  Halt(0);
end.