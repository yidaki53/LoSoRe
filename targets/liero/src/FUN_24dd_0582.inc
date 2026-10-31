procedure FUN_24dd_0582;
begin
  RegisterAX := $0576;
  CopyCodeWordsToESDI;
  RegisterAX := (RegisterAX + 12) and $FFFF;
end;
