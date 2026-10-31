{ liero::FUN_24dd_04ed — modeled XCHG at DS:$6410
  (oracle: none; behavior is not yet verified against the original executable). }
function FUN_24dd_04ed: Word;
begin
  FUN_24dd_04ed := GlobalWord6410;
  GlobalWord6410 := 0;
end;
