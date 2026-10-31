procedure FUN_24dd_05e8;
begin
  RegisterAX := $05DC;
  CopyCodeWordsToESDI;
  RegisterAX := (RegisterAX + 12) and $FFFF;
end;
