program TestLieroDat;

{$MODE TP}

uses
  LieroDat;

var
  OriginalBytes: TDatBytes;
  SerializedBytes: TDatBytes;
  Settings: TDatSettings;
  Index: Integer;
begin
  for Index := 0 to DAT_SIZE - 1 do
    OriginalBytes[Index] := Byte((Index * 37 + 11) mod 256);

  ParseDat(OriginalBytes, Settings);
  if Settings.MaxBonuses <> 11 then Halt(1);
  if Settings.LoadingTimes <> 21808 then Halt(2);
  if Settings.GameMode <> OriginalBytes[$10] then Halt(3);
  if Settings.WeaponsP1[0] <> OriginalBytes[$42] then Halt(4);
  if Settings.WeaponsP2[4] <> OriginalBytes[$4B] then Halt(5);

  SerializeDat(Settings, SerializedBytes);
  for Index := 0 to DAT_SIZE - 1 do
    if SerializedBytes[Index] <> OriginalBytes[Index] then Halt(6);

  Inc(Settings.Lives);
  SerializeDat(Settings, SerializedBytes);
  if (SerializedBytes[$03] = OriginalBytes[$03]) and
    (SerializedBytes[$04] = OriginalBytes[$04]) then Halt(7);
  for Index := 0 to DAT_SIZE - 1 do
    if ((Index < $03) or (Index > $04)) and
      (SerializedBytes[Index] <> OriginalBytes[Index]) then Halt(8);

  WriteLn('Liero DAT parse/edit/serialize: PASS');
end.
