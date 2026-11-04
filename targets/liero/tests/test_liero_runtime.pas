program TestLieroRuntime;

{$MODE TP}

uses LieroRuntime;

{$I ../src/FUN_1ea2_01f0.inc}
{$I ../src/FUN_1ea2_01a8.inc}
{$I ../src/FUN_24dd_04ed.inc}
{$I ../src/FUN_24dd_0530.inc}
{$I ../src/FUN_24dd_00b1.inc}
{$I ../src/FUN_24dd_1ee4.inc}
{$I ../src/FUN_24dd_0232.inc}
{$I ../src/FUN_24dd_020a.inc}
{$I ../src/FUN_24dd_022a.inc}
{$I ../src/FUN_24dd_021f.inc}
{$I ../src/FUN_24dd_0218.inc}
{$I ../src/FUN_24dd_01fe.inc}
{$I ../src/FUN_24dd_4732.inc}
{$I ../src/FUN_24dd_4712.inc}
{$I ../src/FUN_24dd_4824.inc}
{$I ../src/FUN_24dd_02cb.inc}
{$I ../src/FUN_24dd_02b9.inc}
{$I ../src/FUN_24dd_0628.inc}
{$I ../src/FUN_24dd_0673.inc}
{$I ../src/FUN_24dd_3c03.inc}
{$I ../src/FUN_24dd_3639.inc}
{$I ../src/FUN_24dd_0582.inc}
{$I ../src/FUN_24dd_05e8.inc}
{$I ../src/FUN_24dd_05fd.inc}
{$I ../src/FUN_24dd_0642.inc}
{$I ../src/FUN_235c_135f.inc}
{$I ../src/FUN_235c_06d7.inc}
{$I ../src/FUN_235c_091d.inc}
{$I ../src/FUN_235c_0aad.inc}
{$I ../src/FUN_235c_0ad3.inc}
{$I ../src/FUN_235c_11aa.inc}
{$I ../src/FUN_235c_0b7c.inc}
{$I ../src/FUN_235c_0a1e.inc}
{$I ../src/FUN_235c_0aeb.inc}
{$I ../src/FUN_235c_095c.inc}
{$I ../src/FUN_235c_09eb.inc}
{$I ../src/FUN_235c_0a51.inc}
{$I ../src/FUN_235c_118c.inc}
{$I ../src/FUN_1ec2_0d5d.inc}
{$I ../src/FUN_1ec2_0d88.inc}
{$I ../src/FUN_1ec2_0e8f.inc}
{$I ../src/FUN_1ec2_1008.inc}
{$I ../src/FUN_1ec2_0f44.inc}
{$I ../src/FUN_1ec2_12e6.inc}
{$I ../src/FUN_1ec2_10cf.inc}
{$I ../src/FUN_1ec2_0810.inc}
{$I ../src/FUN_1ec2_152f.inc}
{$I ../src/FUN_1ec2_15bb.inc}
{$I ../src/FUN_1ec2_155e.inc}
{$I ../src/FUN_1ec2_10ea.inc}
{$I ../src/FUN_1ec2_11b5.inc}
{$I ../src/FUN_1ec2_0dc8.inc}
{$I ../src/FUN_1ec2_0e06.inc}
{$I ../src/FUN_1ec2_0e4a.inc}
{$I ../src/FUN_1ec2_0734.inc}
{$I ../src/FUN_1ec2_01df.inc}
{$I ../src/FUN_1ec2_0386.inc}
{$I ../src/FUN_1ec2_12ad.inc}
{$I ../src/FUN_1ec2_0000.inc}
{$I ../src/FUN_1ec2_13b0.inc}
{$I ../src/FUN_1ec2_00a5.inc}
{$I ../src/FUN_1ec2_13d3.inc}
{$I ../src/FUN_1ec2_13a4.inc}
{$I ../src/FUN_1ec2_13c5.inc}
{$I ../src/FUN_24dd_04dc.inc}
{$I ../src/FUN_1ec2_086b.inc}
{$I ../src/FUN_1ec2_09bd.inc}
{$I ../src/FUN_1ec2_0ae3.inc}
{$I ../src/FUN_1ec2_0b0d.inc}
{$I ../src/FUN_1ec2_0c11.inc}
{$I ../src/FUN_1ec2_0c3b.inc}
{$I ../src/FUN_1ec2_09e7.inc}
{$I ../src/FUN_24dd_4919.inc}
{$I ../src/FUN_24dd_40d6.inc}
{$I ../src/FUN_24dd_3d68.inc}
{$I ../src/FUN_24dd_4905.inc}
{$I ../src/FUN_24dd_492c.inc}
{$I ../src/FUN_235c_04f3.inc}
{$I ../src/FUN_24dd_3e63.inc}
{$I ../src/FUN_24dd_3e7c.inc}
{$I ../src/FUN_24dd_3e95.inc}
{$I ../src/FUN_24dd_3eaf.inc}
{$I ../src/FUN_235c_04bc.inc}
{$I ../src/FUN_24dd_3ed3.inc}
{$I ../src/FUN_24dd_3fb1.inc}
{$I ../src/FUN_24dd_3fc3.inc}
{$I ../src/FUN_24dd_3f14.inc}
{$I ../src/FUN_24dd_40ac.inc}
{$I ../src/FUN_24dd_4161.inc}
{$I ../src/FUN_24dd_4181.inc}
{$I ../src/FUN_24dd_40ec.inc}
{$I ../src/FUN_24dd_350e.inc}
{$I ../src/FUN_24dd_3b22.inc}
{$I ../src/FUN_24dd_3d36.inc}
{$I ../src/FUN_24dd_3d2f.inc}
{$I ../src/FUN_24dd_3d80.inc}
{$I ../src/FUN_24dd_3f40.inc}
{$I ../src/FUN_24dd_3f86.inc}
{$I ../src/FUN_24dd_3dbd.inc}
{$I ../src/FUN_24dd_46b1.inc}
{$I ../src/FUN_24dd_4654.inc}
{$I ../src/FUN_1000_5e66.inc}
{$I ../src/FUN_1000_0961.inc}
{$I ../src/FUN_249c_0013.inc}
{$I ../src/FUN_249c_0000.inc}

var
  sourceBuffer: array[0..7] of Byte;
  destinationBuffer: array[0..7] of Byte;
  wordBuffer: array[0..17] of Word;
  orSourceWords: array[0..15] of Word;
  realModeAddress: Longint;
  sourceFarAddress: Longint;
  destinationFarAddress: Longint;
  searchResult: Word;
  builderIndex: Integer;
  commandLineSegment: Word;
  wordIndex: Integer;
  copySourceBuffer: array[0..7] of Byte;
  copyDestinationBuffer: array[0..7] of Byte;
  countedSourceBuffer: array[0..255] of Byte;
  countedDestinationBuffer: array[0..256] of Byte;
  longStringBuffer: array[0..511] of Byte;
  formattedBuffer: array[0..33] of Byte;
  fillBuffer: array[0..258] of Byte;
  largeFillBuffer: array[0..65536] of Byte;
  sourceFrameBuffer: array[0..63999] of Byte;
  destinationFrameBuffer: array[0..63999] of Byte;
  clearFrameBuffer: array[0..63999] of Byte;
  farPointerValue: packed record
    Offset: Word;
    Segment: Word;
  end;
  sourceName: array[0..80] of Byte;
  paletteBytes: array[0..767] of Byte;
  fileControlRecord: array[0..127] of Byte;
  shiftCases: array[0..5] of Word;
  index: Longint;
  shiftIndex: Integer;
  cpuIndex: Integer;
  expectedAX: Word;
  expectedDX: Word;
  addCarry: Boolean;
  expectedDirectionFlag: Boolean;
  actualWord: Word;
  expectedByte: Byte;
  playerRecordAddress: Longint;
  actualLong: LongInt;
  backgroundPhysical: Longint;
  backgroundRow: Integer;
  backgroundColumn: Integer;
  backgroundOffset: Word;
  backgroundSegment: Word;
  mapColumn: Integer;
  mapRow: Integer;
  mapTablePhysical: Longint;
  mapGridPhysical: Longint;
