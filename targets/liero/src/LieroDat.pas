unit LieroDat;

{$MODE TP}

interface

const
  DAT_SIZE = $9B;
  WEAPON_COUNT = 5;

type
  TDatBytes = array[0..DAT_SIZE - 1] of Byte;
  TWeaponSettings = array[0..WEAPON_COUNT - 1] of Byte;
  TDatSettings = record
    RawBytes: TDatBytes;
    MaxBonuses: Byte;
    LoadingTimes: Word;
    Lives: SmallInt;
    GameMode: Byte;
    WeaponsP1: TWeaponSettings;
    WeaponsP2: TWeaponSettings;
    HealthP1: SmallInt;
    HealthP2: SmallInt;
  end;

procedure ParseDat(const Bytes: TDatBytes; var Settings: TDatSettings);
procedure SerializeDat(const Settings: TDatSettings; var Bytes: TDatBytes);

implementation

function ReadWordLE(const Bytes: TDatBytes; Offset: Word): Word;
begin
  ReadWordLE := Bytes[Offset] + (Word(Bytes[Offset + 1]) shl 8);
end;

function ReadSignedLE(const Bytes: TDatBytes; Offset: Word): SmallInt;
begin
  ReadSignedLE := SmallInt(ReadWordLE(Bytes, Offset));
end;

procedure WriteWordLE(Value: Word; Offset: Word; var Bytes: TDatBytes);
begin
  Bytes[Offset] := Byte(Value and $FF);
  Bytes[Offset + 1] := Byte(Value shr 8);
end;

procedure CopyWeapons(const Bytes: TDatBytes; Offset: Word;
  var Weapons: TWeaponSettings);
var
  Index: Integer;
begin
  for Index := 0 to WEAPON_COUNT - 1 do
    Weapons[Index] := Bytes[Offset + Index];
end;

procedure WriteWeapons(const Weapons: TWeaponSettings; Offset: Word;
  var Bytes: TDatBytes);
var
  Index: Integer;
begin
  for Index := 0 to WEAPON_COUNT - 1 do
    Bytes[Offset + Index] := Weapons[Index];
end;

procedure ParseDat(const Bytes: TDatBytes; var Settings: TDatSettings);
begin
  Settings.RawBytes := Bytes;
  Settings.MaxBonuses := Bytes[$00];
  Settings.LoadingTimes := ReadWordLE(Bytes, $01);
  Settings.Lives := ReadSignedLE(Bytes, $03);
  Settings.GameMode := Bytes[$10];
  CopyWeapons(Bytes, $42, Settings.WeaponsP1);
  CopyWeapons(Bytes, $47, Settings.WeaponsP2);
  Settings.HealthP1 := ReadSignedLE(Bytes, $4C);
  Settings.HealthP2 := ReadSignedLE(Bytes, $4E);
end;

procedure SerializeDat(const Settings: TDatSettings; var Bytes: TDatBytes);
begin
  Bytes := Settings.RawBytes;
  Bytes[$00] := Settings.MaxBonuses;
  WriteWordLE(Settings.LoadingTimes, $01, Bytes);
  WriteWordLE(Word(Settings.Lives), $03, Bytes);
  Bytes[$10] := Settings.GameMode;
  WriteWeapons(Settings.WeaponsP1, $42, Bytes);
  WriteWeapons(Settings.WeaponsP2, $47, Bytes);
  WriteWordLE(Word(Settings.HealthP1), $4C, Bytes);
  WriteWordLE(Word(Settings.HealthP2), $4E, Bytes);
end;

end.
