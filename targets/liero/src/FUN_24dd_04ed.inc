{ liero::FUN_24dd_04ed — take and clear the logical DS:$6410 error word.
  Oracle: complete original-byte review and exhaustive actual-source comparison.
  Requires the logical global mirror and no concurrent cell mutation;
  native memory-XCHG atomicity and host ABI are not modeled. }
function FUN_24dd_04ed: Word;
begin
  RegisterAX := GlobalWord6410;
  GlobalWord6410 := 0;
  RegisterCarryFlag := False;
  RegisterZeroFlag := True;
  FUN_24dd_04ed := RegisterAX;
end;
