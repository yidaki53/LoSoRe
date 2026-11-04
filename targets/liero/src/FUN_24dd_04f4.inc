{ Oracle: original04f4 zero return or checked nonreturning010f error scope.
  Unknown cleanup chains/targets still reject. Original assembly retained. }
procedure FUN_24dd_04f4;
begin
  if GlobalWord6410 <> 0 then begin
    RegisterAX := GlobalWord6410;
    FUN_24dd_010f;
    RunError(211);
  end;
  RegisterCarryFlag := False;
  RegisterZeroFlag := True;
  RegisterSP := (LongInt(RegisterSP) + 4) and $FFFF;
end;