begin
  RegisterES := 0;
  RegisterDI := $0500;
  RegisterCX := 4;
  DosMemory[$0500] := Ord('1');
  DosMemory[$0501] := Ord('2');
  DosMemory[$0502] := Ord('3');
  DosMemory[$0503] := Ord('4');
  if FUN_24dd_4732 <> 1234 then
    Halt(176);
  RegisterDI := $0510;
  RegisterCX := 3;
  DosMemory[$0510] := Ord('$');
  DosMemory[$0511] := Ord('2');
  DosMemory[$0512] := Ord('A');
  if FUN_24dd_4732 <> 42 then
    Halt(177);
  sourceName[0] := 2;
  sourceName[1] := Ord('4');
  sourceName[2] := Ord('2');
  wordBuffer[0] := $FFFF;
  if FUN_24dd_4824(@wordBuffer[0], @sourceName[0]) <> 42 then
    Halt(181);
  if wordBuffer[0] <> 0 then
    Halt(182);
  sourceName[1] := Ord('4');
  sourceName[2] := Ord('x');
  wordBuffer[0] := $FFFF;
  if FUN_24dd_4824(@wordBuffer[0], @sourceName[0]) <> 0 then
    Halt(183);
  if wordBuffer[0] <> 2 then
    Halt(184);
  RegisterES := 0;
  RegisterAX := $1234;
  RegisterBX := 0;
  RegisterSI := 16;
  RegisterDI := $0604;
  FUN_24dd_4712;
  if (DosMemory[$0600] <> Ord('1')) or
     (DosMemory[$0601] <> Ord('2')) or
     (DosMemory[$0602] <> Ord('3')) or
     (DosMemory[$0603] <> Ord('4')) then
    Halt(178);

  DosMemory[$6420] := 0;
  FUN_24dd_00b1;
  if DosMemory[$6420] <> 2 then
    Halt(170);
  RegisterBX := $0103;
  RegisterCarryFlag := True;
  DosMemory[$0161] := $20;
  FUN_24dd_1ee4;
  if DosMemory[$0161] <> $1C then
    Halt(171);
  RegisterBX := $0000;
  RegisterCarryFlag := False;
  sourceName[0] := 3;
  sourceName[1] := Ord('L');
  sourceName[2] := Ord('I');
  sourceName[3] := Ord('E');
  DosMemory[$7690] := 0;
  FUN_235c_04bc(@sourceName[0]);
  if (DosMemory[$7690] <> 1) or (DosMemory[$7692] <> 3) or
     (DosMemory[$7693] <> Ord('L')) or (DosMemory[$7694] <> Ord('I')) or
     (DosMemory[$7695] <> Ord('E')) then
    Halt(172);

  for index := 0 to 255 do
  begin
    expectedByte := Byte(index);
    if (index >= $61) and (index <= $7A) then
      expectedByte := expectedByte - $20;
    if FUN_24dd_4919(Byte(index)) <> expectedByte then
      Halt(38);
  end;

  shiftCases[0] := 0;
  shiftCases[1] := 1;
  shiftCases[2] := 16;
  shiftCases[3] := 31;
  shiftCases[4] := 32;
  shiftCases[5] := $FF1F;
  for cpuIndex := 0 to 2 do
  begin
    DosMemory[$6420] := cpuIndex;
    for shiftIndex := 0 to 5 do
    begin
      RegisterDX := $8123;
      RegisterAX := $4567;
      RegisterCX := shiftCases[shiftIndex];
      case shiftCases[shiftIndex] of
        0, 32:
          begin
            expectedDX := $8123;
            expectedAX := $4567;
          end;
        1:
          begin
            expectedDX := $4091;
            expectedAX := $A2B3;
          end;
        16:
          begin
            expectedDX := 0;
            expectedAX := $8123;
          end;
        31, $FF1F:
          begin
            expectedDX := 0;
            expectedAX := 1;
          end;
      end;
      if FUN_24dd_3e63 <> expectedAX then
        Halt(55);
      if (RegisterDX <> expectedDX) or (RegisterAX <> expectedAX) then
        Halt(56);

      RegisterDX := $8123;
      RegisterAX := $4567;
      RegisterCX := shiftCases[shiftIndex];
      case shiftCases[shiftIndex] of
        0, 32:
          begin
            expectedDX := $8123;
            expectedAX := $4567;
          end;
        1:
          begin
            expectedDX := $0246;
            expectedAX := $8ACE;
          end;
        16:
          begin
            expectedDX := $4567;
            expectedAX := 0;
          end;
        31, $FF1F:
          begin
            expectedDX := $8000;
            expectedAX := 0;
          end;
      end;
      if Word(FUN_24dd_3e7c) <> expectedAX then
        Halt(57);
      if (RegisterDX <> expectedDX) or (RegisterAX <> expectedAX) then
        Halt(58);
    end;
  end;

  for index := 0 to 16 do
    wordBuffer[index] := $FFFF;
  FUN_24dd_40d6($A55A, @wordBuffer[1]);
  if wordBuffer[0] <> $FFFF then
    Halt(39);
  if wordBuffer[1] <> $A55A then
    Halt(40);
  for index := 2 to 16 do
    if wordBuffer[index] <> 0 then
      Halt(41);

  for index := 0 to 7 do
  begin
    copySourceBuffer[index] := index;
    copyDestinationBuffer[index] := $FF;
  end;
  FUN_24dd_3d68(0, @copyDestinationBuffer[0], @copySourceBuffer[0]);
  for index := 0 to 7 do
    if copyDestinationBuffer[index] <> $FF then
      Halt(42);
  FUN_24dd_3d68(6, @copyDestinationBuffer[0], @copySourceBuffer[0]);
  for index := 0 to 5 do
    if copyDestinationBuffer[index] <> index then
      Halt(43);
  for index := 6 to 7 do
    if copyDestinationBuffer[index] <> $FF then
      Halt(44);

  sourceName[0] := 3;
  sourceName[1] := Ord('A');
  sourceName[2] := Ord('B');
  sourceName[3] := Ord('C');
  sourceName[4] := Ord('D');
  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3e95(@sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 3) or
     (copyDestinationBuffer[1] <> Ord('A')) or
     (copyDestinationBuffer[2] <> Ord('B')) or
     (copyDestinationBuffer[3] <> Ord('C')) or
     (copyDestinationBuffer[4] <> $FF) then
    Halt(59);

  sourceName[0] := 5;
  sourceName[1] := Ord('A');
  sourceName[2] := Ord('B');
  sourceName[3] := Ord('C');
  sourceName[4] := Ord('D');
  sourceName[5] := Ord('E');
  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3eaf(3, @copyDestinationBuffer[0], @sourceName[0]);
  if (copyDestinationBuffer[0] <> 3) or
     (copyDestinationBuffer[1] <> Ord('A')) or
     (copyDestinationBuffer[2] <> Ord('B')) or
     (copyDestinationBuffer[3] <> Ord('C')) or
     (copyDestinationBuffer[4] <> $FF) then
    Halt(60);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3eaf(7, @copyDestinationBuffer[0], @sourceName[0]);
  if (copyDestinationBuffer[0] <> 5) or
     (copyDestinationBuffer[1] <> Ord('A')) or
     (copyDestinationBuffer[2] <> Ord('B')) or
     (copyDestinationBuffer[3] <> Ord('C')) or
     (copyDestinationBuffer[4] <> Ord('D')) or
     (copyDestinationBuffer[5] <> Ord('E')) or
     (copyDestinationBuffer[6] <> $FF) then
    Halt(61);

  sourceName[0] := 5;
  sourceName[1] := Ord('A');
  sourceName[2] := Ord('B');
  sourceName[3] := Ord('C');
  sourceName[4] := Ord('D');
  sourceName[5] := Ord('E');
  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3ed3(3, 2, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 3) or
     (copyDestinationBuffer[1] <> Ord('B')) or
     (copyDestinationBuffer[2] <> Ord('C')) or
     (copyDestinationBuffer[3] <> Ord('D')) or
     (copyDestinationBuffer[4] <> $FF) then
    Halt(62);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3ed3(9, 5, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 1) or
     (copyDestinationBuffer[1] <> Ord('E')) or
     (copyDestinationBuffer[2] <> $FF) then
    Halt(63);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3ed3(4, 6, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 0) or
     (copyDestinationBuffer[1] <> $FF) then
    Halt(64);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3ed3(2, 0, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 2) or
     (copyDestinationBuffer[1] <> Ord('A')) or
     (copyDestinationBuffer[2] <> Ord('B')) or
     (copyDestinationBuffer[3] <> $FF) then
    Halt(65);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3ed3($FFFF, 2, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 0) or
     (copyDestinationBuffer[1] <> $FF) then
    Halt(66);

  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3fb1($5A, @copyDestinationBuffer[1]);
  if (copyDestinationBuffer[0] <> $FF) or
     (copyDestinationBuffer[1] <> 1) or
     (copyDestinationBuffer[2] <> $5A) or
     (copyDestinationBuffer[3] <> $FF) then
    Halt(67);

  sourceName[0] := Ord('X');
  sourceName[1] := Ord('Y');
  sourceName[2] := Ord('Z');
  for index := 0 to 7 do
    copyDestinationBuffer[index] := $FF;
  FUN_24dd_3fc3(3, @sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 3) or
     (copyDestinationBuffer[1] <> Ord('X')) or
     (copyDestinationBuffer[2] <> Ord('Y')) or
     (copyDestinationBuffer[3] <> Ord('Z')) or
     (copyDestinationBuffer[4] <> $FF) then
    Halt(68);

  for index := 0 to 255 do
  begin
    countedSourceBuffer[index] := Byte(index);
    countedDestinationBuffer[index] := $FF;
  end;
  countedDestinationBuffer[256] := $FF;
  FUN_24dd_3fc3(256, @countedSourceBuffer[0], @countedDestinationBuffer[0]);
  if countedDestinationBuffer[0] <> 0 then
    Halt(69);
  for index := 0 to 255 do
    if countedDestinationBuffer[index + 1] <> Byte(index) then
      Halt(70);
  if countedDestinationBuffer[256] <> $FF then
    Halt(71);
  copyDestinationBuffer[0] := $FF;
  copyDestinationBuffer[1] := $A5;
  FUN_24dd_3fc3(0, @countedSourceBuffer[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 0) or
     (copyDestinationBuffer[1] <> $A5) then
    Halt(86);

  sourceName[0] := 2;
  sourceName[1] := Ord('X');
  sourceName[2] := Ord('Y');
  copyDestinationBuffer[0] := 2;
  copyDestinationBuffer[1] := Ord('A');
  copyDestinationBuffer[2] := Ord('B');
  copyDestinationBuffer[3] := $FF;
  FUN_24dd_3f14(@sourceName[0], @copyDestinationBuffer[0]);
  if (copyDestinationBuffer[0] <> 4) or
     (copyDestinationBuffer[1] <> Ord('A')) or
     (copyDestinationBuffer[2] <> Ord('B')) or
     (copyDestinationBuffer[3] <> Ord('X')) or
     (copyDestinationBuffer[4] <> Ord('Y')) then
    Halt(72);

  sourceName[0] := 3;
  sourceName[1] := Ord('X');
  sourceName[2] := Ord('Y');
  sourceName[3] := Ord('Z');
  for index := 0 to 511 do
    longStringBuffer[index] := $FF;
  longStringBuffer[0] := 254;
  FUN_24dd_3f14(@sourceName[0], @longStringBuffer[0]);
  if (longStringBuffer[0] <> 255) or
     (longStringBuffer[255] <> Ord('X')) or
     (longStringBuffer[256] <> $FF) then
    Halt(73);

  sourceName[0] := Ord('A');
  sourceName[1] := Ord('B');
  sourceName[2] := Ord('C');
  for index := 0 to 33 do
    formattedBuffer[index] := $FF;
  FUN_24dd_40ac($0203, @sourceName[0], @formattedBuffer[1]);
  if (formattedBuffer[0] <> $FF) or (formattedBuffer[1] <> 0) or
     (formattedBuffer[2] <> 0) or (formattedBuffer[3] <> Ord('A')) or
     (formattedBuffer[4] <> Ord('B')) or (formattedBuffer[5] <> Ord('C')) then
    Halt(74);
  for index := 6 to 32 do
    if formattedBuffer[index] <> 0 then
      Halt(75);
  if formattedBuffer[33] <> $FF then
    Halt(76);
  for index := 0 to 33 do
    formattedBuffer[index] := $FF;
  FUN_24dd_40ac(0, @sourceName[0], @formattedBuffer[1]);
  for index := 1 to 32 do
    if formattedBuffer[index] <> 0 then
      Halt(87);
  if (formattedBuffer[0] <> $FF) or (formattedBuffer[33] <> $FF) then
    Halt(88);

  wordBuffer[0] := $A55A;
  wordBuffer[17] := $5AA5;
  for index := 0 to 15 do
  begin
    wordBuffer[index + 1] := $00F0 + index;
    orSourceWords[index] := $0F00 + index;
  end;
  FUN_24dd_4181(@orSourceWords[0], @wordBuffer[1]);
  if (wordBuffer[0] <> $A55A) or (wordBuffer[17] <> $5AA5) then
    Halt(78);
  for index := 0 to 15 do
    if wordBuffer[index + 1] <> (($00F0 + index) or ($0F00 + index)) then
      Halt(79);

  RegisterAX := $5A23;
  RegisterDX := $020A;
  if Word(FUN_24dd_4161) <> $5AD2 then
    Halt(80);
  if (RegisterDX <> $0002) or (RegisterCX <> $0203) then
    Halt(81);
  RegisterAX := $0020;
  RegisterDX := $0004;
  if Word(FUN_24dd_4161) <> 0 then
    Halt(82);
  if (RegisterDX <> 0) or (RegisterCX <> $0403) then
    Halt(83);
  RegisterAX := $8001;
  RegisterDX := $010A;
  if Word(FUN_24dd_4161) <> $FFFF then
    Halt(84);
  if (RegisterDX <> 0) or (RegisterCX <> $FF03) then
    Halt(85);

  RegisterSP := $FFF0;
  DosMemory[$640E] := 0;
  DosMemory[$640F] := 0;
  DosMemory[$669C] := 0;
  for index := $6604 to $6623 do
    DosMemory[index] := 0;
  for index := $14C0 to $14DF do
    DosMemory[index] := 0;
  DosMemory[$6674] := 0;
  DosMemory[$6675] := 1;
  DosMemory[$6676] := 0;
  DosMemory[$6677] := $10;
  for mapColumn := 0 to 15 do
  begin
    mapTablePhysical := $10000 + $0100 + mapColumn * 4;
    RealModeMemory[mapTablePhysical] := Byte($0200 + mapColumn * 32);
    RealModeMemory[mapTablePhysical + 1] := Byte(($0200 + mapColumn * 32) shr 8);
    RealModeMemory[mapTablePhysical + 2] := 0;
    RealModeMemory[mapTablePhysical + 3] := $30;
    for mapRow := 0 to 31 do
    begin
      mapGridPhysical := $30000 + $0200 + mapColumn * 32 + mapRow;
      RealModeMemory[mapGridPhysical] := 0;
    end;
  end;
  if FUN_1000_0961(0, 10, 10) <> 1 then
    Halt(101);

  mapGridPhysical := $30000 + $0200 + 8 * 32 + 8;
  RealModeMemory[mapGridPhysical] := $08;
  DosMemory[$6605] := 1;
  if FUN_1000_0961(0, 10, 10) <> 0 then
    Halt(102);

  DosMemory[$6605] := 0;
  mapGridPhysical := $30000 + $0200 + 10 * 32 + 10;
  RealModeMemory[mapGridPhysical] := $08;
  DosMemory[$14C1] := 1;
  if FUN_1000_0961(0, 10, 10) <> 1 then
    Halt(103);

  RegisterSS := $1000;
  RegisterBP := $0100;
  RegisterSI := $0030;
  RegisterAX := $5A00;
  RegisterCarryFlag := True;
  RegisterZeroFlag := True;
  RealModeMemory[$10108] := Ord('7');
  if FUN_24dd_350e <> '7' then
    Halt(104);
  if (RegisterSI <> $0031) or (RegisterAX <> $5A37) or
     RegisterCarryFlag or RegisterZeroFlag then
    Halt(105);

  RegisterBP := $1000;
  RegisterSI := $0028;
  RegisterAX := $A500;
  RealModeMemory[$11000] := 0;
  if FUN_24dd_350e <> '0' then
    Halt(106);
  if (RegisterSI <> $0028) or (RegisterAX <> $A530) or
     RegisterCarryFlag or RegisterZeroFlag then
    Halt(107);

  RegisterSI := 0;
  RegisterAX := $A500;
  RealModeMemory[$10FD8] := 0;
  if FUN_24dd_350e <> '0' then
    Halt(110);
  if (RegisterSI <> 0) or not RegisterZeroFlag or RegisterCarryFlag then
    Halt(111);

  RegisterSS := $2000;
  RegisterBP := $FFF0;
  RegisterSI := $0048;
  RealModeMemory[$20010] := Ord('X');
  if FUN_24dd_350e <> 'X' then
    Halt(108);
  if RegisterSI <> $0049 then
    Halt(109);

  RegisterSS := $FFFF;
  RegisterBP := 0;
  RegisterSI := $0048;
  RegisterAX := $C500;
  RealModeMemory[$00010] := Ord('Y');
  if FUN_24dd_350e <> 'Y' then
    Halt(112);
  if (RegisterSI <> $0049) or (RegisterAX <> $C559) or
     RegisterCarryFlag or RegisterZeroFlag then
    Halt(113);

  realModeAddress := $100000F0;
  RealModeMemory[$100F0] := $80;
  RealModeMemory[$100F1] := $01;
  FUN_24dd_40ec(0, realModeAddress);
  FUN_24dd_40ec(9, realModeAddress);
  if (RealModeMemory[$100F0] <> $81) or
     (RealModeMemory[$100F1] <> $03) then
    Halt(89);
  if RealModeMemory[$100F2] <> 0 then
    Halt(90);
  realModeAddress := $0000FFF8;
  RealModeMemory[$0000FFFF] := $20;
  RealModeMemory[$00000000] := $40;
  FUN_24dd_40ec(63, realModeAddress);
  FUN_24dd_40ec(64, realModeAddress);
  if (RealModeMemory[$0000FFFF] <> $A0) or
     (RealModeMemory[$00000000] <> $41) then
    Halt(91);

  sourceFarAddress := $12340200;
  destinationFarAddress := $23450100;
  RealModeMemory[$12540] := 2;
  RealModeMemory[$12541] := Ord('A');
  RealModeMemory[$12542] := Ord('B');
  RealModeMemory[$23550] := 2;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$23552] := Ord('B');
  RegisterZeroFlag := False;
  RegisterCarryFlag := True;
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if not RegisterZeroFlag or RegisterCarryFlag then
    Halt(92);

  RealModeMemory[$23550] := 1;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$12540] := 1;
  RealModeMemory[$12541] := Ord('B');
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if RegisterZeroFlag or RegisterCarryFlag then
    Halt(93);

  RealModeMemory[$23551] := Ord('C');
  RealModeMemory[$12541] := Ord('B');
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if RegisterZeroFlag or not RegisterCarryFlag then
    Halt(94);

  RealModeMemory[$23550] := 2;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$23552] := Ord('B');
  RealModeMemory[$12540] := 3;
  RealModeMemory[$12541] := Ord('A');
  RealModeMemory[$12542] := Ord('B');
  RealModeMemory[$12543] := Ord('C');
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if RegisterZeroFlag or RegisterCarryFlag then
    Halt(95);

  RealModeMemory[$23550] := 3;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$23552] := Ord('B');
  RealModeMemory[$23553] := Ord('C');
  RealModeMemory[$12540] := 2;
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if RegisterZeroFlag or not RegisterCarryFlag then
    Halt(96);

  RealModeMemory[$23550] := 2;
  RealModeMemory[$12540] := 0;
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if not RegisterZeroFlag or RegisterCarryFlag then
    Halt(97);

  destinationFarAddress := $2345FFFF;
  RealModeMemory[$3344F] := 1;
  RealModeMemory[$23450] := Ord('A');
  RealModeMemory[$12540] := 1;
  RealModeMemory[$12541] := Ord('A');
  FUN_24dd_3f86(destinationFarAddress, sourceFarAddress);
  if not RegisterZeroFlag or RegisterCarryFlag then
    Halt(98);

  RealModeMemory[$23550] := 5;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$23552] := Ord('B');
  RealModeMemory[$23553] := Ord('C');
  RealModeMemory[$23554] := Ord('D');
  RealModeMemory[$23555] := Ord('E');
  RealModeMemory[$12540] := 2;
  RealModeMemory[$12541] := Ord('B');
  RealModeMemory[$12542] := Ord('C');
  searchResult := FUN_24dd_3f40($23450100, $12340200);
  if searchResult <> 2 then
    Halt(99);

  RealModeMemory[$23550] := 6;
  RealModeMemory[$23551] := Ord('A');
  RealModeMemory[$23552] := Ord('B');
  RealModeMemory[$23553] := Ord('X');
  RealModeMemory[$23554] := Ord('A');
  RealModeMemory[$23555] := Ord('B');
  RealModeMemory[$23556] := Ord('Y');
  RealModeMemory[$12540] := 3;
  RealModeMemory[$12541] := Ord('A');
  RealModeMemory[$12542] := Ord('B');
  RealModeMemory[$12543] := Ord('Y');
  searchResult := FUN_24dd_3f40($23450100, $12340200);
  if searchResult <> 4 then
    Halt(100);

  RealModeMemory[$12541] := Ord('Z');
  RealModeMemory[$12542] := Ord('Z');
  searchResult := FUN_24dd_3f40($23450100, $12340200);
  if searchResult <> 0 then
    Halt(101);
  RealModeMemory[$12540] := 0;
  searchResult := FUN_24dd_3f40($23450100, $12340200);
  if searchResult <> 0 then
    Halt(102);
  RealModeMemory[$12540] := 7;
  searchResult := FUN_24dd_3f40($23450100, $12340200);
  if searchResult <> 0 then
    Halt(103);

  RealModeMemory[$3344D] := 3;
  RealModeMemory[$3344E] := Ord('A');
  RealModeMemory[$3344F] := Ord('B');
  RealModeMemory[$23450] := Ord('C');
  RealModeMemory[$12540] := 2;
  RealModeMemory[$12541] := Ord('B');
  RealModeMemory[$12542] := Ord('C');
  searchResult := FUN_24dd_3f40($2345FFFD, $12340200);
  if searchResult <> 2 then
    Halt(104);

  RealModeMemory[$12540] := 3;
  RealModeMemory[$12541] := Ord('A');
  RealModeMemory[$12542] := Ord('B');
  RealModeMemory[$12543] := Ord('C');
  for builderIndex := 0 to 180 do
    RealModeMemory[$23550 + builderIndex] := $FF;
  FUN_24dd_3b22($12340200, $23450100);
  if (RealModeMemory[$23550] <> 0) or
     (RealModeMemory[$23552] <> $B0) or
     (RealModeMemory[$23553] <> $D7) then
    Halt(105);
  for builderIndex := 4 to 47 do
    if RealModeMemory[$23550 + builderIndex] <> 0 then
      Halt(106);
  if (RealModeMemory[$23580] <> Ord('A')) or
     (RealModeMemory[$23581] <> Ord('B')) or
     (RealModeMemory[$23582] <> Ord('C')) or
     (RealModeMemory[$23583] <> 0) then
    Halt(107);

  for builderIndex := 0 to 180 do
    RealModeMemory[$23550 + builderIndex] := $FF;
  RealModeMemory[$12540] := 80;
  for builderIndex := 1 to 80 do
    RealModeMemory[$12540 + builderIndex] := Ord('K');
  FUN_24dd_3b22($12340200, $23450100);
  if (RealModeMemory[$23580] <> Ord('K')) or
     (RealModeMemory[$235CE] <> Ord('K')) or
     (RealModeMemory[$235CF] <> 0) or
     (RealModeMemory[$235D0] <> $FF) then
    Halt(108);

  for builderIndex := 0 to 180 do
    RealModeMemory[$23550 + builderIndex] := $FF;
  RealModeMemory[$12540] := 4;
  RealModeMemory[$12541] := Ord('X');
  RealModeMemory[$12542] := 0;
  RealModeMemory[$12543] := Ord('Y');
  RealModeMemory[$12544] := Ord('Z');
  FUN_24dd_3b22($12340200, $23450100);
  if (RealModeMemory[$23580] <> Ord('X')) or
     (RealModeMemory[$23581] <> 0) or
     (RealModeMemory[$23582] <> $FF) then
    Halt(109);

  for builderIndex := 0 to 180 do
    RealModeMemory[$23550 + builderIndex] := $FF;
  RealModeMemory[$12540] := 0;
  FUN_24dd_3b22($12340200, $23450100);
  if (RealModeMemory[$23580] <> 0) or
     (RealModeMemory[$23581] <> $FF) then
    Halt(110);

  commandLineSegment := $3456;
  DosMemory[$640C] := commandLineSegment and $FF;
  DosMemory[$640D] := commandLineSegment shr 8;
  RealModeMemory[$345E0] := 19;
  RealModeMemory[$345E1] := Ord(' ');
  RealModeMemory[$345E2] := Ord(' ');
  RealModeMemory[$345E3] := Ord('a');
  RealModeMemory[$345E4] := Ord('l');
  RealModeMemory[$345E5] := Ord('p');
  RealModeMemory[$345E6] := Ord('h');
  RealModeMemory[$345E7] := Ord('a');
  RealModeMemory[$345E8] := Ord(' ');
  RealModeMemory[$345E9] := Ord('b');
  RealModeMemory[$345EA] := Ord('e');
  RealModeMemory[$345EB] := Ord('t');
  RealModeMemory[$345EC] := Ord('a');
  RealModeMemory[$345ED] := Ord(' ');
  RealModeMemory[$345EE] := Ord('g');
  RealModeMemory[$345EF] := Ord('a');
  RealModeMemory[$345F0] := Ord('m');
  RealModeMemory[$345F1] := Ord('m');
  RealModeMemory[$345F2] := Ord('a');
  RealModeMemory[$345F3] := Ord(' ');
  searchResult := FUN_24dd_3d2f;
  if searchResult <> 3 then
    Halt(111);
  RegisterDX := 1;
  FUN_24dd_3d36;
  if (RegisterBX <> 1) or (RegisterDX <> 0) or (RegisterAX <> 5) then
    Halt(112);
  RealModeMemory[$345E0] := 0;
  if FUN_24dd_3d2f <> 0 then
    Halt(113);

  DosMemory[$6420] := 0;
  RegisterAX := 3;
  RegisterDX := 2;
  RegisterCX := 5;
  RegisterBX := 4;
  if FUN_24dd_3d80 <> 15 then
    Halt(114);
  if RegisterAX <> 15 then
    Halt(115);
  if RegisterDX <> $0016 then
    Halt(118);
  DosMemory[$6420] := 2;
  RegisterAX := $FFFF;
  RegisterDX := 0;
  RegisterCX := $FFFF;
  RegisterBX := 0;
  if FUN_24dd_3d80 <> 1 then
    Halt(116);
  if (RegisterAX <> 1) or (RegisterDX <> $FFFE) then
    Halt(117);

  RegisterDS := $1111;
  RegisterES := $2222;
  RegisterSI := $3456;
  RegisterDI := $0100;
  RegisterAX := $BEEF;
  RegisterCX := $1234;
  RegisterDirectionFlag := True;
  RegisterZeroFlag := True;
  RegisterCarryFlag := True;
  for wordIndex := 0 to 5 do
  begin
    CodeMemory[$0576 + wordIndex * 2] := $10 + wordIndex;
    CodeMemory[$0577 + wordIndex * 2] := $A0 + wordIndex;
    RealModeMemory[$11686 + wordIndex * 2] := $EE;
    RealModeMemory[$11687 + wordIndex * 2] := $EE;
    RealModeMemory[$22320 + wordIndex * 2] := $FF;
    RealModeMemory[$22321 + wordIndex * 2] := $FF;
  end;
  FUN_24dd_0582;
  for wordIndex := 0 to 5 do
    if (RealModeMemory[$22320 + wordIndex * 2] <> $10 + wordIndex) or
       (RealModeMemory[$22321 + wordIndex * 2] <> $A0 + wordIndex) then
      Halt(119);
  if (RegisterDI <> $0100) or (RegisterSI <> $3456) or
     (RegisterDS <> $1111) or (RegisterAX <> $0582) or (RegisterCX <> 0) then
    Halt(120);
  if RegisterDirectionFlag then
    Halt(128);
  if RegisterZeroFlag or RegisterCarryFlag then
    Halt(129);

  RegisterDI := $FFFA;
  FUN_24dd_0582;
  for wordIndex := 0 to 5 do
  begin
    realModeAddress := ((Longint(RegisterES) * 16) +
      (($FFFA + wordIndex * 2) and $FFFF)) and $FFFFF;
    if (RealModeMemory[realModeAddress] <> $10 + wordIndex) or
       (RealModeMemory[(realModeAddress + 1) and $FFFFF] <> $A0 + wordIndex) then
      Halt(121);
  end;
  if (RegisterDI <> $FFFA) or RegisterZeroFlag or not RegisterCarryFlag then
    Halt(122);
  RegisterDI := 0;
  FUN_24dd_0582;
  if not RegisterZeroFlag or RegisterCarryFlag then
    Halt(130);

  RegisterDS := $1111;
  RegisterES := $2222;
  RegisterSI := $3456;
  RegisterDI := $0200;
  RegisterAX := $BEEF;
  RegisterCX := $1234;
  RegisterDirectionFlag := True;
  for wordIndex := 0 to 5 do
  begin
    CodeMemory[$05DC + wordIndex * 2] := $20 + wordIndex;
    CodeMemory[$05DD + wordIndex * 2] := $B0 + wordIndex;
    RealModeMemory[$116EC + wordIndex * 2] := $EE;
    RealModeMemory[$116ED + wordIndex * 2] := $EE;
    RealModeMemory[$22420 + wordIndex * 2] := $FF;
    RealModeMemory[$22421 + wordIndex * 2] := $FF;
  end;
  FUN_24dd_05e8;
  for wordIndex := 0 to 5 do
    if (RealModeMemory[$22420 + wordIndex * 2] <> $20 + wordIndex) or
       (RealModeMemory[$22421 + wordIndex * 2] <> $B0 + wordIndex) then
      Halt(123);
  if (RegisterDI <> $0200) or (RegisterSI <> $3456) or
     (RegisterDS <> $1111) or (RegisterAX <> $05E8) or (RegisterCX <> 0) or
     RegisterDirectionFlag then
    Halt(124);

  RegisterES := $2222;
  RegisterDI := $0300;
  RegisterAX := $1234;
  RegisterCX := $ABCD;
  RealModeMemory[$2251F] := $AA;
  RealModeMemory[$2252C] := $BB;
  FUN_24dd_05fd;
  for wordIndex := 0 to 3 do
    if (RealModeMemory[$22520 + wordIndex * 2] <> 0) or
       (RealModeMemory[$22521 + wordIndex * 2] <> 0) then
      Halt(125);
  if (RealModeMemory[$22528] <> $34) or (RealModeMemory[$22529] <> $12) or
     (RealModeMemory[$2252A] <> $CD) or (RealModeMemory[$2252B] <> 0) then
    Halt(126);
  if (RealModeMemory[$2251F] <> $AA) or (RealModeMemory[$2252C] <> $BB) or
     (RegisterDI <> $0300) or (RegisterAX <> $00CD) or
     (RegisterCX <> $ABCD) then
    Halt(127);

  StackPointerD8 := $1000;
  RegisterSI := $00FE;
  RegisterDI := $5678;
  RegisterDS := $1111;
  RegisterES := $2222;
  RegisterCX := $FFFF;
  for wordIndex := 0 to 11 do
  begin
    CodeMemory[($00FE + wordIndex) and $FFFF] := $40 + wordIndex;
    DosMemory[($0FF4 + wordIndex) and $FFFF] := $FF;
  end;
  FUN_24dd_0642;
  for wordIndex := 0 to 11 do
    if DosMemory[$0FF4 + wordIndex] <> $40 + wordIndex then
      Halt(128);
  if (StackPointerD8 <> $0FF4) or (RegisterSI <> $00FE) or
     (RegisterDI <> $5678) or (RegisterDS <> $1111) or
     (RegisterES <> $2222) or (RegisterCX <> 0) then
    Halt(129);

  DosMemory[$67F9] := $A5;
  DosMemory[$67FA] := $01;
  DosMemory[$7688] := $02;
  DosMemory[$7689] := $B6;
  DosMemory[$768F] := $C7;
  DosMemory[$7690] := $03;
  DosMemory[$7691] := $D8;
  FUN_235c_135f;
  if (DosMemory[$67FA] <> 0) or (DosMemory[$7688] <> 0) or
     (DosMemory[$7690] <> 0) then
    Halt(130);
  if (DosMemory[$67F9] <> $A5) or (DosMemory[$7689] <> $B6) or
     (DosMemory[$768F] <> $C7) or (DosMemory[$7691] <> $D8) then
    Halt(131);

  if FUN_235c_06d7($FFFF, 0, 0, 1) <> $0000FFFF then
    Halt(132);
  if FUN_235c_06d7($FFFF, -1, 0, 0) <> -1 then
    Halt(133);
  if FUN_235c_06d7(5, 2, 4, 2) <> $00020004 then
    Halt(134);

  DosMemory[$67FB] := $AA;
  DosMemory[$67FC] := $01;
  DosMemory[$67FD] := $BB;
  for wordIndex := 0 to 11 do
    DosMemory[$680D + wordIndex] := $FF;
  FUN_235c_091d(1);
  if DosMemory[$67FD] <> 0 then
    Halt(135);
  for wordIndex := 0 to 9 do
    if DosMemory[$680E + wordIndex] <> 0 then
      Halt(140 + wordIndex);
  if (DosMemory[$67FB] <> $AA) or (DosMemory[$67FC] <> $01) or
     (DosMemory[$680D] <> $FF) or (DosMemory[$6818] <> $FF) then
    Halt(136);

  DosMemory[$6854] := $FF;
  DosMemory[$6E64] := $12;
  DosMemory[$6E65] := $34;
  DosMemory[$6E66] := $56;
  DosMemory[$6E67] := $78;
  DosMemory[$6E6C] := $AA;
  DosMemory[$6E6D] := $AA;
  DosMemory[$6E6E] := $BB;
  DosMemory[$6E6F] := $BB;
  FUN_235c_0aad(1);
  if (DosMemory[$6854] <> 1) or (DosMemory[$6E6C] <> $12) or
     (DosMemory[$6E6D] <> $34) or (DosMemory[$6E6E] <> $56) or
     (DosMemory[$6E6F] <> $78) then
    Halt(137);

  DosMemory[$6E64] := $11;
  DosMemory[$6E65] := $12;
  DosMemory[$6E66] := $13;
  DosMemory[$6E67] := $14;
  DosMemory[$6E68] := $21;
  DosMemory[$6E69] := $22;
  DosMemory[$6E6A] := $23;
  DosMemory[$6E6B] := $24;
  DosMemory[$6854] := 1;
  FUN_235c_0ad3;
  if (DosMemory[$6854] <> 2) or (DosMemory[$6E6C] <> $21) or
     (DosMemory[$6E6F] <> $24) then
    Halt(167);
  DosMemory[$6854] := 0;
  FUN_235c_0ad3;
  if (DosMemory[$6854] <> 1) or (DosMemory[$6E6C] <> $11) or
     (DosMemory[$6E6F] <> $14) then
    Halt(168);

  DosMemory[$6E6C] := 0;
  DosMemory[$6E6D] := 0;
  DosMemory[$6E6E] := 0;
  DosMemory[$6E6F] := $20;
  DosMemory[$6A58] := 0;
  DosMemory[$6A59] := 0;
  DosMemory[$6A5A] := 1;
  DosMemory[$6A5B] := 0;
  DosMemory[$6A5C] := 2;
  DosMemory[$6A5D] := 0;
  DosMemory[$6A58 + 511 * 2] := 3;
  DosMemory[$6A58 + 511 * 2 + 1] := 0;
  DosMemory[$7286] := $A1;
  DosMemory[$7287] := $B2;
  DosMemory[$7288] := $C3;
  DosMemory[$7289] := $D4;
  FUN_235c_11aa;
  if (RealModeMemory[$20000] <> $A1) or
     (RealModeMemory[$20001] <> $B2) or
     (RealModeMemory[$20002] <> $C3) or
     (RealModeMemory[$201FF] <> $D4) then
    Halt(169);

  DosMemory[$6886] := $AA;
  FUN_235c_0b7c;
  if (DosMemory[$6886] <> $AA) or (DosMemory[$6887] <> 0) or
     (DosMemory[$7207] <> 1) or (DosMemory[$7286] <> $80) or
     (DosMemory[$7305] <> $FF) or (DosMemory[$7686] <> $FF) then
    Halt(138);

  for index := 0 to 79 do
    DosMemory[$6804 + index] := 0;
  DosMemory[$6808] := Ord('X');
  DosMemory[$6804 + 7 * 10 + 4] := Ord('Q');
  expectedByte := FUN_235c_0a1e('Q');
  if expectedByte <> 1 then
    Halt(139);
  expectedByte := FUN_235c_0a1e('Z');
  if expectedByte <> 0 then
    Halt(140);

  DosMemory[$6A57] := $AA;
  for index := $6A58 to $6E58 do
    DosMemory[index] := $FF;
  FUN_235c_0aeb;
  if (DosMemory[$6A57] <> $AA) or (DosMemory[$6A58] <> 0) or
     (DosMemory[$6E57] <> 0) or (DosMemory[$6E58] <> $FF) then
    Halt(141);

  for index := 0 to 7 do
    DosMemory[$67FC + index] := 0;
  DosMemory[$67FC] := 1;
  DosMemory[$67FD] := 0;
  DosMemory[$67CE] := $10;
  FUN_235c_095c($A5, $5A, $1234, $5678);
  if DosMemory[$67CE] <> $11 then
    Halt(142);
  if DosMemory[$67FD] <> 1 then
    Halt(143);
  if DosMemory[$680E] <> $34 then Halt(144);
  if DosMemory[$680F] <> $12 then Halt(145);
  if DosMemory[$6810] <> $78 then Halt(146);
  if DosMemory[$6811] <> $56 then Halt(147);
  if DosMemory[$6812] <> $5A then Halt(148);
  if (DosMemory[$6813] <> 0) or (DosMemory[$6814] <> 0) or
     (DosMemory[$6815] <> 0) or (DosMemory[$6816] <> 0) then Halt(149);
  if DosMemory[$6817] <> $A5 then Halt(150);

  DosMemory[$67FC] := 1;
  DosMemory[$67FD] := 1;
  DosMemory[$67FE] := 1;
  DosMemory[$67CE] := 3;
  DosMemory[$6808] := Ord('R');
  DosMemory[$680E + 4] := Ord('R');
  DosMemory[$6818] := Ord('S');
  FUN_235c_09eb('R');
  if (DosMemory[$67FC] <> 0) or (DosMemory[$67FD] <> 0) or
     (DosMemory[$67FE] <> 1) or (DosMemory[$67CE] <> 1) or
     (DosMemory[$6808] <> 0) or (DosMemory[$6812] <> 0) or
     (DosMemory[$680E + 4] <> 0) or (DosMemory[$6818] <> Ord('S')) then
    Halt(151);

  for index := 0 to 7 do
    DosMemory[$67FC + index] := 0;
  DosMemory[$67FC] := 1;
  DosMemory[$67CE] := 1;
  DosMemory[$6804] := 0;
  DosMemory[$6805] := 1;
  DosMemory[$6806] := 0;
  DosMemory[$6807] := $10;
  DosMemory[$6809] := 0;
  DosMemory[$680A] := 0;
  DosMemory[$680B] := 5;
  DosMemory[$680C] := 0;
  RealModeMemory[$10100 + 6] := 0;
  RealModeMemory[$10100 + 7] := 0;
  RealModeMemory[$10100 + 8] := 4;
  RealModeMemory[$10100 + 9] := 0;
  FUN_235c_0a51;
  if (DosMemory[$67FC] <> 0) or (DosMemory[$67CE] <> 0) or
     (DosMemory[$6804] <> 0) or (DosMemory[$680D] <> 0) then
    Halt(152);

  DosMemory[$6A58] := $02;
  DosMemory[$6A59] := $00;
  DosMemory[$6A5A] := $00;
  DosMemory[$6A5B] := $80;
  DosMemory[$6E6C] := $00;
  DosMemory[$6E6D] := $02;
  DosMemory[$6E6E] := $00;
  DosMemory[$6E6F] := $10;
  FUN_235c_118c;
  if (RealModeMemory[$10200] <> $40) or
     (RealModeMemory[$10201] <> 0) or
     (RealModeMemory[$10202] <> 0) or
     (RealModeMemory[$10203] <> 0) then
    Halt(153);

  for index := 0 to 645 do
    destinationFrameBuffer[index] := $FF;
  FUN_1ec2_0d5d($7C, 2, 3, @destinationFrameBuffer[0]);
  if (destinationFrameBuffer[0] <> $7C) or
     (destinationFrameBuffer[1] <> $7C) or
     (destinationFrameBuffer[2] <> $7C) or
     (destinationFrameBuffer[3] <> $FF) or
     (destinationFrameBuffer[319] <> $FF) or
     (destinationFrameBuffer[320] <> $7C) or
     (destinationFrameBuffer[321] <> $7C) or
     (destinationFrameBuffer[322] <> $7C) or
     (destinationFrameBuffer[323] <> $FF) then
    Halt(154);

  for index := 0 to 8 do
    RealModeMemory[$12400 + 10 * 320 + index] := $FF;
  FUN_1ec2_0b0d($12400, $7A, 10, 6, 10, 2);
  if (RealModeMemory[$12400 + 10 * 320 + 2] <> $FF) or
     (RealModeMemory[$12400 + 10 * 320 + 3] <> $7A) or
     (RealModeMemory[$12400 + 10 * 320 + 6] <> $7A) then
    Halt(185);
  for index := 0 to 8 do
    RealModeMemory[$12500 + 10 * 320 + index] := $FF;
  FUN_1ec2_0c3b($12500, 10, 4, 10, 2);
  if (RealModeMemory[$12500 + 10 * 320 + 2] <> $FF) or
     (RealModeMemory[$12500 + 10 * 320 + 3] <> $3F) or
     (RealModeMemory[$12500 + 10 * 320 + 4] <> $3E) then
    Halt(186);
  RealModeMemory[$12600 + 10 * 320 + 3] := $A1;
  RealModeMemory[$12600 + 10 * 320 + 4] := $9F;
  FUN_1ec2_09e7($12600, 4, 10, 2, 10);
  if (RealModeMemory[$12600 + 10 * 320 + 3] <> $A5) or
     (RealModeMemory[$12600 + 10 * 320 + 4] <> $9F) then
    Halt(187);

  for index := 0 to 642 do
    destinationFrameBuffer[index] := $FF;
  FUN_1ec2_0d88($44, 3, 5, @destinationFrameBuffer[0]);
  if (destinationFrameBuffer[0] <> $FF) or
     (destinationFrameBuffer[1] <> $44) or
     (destinationFrameBuffer[3] <> $44) or
     (destinationFrameBuffer[4] <> $FF) or
     (destinationFrameBuffer[320] <> $44) or
     (destinationFrameBuffer[324] <> $44) or
     (destinationFrameBuffer[325] <> $FF) or
     (destinationFrameBuffer[641] <> $44) or
     (destinationFrameBuffer[643] <> $44) or
     (destinationFrameBuffer[644] <> $FF) then
    Halt(162);

  sourceBuffer[0] := 0;
  sourceBuffer[1] := $11;
  sourceBuffer[2] := 0;
  sourceBuffer[3] := $22;
  sourceBuffer[4] := $33;
  sourceBuffer[5] := $44;
  sourceBuffer[6] := 0;
  sourceBuffer[7] := $55;
  for index := 0 to 4 do
  begin
    RealModeMemory[$12000 + index] := $EE;
    RealModeMemory[$12000 + 320 + index] := $EE;
  end;
  FUN_1ec2_0e8f(@sourceBuffer[0], $12000, 2, 4, 0, -1);
  if (RealModeMemory[$12000] <> $11) or
     (RealModeMemory[$12001] <> $EE) or
     (RealModeMemory[$12002] <> $22) or
     (RealModeMemory[$12003] <> $EE) or
     (RealModeMemory[$12000 + 320] <> $44) or
     (RealModeMemory[$12000 + 321] <> $EE) or
     (RealModeMemory[$12000 + 322] <> $55) then
    Halt(163);

  sourceBuffer[0] := 0;
  sourceBuffer[1] := $12;
  sourceBuffer[2] := $13;
  sourceBuffer[3] := $14;
  RealModeMemory[$12100] := 0;
  RealModeMemory[$12101] := 7;
  RealModeMemory[$12102] := 9;
  RealModeMemory[$12103] := 11;
  FUN_1ec2_1008(@sourceBuffer[0], $12100, 10, 8, 1, 4, 0, 0);
  if (RealModeMemory[$12100] <> 0) or
     (RealModeMemory[$12101] <> 7) or
     (RealModeMemory[$12102] <> $13) or
     (RealModeMemory[$12103] <> 11) then
    Halt(164);

  sourceBuffer[0] := 1;
  sourceBuffer[1] := 2;
  sourceBuffer[2] := 3;
  RealModeMemory[$12200] := 9;
  RealModeMemory[$12201] := 9;
  RealModeMemory[$12202] := 11;
  FUN_1ec2_0f44(@sourceBuffer[0], $12200, Char($FE), 10, 8, 1, 3, 0, 0);
  if (RealModeMemory[$12200] <> 7) or
     (RealModeMemory[$12201] <> 7) or
     (RealModeMemory[$12202] <> 11) then
    Halt(165);

  for index := 0 to 63 do
    sourceFrameBuffer[index] := 0;
  sourceFrameBuffer[0] := 1;
  sourceFrameBuffer[8] := 2;
  RealModeMemory[$12300 + 198 * 320 + 318] := $EE;
  RealModeMemory[$12300 + 198 * 320 + 319] := $EE;
  RealModeMemory[$12300 + 199 * 320 + 318] := $EE;
  RealModeMemory[$12300 + 199 * 320 + 319] := $EE;
  FUN_1ec2_12e6($66, @sourceFrameBuffer[0], $12300, 198, 318);
  if (RealModeMemory[$12300 + 198 * 320 + 318] <> $66) or
     (RealModeMemory[$12300 + 198 * 320 + 319] <> $EE) or
     (RealModeMemory[$12300 + 199 * 320 + 318] <> $66) or
     (RealModeMemory[$12300 + 199 * 320 + 319] <> $EE) then
    Halt(166);

  FUN_1ec2_10cf($11, $22, $33, $44);
  if (VideoPalette[$44].Red <> $33) or
     (VideoPalette[$44].Green <> $22) or
     (VideoPalette[$44].Blue <> $11) then
    Halt(173);
  paletteBytes[21] := $12;
  paletteBytes[22] := $34;
  paletteBytes[23] := $56;
  FUN_1ec2_0810(7, @paletteBytes[0]);
  if (VideoPalette[7].Red <> $12) or
     (VideoPalette[7].Green <> $34) or
     (VideoPalette[7].Blue <> $56) then
    Halt(188);
  VideoPalette[5].Red := $11;
  VideoPalette[5].Green := $22;
  VideoPalette[5].Blue := $33;
  sourceName[0] := 5;
  FUN_1ec2_152f(@destinationBuffer[0], @destinationBuffer[1],
    @destinationBuffer[2], @sourceName[0]);
  if (destinationBuffer[0] <> $11) or
     (destinationBuffer[1] <> $22) or
     (destinationBuffer[2] <> $33) then
    Halt(191);
  FUN_1ec2_15bb(@paletteBytes[0]);
  if (paletteBytes[15] <> $33) or
     (paletteBytes[16] <> $22) or
     (paletteBytes[17] <> $11) then
    Halt(195);
  paletteBytes[30] := $41;
  paletteBytes[31] := $52;
  paletteBytes[32] := $63;
  FUN_1ec2_155e(@paletteBytes[0]);
  if (VideoPalette[10].Red <> $41) or
     (VideoPalette[10].Green <> $52) or
     (VideoPalette[10].Blue <> $63) then
    Halt(197);

  for index := 0 to 767 do
    sourceFrameBuffer[index] := 0;
  sourceFrameBuffer[0] := 32;
  sourceFrameBuffer[1] := 64;
  sourceFrameBuffer[2] := 255;
  sourceFrameBuffer[3] := 10;
  sourceFrameBuffer[4] := 20;
  sourceFrameBuffer[5] := 30;
  FUN_1ec2_10ea(32, @sourceFrameBuffer[0]);
  if (VideoPalette[0].Red <> 32) or (VideoPalette[0].Green <> 63) or
     (VideoPalette[0].Blue <> 63) or (VideoPalette[1].Red <> 10) or
     (VideoPalette[1].Green <> 20) or (VideoPalette[1].Blue <> 30) then
    Halt(174);

  sourceFrameBuffer[0] := 0;
  sourceFrameBuffer[1] := 32;
  sourceFrameBuffer[2] := 63;
  FUN_1ec2_11b5(16, @sourceFrameBuffer[0]);
  if (VideoPalette[0].Red <> 31) or (VideoPalette[0].Green <> 47) or
     (VideoPalette[0].Blue <> 63) then
    Halt(175);

  sourceFrameBuffer[0] := $12;
  sourceFrameBuffer[63999] := $34;
  destinationFrameBuffer[0] := $AA;
  destinationFrameBuffer[63999] := $AA;
  FUN_1ec2_13b0(@destinationFrameBuffer[0], @sourceFrameBuffer[0]);
  if (destinationFrameBuffer[0] <> $12) or
     (destinationFrameBuffer[63999] <> $34) then
    Halt(179);
  largeFillBuffer[0] := $AA;
  largeFillBuffer[63999] := $AA;
  largeFillBuffer[64000] := $BB;
  FUN_1ec2_13d3(@largeFillBuffer[0]);
  if (largeFillBuffer[0] <> 0) or (largeFillBuffer[63999] <> 0) or
     (largeFillBuffer[64000] <> $BB) then
    Halt(180);

  RealModeMemory[$10000 + 643] := $FF;
  FUN_1ec2_0dc8($10000, 'P', 2, 3);
  if RealModeMemory[$10000 + 643] <> Ord('P') then
    Halt(155);
  FUN_1ec2_0dc8($10000, #0, 2, 3);
  FUN_1ec2_0dc8($10000, 'X', -1, 3);
  FUN_1ec2_0dc8($10000, 'X', 158, 3);
  if (RealModeMemory[$10000 + 643] <> Ord('P')) or
     (RealModeMemory[$10000 + 643 + 1] <> 0) then
    Halt(156);

  RealModeMemory[$10000 + 964] := $FF;
  FUN_1ec2_0e06($10000, 2, 3, 4);
  if RealModeMemory[$10000 + 964] <> 11 then
    Halt(157);
  FUN_1ec2_0e06($10000, $27, 3, 4);
  if RealModeMemory[$10000 + 964] <> $27 then
    Halt(158);

  RealModeMemory[$10000 + 964] := $A1;
  FUN_1ec2_0e4a($10000, 3, 4);
  if RealModeMemory[$10000 + 964] <> $A5 then
    Halt(159);
  RealModeMemory[$10000 + 964] := $9F;
  FUN_1ec2_0e4a($10000, 3, 4);
  if RealModeMemory[$10000 + 964] <> $9F then
    Halt(160);
  for index := 0 to 255 do
    sourceFrameBuffer[index] := 0;
  sourceFrameBuffer[2] := 1;
  RealModeMemory[$10000 + 5 * 320 + 7] := $A0;
  RealModeMemory[$10000 + 5 * 320 + 8] := $A2;
  FUN_1ec2_0734(#1, $10000, @sourceFrameBuffer[0], 5, 5);
  if (RealModeMemory[$10000 + 5 * 320 + 7] <> $A4) or
     (RealModeMemory[$10000 + 5 * 320 + 8] <> $A2) then
    Halt(189);
  for index := 0 to 255 do
    sourceFrameBuffer[index] := 0;
  sourceFrameBuffer[2] := $45;
  RealModeMemory[$10000 + 5 * 320 + 17] := $EE;
  FUN_1ec2_01df(#0, #0, $10000, @sourceFrameBuffer[0], 5, 5);
  if RealModeMemory[$10000 + 5 * 320 + 17] <> $45 then
    Halt(190);
  for index := 0 to 255 do
    sourceFrameBuffer[index] := 0;
  sourceFrameBuffer[2] := $80;
  sourceFrameBuffer[3] := $70;
  FUN_1ec2_0386(#0, #0, $10000, @sourceFrameBuffer[0], 5, 5);
  if (RealModeMemory[$10000 + 5 * 320 + 17] <> $7B) or
     (RealModeMemory[$10000 + 5 * 320 + 16] <> 0) then
    Halt(193);

  for index := 0 to 4 do
  begin
    RealModeMemory[$10000 + 647 + index] := $FF;
    RealModeMemory[$10000 + 967 + index] := $FF;
  end;
  FUN_1ec2_12ad($10000, $33, 2, 5, 7);
  if (RealModeMemory[$10000 + 646] <> 0) or
     (RealModeMemory[$10000 + 647] <> $33) or
     (RealModeMemory[$10000 + 651] <> $33) or
     (RealModeMemory[$10000 + 652] <> 0) or
     (RealModeMemory[$10000 + 967] <> $33) or
     (RealModeMemory[$10000 + 971] <> $33) then
    Halt(161);

  for index := 0 to 258 do
    fillBuffer[index] := $FF;
  FUN_24dd_4905($A5, 0, @fillBuffer[1]);
  for index := 0 to 258 do
    if fillBuffer[index] <> $FF then
      Halt(46);
  FUN_24dd_4905($A5, 257, @fillBuffer[1]);
  if (fillBuffer[0] <> $FF) or (fillBuffer[258] <> $FF) then
    Halt(47);
  for index := 1 to 257 do
    if fillBuffer[index] <> $A5 then
      Halt(48);

  for index := 0 to 65536 do
    largeFillBuffer[index] := $FF;
  FUN_24dd_4905($A5, -1, @largeFillBuffer[1]);
  if (largeFillBuffer[0] <> $FF) or (largeFillBuffer[65536] <> $FF) then
    Halt(51);
  for index := 1 to 65535 do
    if largeFillBuffer[index] <> $A5 then
      Halt(52);

  DosMemory[$6425] := $A5;
  for index := $6426 to $7B51 do
    DosMemory[index] := $FF;
  DosMemory[$7B52] := $5A;
  FUN_24dd_492c;
  if (DosMemory[$6425] <> $A5) or (DosMemory[$7B52] <> $5A) then
    Halt(49);
  for index := $6426 to $7B51 do
    if DosMemory[index] <> 0 then
      Halt(50);

  DosMemory[$768F] := $A5;
  DosMemory[$7690] := $FF;
  DosMemory[$7691] := $5A;
  DosMemory[$7692] := $FF;
  DosMemory[$7693] := $C3;
  FUN_235c_04f3;
  if (DosMemory[$768F] <> $A5) or (DosMemory[$7691] <> $5A) or
     (DosMemory[$7693] <> $C3) then
    Halt(53);
  if (DosMemory[$7690] <> 0) or (DosMemory[$7692] <> 0) then
    Halt(54);

  for index := 0 to 7 do
    copySourceBuffer[index] := index;
  FUN_24dd_3d68(5, @copySourceBuffer[1], @copySourceBuffer[0]);
  if (copySourceBuffer[0] <> 0) or (copySourceBuffer[1] <> 0) or
     (copySourceBuffer[2] <> 0) or (copySourceBuffer[3] <> 0) or
     (copySourceBuffer[4] <> 0) or (copySourceBuffer[5] <> 0) or
     (copySourceBuffer[6] <> 6) or (copySourceBuffer[7] <> 7) then
    Halt(45);

  ErrorFrameDepth := 7;
  FUN_1ea2_01f0;
  if ErrorFrameDepth <> 0 then
    Halt(1);
  GlobalWord6410 := $BEEF;
  if FUN_24dd_04ed <> $BEEF then
    Halt(2);
  if GlobalWord6410 <> 0 then
    Halt(3);
  farPointerValue.Offset := $1234;
  farPointerValue.Segment := $ABCD;
  FUN_24dd_02cb(@farPointerValue);
  if (PointerOffset63EE <> $1234) or (PointerSegment63F0 <> $ABCD) or
     (PointerOffset63F6 <> $1234) or (PointerSegment63F8 <> $ABCD) then
    Halt(22);
  farPointerValue.Offset := 0;
  farPointerValue.Segment := 0;
  FUN_24dd_02b9(@farPointerValue);
  if (farPointerValue.Offset <> $1234) or
     (farPointerValue.Segment <> $ABCD) then
    Halt(27);
  RegisterWordESDIPlus2 := $D7B3;
  GlobalWord6410 := $BEEF;
  FUN_24dd_3c03;
  if (not RegisterZeroFlag) or (GlobalWord6410 <> $BEEF) then
    Halt(30);
  RegisterWordESDIPlus2 := $0000;
  FUN_24dd_3c03;
  if RegisterZeroFlag or (GlobalWord6410 <> $0067) then
    Halt(31);

  RegisterES := $ABCD;
  RegisterDI := $FFF0;
  sourceName[0] := 5;
  sourceName[1] := Ord('L');
  sourceName[2] := Ord('I');
  sourceName[3] := Ord('E');
  sourceName[4] := Ord('R');
  sourceName[5] := Ord('O');
  for index := 6 to 80 do
    sourceName[index] := 0;
  FUN_24dd_3639(@sourceName[0], @fileControlRecord[0]);
  if (fileControlRecord[0] <> 0) or (fileControlRecord[1] <> 0) or
     (fileControlRecord[2] <> $B0) or (fileControlRecord[3] <> $D7) or
     (fileControlRecord[4] <> $80) or (fileControlRecord[5] <> 0) then
    Halt(32);
  if (fileControlRecord[12] <> $70) or (fileControlRecord[13] <> 0) or
     (fileControlRecord[14] <> $CD) or (fileControlRecord[15] <> $AB) then
    Halt(33);
  if (fileControlRecord[16] <> $0C) or (fileControlRecord[17] <> $42) or
     (fileControlRecord[18] <> $DD) or (fileControlRecord[19] <> $24) then
    Halt(34);
  if (fileControlRecord[48] <> Ord('L')) or
     (fileControlRecord[52] <> Ord('O')) or (fileControlRecord[53] <> 0) then
    Halt(35);

  sourceName[0] := 5;
  sourceName[1] := Ord('L');
  sourceName[2] := Ord('I');
  sourceName[3] := 0;
  sourceName[4] := Ord('R');
  sourceName[5] := Ord('O');
  FUN_24dd_3639(@sourceName[0], @fileControlRecord[0]);
  if (fileControlRecord[48] <> Ord('L')) or
     (fileControlRecord[49] <> Ord('I')) or
     (fileControlRecord[50] <> 0) then
    Halt(37);

  sourceName[0] := 80;
  for index := 1 to 80 do
    sourceName[index] := Ord('A');
  FUN_24dd_3639(@sourceName[0], @fileControlRecord[0]);
  if (fileControlRecord[48] <> Ord('A')) or
     (fileControlRecord[126] <> Ord('A')) or
     (fileControlRecord[127] <> 0) then
    Halt(36);
  StackPointerD8 := $2000;
  RegisterSI := $3000;
  for index := 0 to 11 do
    DosMemory[$3000 + index] := index + 1;
  FUN_24dd_0628;
  if StackPointerD8 <> $1FF4 then Halt(23);
  for index := 0 to 11 do
    if DosMemory[$1FF4 + index] <> index + 1 then
      Halt(24);

  StackPointerD8 := 5;
  RegisterSI := $1000;
  for index := 0 to 7 do
    DosMemory[$1000 + index] := index + 20;
  DosMemory[$1008] := 28;
  DosMemory[$1009] := 29;
  DosMemory[$100A] := 30;
  DosMemory[$100B] := 31;
  FUN_24dd_0628;
  if StackPointerD8 <> $FFF9 then Halt(25);
  for index := 0 to 11 do
    if DosMemory[($FFF9 + index) and $FFFF] <> index + 20 then
      Halt(26);

  StackPointerD8 := $4000;
  for index := 0 to 11 do
    DosMemory[$4000 + index] := index + 40;
  FUN_24dd_0673;
  if StackPointerD8 <> $3FF4 then Halt(28);
  for index := 0 to 11 do
    if DosMemory[$3FF4 + index] <> index + 40 then
      Halt(29);

  for index := 0 to $FFFF do
  begin
    expectedAX := Word(index + 7);
    addCarry := index + 7 > $FFFF;
    expectedDX := expectedAX shr 1;
    if addCarry then
      expectedDX := expectedDX or $8000;
    for shiftIndex := 1 to 3 do
      expectedDX := expectedDX shr 1;
    expectedAX := expectedAX and $0008;

    RegisterAX := Word(index);
    RegisterCarryFlag := True;
    RegisterZeroFlag := False;
    expectedDirectionFlag := (index and 1) <> 0;
    RegisterDirectionFlag := expectedDirectionFlag;
    actualLong := FUN_24dd_04dc;
    if actualLong <> (Longint(expectedDX) shl 16) + expectedAX then
      Halt(201);
    if (RegisterAX <> expectedAX) or (RegisterDX <> expectedDX) then
      Halt(202);
    if RegisterCarryFlag or (RegisterZeroFlag <> (expectedAX = 0)) then
      Halt(203);
    if RegisterDirectionFlag <> expectedDirectionFlag then
      Halt(204);
  end;

  if FUN_1ec2_086b(0, -32768) <> $FFFF then Halt(18);
  if FUN_1ec2_09bd($FFFF, -1) <> $FFFF then Halt(19);
  if FUN_1ec2_0ae3(0, 0) <> 0 then Halt(20);
  if FUN_1ec2_0c11($FFFF, 32767) <> 1 then Halt(21);

  for index := 0 to 7 do
  begin
    sourceBuffer[index] := index;
    destinationBuffer[index] := $FF;
  end;
  FUN_1ec2_0000(7, @destinationBuffer[0], @sourceBuffer[0]);
  for index := 0 to 3 do
    if destinationBuffer[index] <> index then
      Halt(4);
  for index := 4 to 7 do
    if destinationBuffer[index] <> $FF then
      Halt(5);

  for index := 0 to 7 do
    sourceBuffer[index] := index;
  FUN_1ec2_0000(8, @sourceBuffer[2], @sourceBuffer[0]);
  if (sourceBuffer[2] <> 0) or (sourceBuffer[3] <> 1) or
     (sourceBuffer[4] <> 2) or (sourceBuffer[5] <> 3) or
     (sourceBuffer[6] <> 2) or (sourceBuffer[7] <> 3) then
    Halt(6);

  for index := 0 to 63999 do
  begin
    sourceFrameBuffer[index] := index mod 256;
    destinationFrameBuffer[index] := $FF;
  end;
  FUN_1ea2_01a8(@destinationFrameBuffer[1], 3, 3, 5,
    @sourceFrameBuffer[2]);
  if (destinationFrameBuffer[1] <> sourceFrameBuffer[2]) or
     (destinationFrameBuffer[2] <> sourceFrameBuffer[3]) or
     (destinationFrameBuffer[3] <> sourceFrameBuffer[4]) or
     (destinationFrameBuffer[321] <> sourceFrameBuffer[7]) or
     (destinationFrameBuffer[322] <> sourceFrameBuffer[8]) or
     (destinationFrameBuffer[323] <> sourceFrameBuffer[9]) or
     (destinationFrameBuffer[641] <> sourceFrameBuffer[12]) or
     (destinationFrameBuffer[0] <> $FF) or
     (destinationFrameBuffer[4] <> $FF) then
    Halt(209);

  for index := 0 to 63999 do
  begin
    sourceFrameBuffer[index] := index mod 256;
    destinationFrameBuffer[index] := $FF;
  end;
  FUN_1ea2_01a8(@destinationFrameBuffer[10], 2, 4, 6,
    @sourceFrameBuffer[10]);
  if (destinationFrameBuffer[10] <> sourceFrameBuffer[10]) or
     (destinationFrameBuffer[13] <> sourceFrameBuffer[13]) or
     (destinationFrameBuffer[330] <> sourceFrameBuffer[16]) or
     (destinationFrameBuffer[333] <> sourceFrameBuffer[19]) or
     (destinationFrameBuffer[334] <> $FF) then
    Halt(210);

  for index := 0 to 63999 do
  begin
    sourceFrameBuffer[index] := index mod 256;
    destinationFrameBuffer[index] := $FF;
  end;
  FUN_1ec2_00a5(2, 4, @destinationFrameBuffer[0], @sourceFrameBuffer[0]);
  for index := 0 to 3 do
    if destinationFrameBuffer[index] <> sourceFrameBuffer[index] then
      Halt(8);
  for index := 0 to 3 do
    if destinationFrameBuffer[320 + index] <> sourceFrameBuffer[320 + index] then
      Halt(9);
  if destinationFrameBuffer[4] <> $FF then
    Halt(10);

  for index := 0 to 63999 do
    destinationFrameBuffer[index] := $FF;
  FUN_1ec2_13b0(@destinationFrameBuffer[0], @sourceFrameBuffer[0]);
  for index := 0 to 63999 do
    if destinationFrameBuffer[index] <> sourceFrameBuffer[index] then
      Halt(7);

  for index := $10000 to $1F9FF do
    RealModeMemory[index] := $EE;
  for backgroundRow := 0 to 201 do
  begin
    backgroundPhysical := $30000 + backgroundRow * $01F8;
    backgroundOffset := backgroundPhysical and $000F;
    backgroundSegment := backgroundPhysical shr 4;
    RealModeMemory[$28000 + backgroundRow * 4] := backgroundOffset and $FF;
    RealModeMemory[$28001 + backgroundRow * 4] := backgroundOffset shr 8;
    RealModeMemory[$28002 + backgroundRow * 4] := backgroundSegment and $FF;
    RealModeMemory[$28003 + backgroundRow * 4] := backgroundSegment shr 8;
    for backgroundColumn := 0 to $01F7 do
      RealModeMemory[backgroundPhysical + backgroundColumn] :=
        (backgroundRow + backgroundColumn) and $FF;
  end;
  DosMemory[$6674] := 0;
  DosMemory[$6675] := 0;
  DosMemory[$6676] := $00;
  DosMemory[$6677] := $28;
  DosMemory[$6684] := 0;
  DosMemory[$6685] := 0;
  DosMemory[$6686] := $00;
  DosMemory[$6687] := $10;
  DosMemory[$67B0] := 3;
  DosMemory[$67B1] := 0;
  DosMemory[$67B4] := 2;
  DosMemory[$67B5] := 0;
  DosMemory[$10] := 7;
  DosMemory[$11] := 0;
  DosMemory[$12] := 5;
  DosMemory[$13] := 0;
  FUN_1000_5e66_CopyBackground(0);
  if (RealModeMemory[$10000 + 5 * $0140 + 7] <> (2 + 3)) or
     (RealModeMemory[$10000 + 104 * $0140 + 164] <>
       ((101 + 160) and $FF)) or
     (RealModeMemory[$10000 + 105 * $0140 + 7] <> (102 + 3)) or
     (RealModeMemory[$10000 + 162 * $0140 + 164] <>
       ((159 + 160) and $FF)) or
     (RealModeMemory[$10000 + 5 * $0140 + 6] <> $EE) or
     (RealModeMemory[$10000 + 5 * $0140 + 165] <> $EE) or
     (RealModeMemory[$10000 + 163 * $0140 + 7] <> $EE) then
    Halt(211);
  DosMemory[$67B2] := 20;
  DosMemory[$67B3] := 0;
  DosMemory[$67B6] := 4;
  DosMemory[$67B7] := 0;
  DosMemory[$14] := 160;
  DosMemory[$15] := 0;
  DosMemory[$16] := 3;
  DosMemory[$17] := 0;
  FUN_1000_5e66_CopyBackground(1);
  if (RealModeMemory[$10000 + 3 * $0140 + 160] <> (4 + 20)) or
     (RealModeMemory[$10000 + 103 * $0140 + 160] <> (104 + 20)) or
     (RealModeMemory[$10000 + 2 * $0140 + 160] <> $EE) or
     (RealModeMemory[$10000 + 3 * $0140 + 159] <> $EE) then
    Halt(212);
  for index := 0 to $FFFF do
    RealModeMemory[$10000 + index] := $EE;
  DosMemory[$6670] := 0;
  DosMemory[$6671] := 0;
  DosMemory[$6672] := $00;
  DosMemory[$6673] := $20;
  WriteWordLE(@RealModeMemory[$20000], $4C, 37);
  RealModeMemory[$20000 + $18] := $2D;
  RealModeMemory[$20000 + $9A] := 0;
  FUN_1000_5e66_DrawHealthBar(0);
  if (RealModeMemory[$10000 + $A1 * $0140 + 240] <> $EE) or
     (RealModeMemory[$10000 + $A1 * $0140 + 241] <> $2D) or
     (RealModeMemory[$10000 + $A1 * $0140 + 315] <> $2D) or
     (RealModeMemory[$10000 + $A1 * $0140 + 316] <> $EE) or
     (RealModeMemory[$10000 + $A2 * $0140 + 241] <> $2D) then
    Halt(213);
  for index := 0 to $FFFF do
    RealModeMemory[$10000 + index] := $EE;
  WriteWordLE(@RealModeMemory[$20000], $4E, 1);
  RealModeMemory[$20000 + $70] := 1;
  WriteWordLE(@RealModeMemory[$20000], $7F, 25);
  WriteWordLE(@RealModeMemory[$20000], $75, 2);
  DosMemory[$0E0F] := 50;
  FUN_1000_5e66_DrawWeaponBar(0);
  if (RealModeMemory[$10000 + $A6 * $0140 + 249] <> $EE) or
     (RealModeMemory[$10000 + $A6 * $0140 + 250] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 299] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 300] <> $EE) or
     (RealModeMemory[$10000 + $A7 * $0140 + 250] <> $2D) then
    Halt(214);
  for index := 0 to $FFFF do
    RealModeMemory[$10000 + index] := $EE;
  RealModeMemory[$20000 + $70] := 0;
  WriteWordLE(@RealModeMemory[$20000], $5C, 50);
  WriteWordLE(@RealModeMemory[$20000], $5E, 0);
  DosMemory[$6480] := 100;
  DosMemory[$6481] := 0;
  DosMemory[$6482] := 0;
  DosMemory[$6483] := 0;
  FUN_1000_5e66_DrawWeaponBar(0);
  if (RealModeMemory[$10000 + $A6 * $0140 + 249] <> $EE) or
     (RealModeMemory[$10000 + $A6 * $0140 + 250] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 299] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 300] <> $EE) or
     (RealModeMemory[$10000 + $A7 * $0140 + 250] <> $2D) then
    Halt(219);
  for index := 0 to $FFFF do
    RealModeMemory[$10000 + index] := $EE;
  WriteWordLE(@RealModeMemory[$20000], $5C, 150);
  FUN_1000_5e66_DrawWeaponBar(0);
  if (RealModeMemory[$10000 + $A6 * $0140 + 255] <> $EE) or
     (RealModeMemory[$10000 + $A7 * $0140 + 255] <> $EE) then
    Halt(220);
  WriteWordLE(@RealModeMemory[$20000], $5C, 0);
  FUN_1000_5e66_DrawWeaponBar(0);
  if (RealModeMemory[$10000 + $A6 * $0140 + 254] <> $EE) or
     (RealModeMemory[$10000 + $A6 * $0140 + 255] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 354] <> $2D) or
     (RealModeMemory[$10000 + $A6 * $0140 + 355] <> $EE) or
     (RealModeMemory[$10000 + $A7 * $0140 + 255] <> $2D) then
    Halt(221);

  for index := 0 to 63999 do
    clearFrameBuffer[index] := $FF;
  FUN_1ec2_13d3(@clearFrameBuffer[0]);
  for index := 0 to 63999 do
    if clearFrameBuffer[index] <> 0 then
      Halt(17);

  BIOSVideoMode := 0;
  FUN_1ec2_13a4($0013);
  if BIOSVideoMode <> $13 then
    Halt(192);
  VideoStatusSequenceLength := 4;
  VideoStatusSequenceIndex := 0;
  VideoStatusReadSequence[0] := $08;
  VideoStatusReadSequence[1] := $00;
  VideoStatusReadSequence[2] := $00;
  VideoStatusReadSequence[3] := $08;
  FUN_1ec2_13c5;
  if VideoStatusSequenceIndex <> 4 then
    Halt(194);
  DosOutputCount := 0;
  RegisterAX := 123;
  expectedAX := FUN_24dd_01fe;
  if (DosOutputCount <> 3) or
     (DosOutputBuffer[0] <> Ord('1')) or
     (DosOutputBuffer[1] <> Ord('2')) or
     (DosOutputBuffer[2] <> Ord('3')) or
     (expectedAX <> $0303) then
    Halt(196);
  DosOutputCount := 0;
  RegisterAX := $00AF;
  FUN_24dd_021f;
  if (DosOutputCount <> 2) or
     (DosOutputBuffer[0] <> Ord('A')) or
     (DosOutputBuffer[1] <> Ord('F')) then
    Halt(198);
  DosOutputCount := 0;
  RegisterAX := $ABCD;
  FUN_24dd_0218;
  if (DosOutputCount <> 4) or
     (DosOutputBuffer[0] <> Ord('A')) or
     (DosOutputBuffer[1] <> Ord('B')) or
     (DosOutputBuffer[2] <> Ord('C')) or
     (DosOutputBuffer[3] <> Ord('D')) then
    Halt(199);

  DosMemory[$6412] := $34;
  DosMemory[$6413] := $12;
  DosMemory[$6414] := $78;
  DosMemory[$6415] := $56;
  CodeMemory[$46E7] := $5A;
  CodeMemory[$46E8] := $A5;
  actualWord := FUN_24dd_4654(1000);
  if actualWord <> 803 then
    Halt(202);
  if (DosMemory[$6412] <> $49) or (DosMemory[$6413] <> $EA) or
     (DosMemory[$6414] <> $B9) or (DosMemory[$6415] <> $CD) then
    Halt(203);

  DosMemory[$6420] := 0;
  RegisterAX := 100;
  RegisterDX := 0;
  RegisterBX := 0;
  RegisterCX := 3;
  actualLong := FUN_24dd_3dbd;
  if (actualLong <> 33) or (RegisterAX <> 33) or (RegisterDX <> 0) or
     (RegisterBX <> 0) or (RegisterCX <> 1) then
    Halt(204);

  RegisterAX := $FF9C;
  RegisterDX := $FFFF;
  RegisterBX := 0;
  RegisterCX := 3;
  actualLong := FUN_24dd_3dbd;
  if (actualLong <> -33) or (RegisterAX <> $FFDF) or
     (RegisterDX <> $FFFF) or (RegisterBX <> $FFFF) or
     (RegisterCX <> $FFFF) then
    Halt(205);

  DosMemory[$6420] := 2;
  RegisterAX := $5678;
  RegisterDX := $1234;
  RegisterBX := 1;
  RegisterCX := 0;
  actualLong := FUN_24dd_3dbd;
  if (actualLong <> $1234) or (RegisterAX <> $1234) or
     (RegisterDX <> 0) or (RegisterBX <> 0) or
     (RegisterCX <> $5678) then
    Halt(206);

  RegisterAX := $0100;
  RegisterSP := $0400;
  DosMemory[$640E] := $00;
  DosMemory[$640F] := $01;
  FUN_24dd_0530;
  if (RegisterAX <> $0100) or (RegisterSP <> $0400) then
    Halt(207);

  DosMemory[$0002] := 4;
  DosMemory[$0003] := 0;
  DosMemory[$6520] := 12;
  DosMemory[$6521] := 0;
  if not FUN_1000_5e66_IsRenderTick then
    Halt(215);
  DosMemory[$6520] := 13;
  if FUN_1000_5e66_IsRenderTick then
    Halt(216);
  DosMemory[$0002] := $FC;
  DosMemory[$0003] := $FF;
  DosMemory[$6520] := 12;
  if not FUN_1000_5e66_IsRenderTick then
    Halt(217);

  FillChar(DosMemory, SizeOf(DosMemory), 0);
  FillChar(RealModeMemory, SizeOf(RealModeMemory), 0);
  DosMemory[$0002] := 1;
  DosMemory[$6670] := $00;
  DosMemory[$6671] := $10;
  DosMemory[$6672] := $00;
  DosMemory[$6673] := $10;
  DosMemory[$6412] := $34;
  DosMemory[$6413] := $12;
  DosMemory[$6414] := $78;
  DosMemory[$6415] := $56;
  CodeMemory[$46E7] := $5A;
  CodeMemory[$46E8] := $A5;
  DosMemory[$67BA] := 3;
  DosMemory[$67BC] := $FF;
  DosMemory[$67BD] := $FF;
  playerRecordAddress := $11000;
  WriteWordLE(@RealModeMemory[playerRecordAddress], $4C, 0);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $06, $0070);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $0A, $0080);
  RealModeMemory[playerRecordAddress + $6F] := 1;
  RealModeMemory[playerRecordAddress + $9A] := 0;
  WriteWordLE(@RealModeMemory[playerRecordAddress + $AA], $4C, 1);
  WriteWordLE(@RealModeMemory[playerRecordAddress + $AA], $50, 1);
  RealModeMemory[playerRecordAddress + $AA + $6F] := 1;
  DosMemory[$67B0] := 20;
  DosMemory[$67B1] := 0;
  DosMemory[$67B4] := 20;
  DosMemory[$67B5] := 0;
  DosMemory[$67B2] := $90;
  DosMemory[$67B3] := 1;
  DosMemory[$67B6] := $C8;
  DosMemory[$67B7] := 0;
  RegisterSP := $FFFE;
  FUN_1000_5e66;
  if RegisterSP <> $FFFE then
    Halt(208);
  actualWord := Word(DosMemory[$67B0]) or (Word(DosMemory[$67B1]) shl 8);
  if actualWord <> 25 then
    Halt(200);
  actualWord := Word(DosMemory[$67B4]) or (Word(DosMemory[$67B5]) shl 8);
  if actualWord <> 25 then
    Halt(200);
  actualWord := Word(DosMemory[$67B2]) or (Word(DosMemory[$67B3]) shl 8);
  if actualWord <> 346 then
    Halt(200);
  actualWord := Word(DosMemory[$67B6]) or (Word(DosMemory[$67B7]) shl 8);
  if actualWord <> 192 then
    Halt(200);
  DosMemory[$0002] := 2;
  DosMemory[$0003] := 0;
  DosMemory[$6520] := 1;
  RealModeMemory[$10000] := $5A;
  FUN_1000_5e66;
  if RealModeMemory[$10000] <> $5A then
    Halt(218);

  FillChar(DosMemory, SizeOf(DosMemory), 0);
  FillChar(RealModeMemory, SizeOf(RealModeMemory), 0);
  DosMemory[$0002] := 1;
  DosMemory[$6670] := $00;
  DosMemory[$6671] := $10;
  DosMemory[$6672] := $00;
  DosMemory[$6673] := $10;
  DosMemory[$6688] := $00;
  DosMemory[$6689] := $20;
  DosMemory[$668A] := $00;
  DosMemory[$668B] := $10;
  playerRecordAddress := $11000;
  WriteWordLE(@RealModeMemory[playerRecordAddress], $4C, 0);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $06, 120);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $0A, 130);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $4E, 0);
  WriteWordLE(@RealModeMemory[playerRecordAddress], $73, 3);
  RealModeMemory[playerRecordAddress + $6C] := 0;
  RealModeMemory[playerRecordAddress + $6F] := 1;
  RealModeMemory[playerRecordAddress + $9A] := 1;
  DosMemory[$11A5 + 3] := 2;
  WriteWordLE(@RealModeMemory[$12000], $02, 105);
  WriteWordLE(@RealModeMemory[$12000], $06, 110);
  RealModeMemory[$12010] := 3;
  WriteWordLE(@RealModeMemory[$12014], $02, 125);
  WriteWordLE(@RealModeMemory[$12014], $06, 130);
  RealModeMemory[$12024] := 3;
  WriteWordLE(@RealModeMemory[$12028], $02, 200);
  WriteWordLE(@RealModeMemory[$12028], $06, 210);
  RealModeMemory[$12038] := $83;
  WriteWordLE(@RealModeMemory[playerRecordAddress + $AA], $4C, 1);
  WriteWordLE(@RealModeMemory[playerRecordAddress + $AA], $50, 1);
  RealModeMemory[playerRecordAddress + $AA + $6F] := 1;
  RegisterSP := $FFFE;
  FUN_1000_5e66;
  actualWord := Word(DosMemory[$67B0]) or (Word(DosMemory[$67B1]) shl 8);
  if actualWord <> 35 then
    Halt(201);
  actualWord := Word(DosMemory[$67B4]) or (Word(DosMemory[$67B5]) shl 8);
  if actualWord <> 40 then
    Halt(201);

  RegisterSS := $2000;
  RegisterDS := $1000;
  RegisterSP := $eff0;
  RegisterBP := $6789;
  RegisterDirectionFlag := True;
  RealModeMemory[$282fb] := 17;
  RealModeMemory[$282fc] := 3;
  FUN_249c_0013(Integer($8400));
  if (RealModeMemory[$282fd] <> 19) or (RegisterAX <> 275) or
     (RegisterDX <> 3) or (RegisterDI <> $8400) or
     (RegisterBP <> $6789) or (RegisterDS <> $1000) or
     (RegisterSP <> $eff4) or not RegisterDirectionFlag or RegisterCarryFlag then
    Halt(219);

  { Oracle: logical cursor input projection only, not external BIOS ABI. }
  RegisterSP := $fff8;
  FUN_249c_0000($ab4f, $cd18);
  if (BIOSCursorColumn <> 79) or (BIOSCursorRow <> 24) or
     (RegisterSP <> 0) then
    Halt(220);

  WriteLn('Liero runtime-state and memory-copy routines: PASS');
end.
