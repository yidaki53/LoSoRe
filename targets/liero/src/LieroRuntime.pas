unit LieroRuntime;

{$MODE TP}

interface

type
  TDosMemory = array[0..$FFFF] of Byte;
  TRealModeMemory = array[0..$FFFFF] of Byte;
  TPaletteEntry = record
    Red: Byte;
    Green: Byte;
    Blue: Byte;
  end;
  TVideoPalette = array[0..255] of TPaletteEntry;

{ Logical mirrors of original DS-relative globals; host addresses are not fixed. }
const
  ErrorFrameDepthAddress = $65EE;
  GlobalWord6410Address = $6410;
  PointerOffset63EEAddress = $63EE;
  PointerSegment63F0Address = $63F0;
  PointerOffset63F6Address = $63F6;
  PointerSegment63F8Address = $63F8;
  StackPointerD8Address = $00D8;

var
  ErrorFrameDepth: Byte;
  GlobalWord6410: Word;
  PointerOffset63EE: Word;
  PointerSegment63F0: Word;
  PointerOffset63F6: Word;
  PointerSegment63F8: Word;
  StackPointerD8: Word;
  RegisterSI: Word;
  RegisterDS: Word;
  RegisterES: Word;
  RegisterDI: Word;
  RegisterWordESDIPlus2: Word;
  RegisterZeroFlag: Boolean;
  RegisterCarryFlag: Boolean;
  RegisterDirectionFlag: Boolean;
  RegisterAX: Word;
  RegisterBX: Word;
  RegisterCX: Word;
  RegisterDX: Word;
  RegisterBP: Word;
  RegisterSP: Word;
  RegisterSS: Word;
  BIOSVideoMode: Byte;
  DosOutputBuffer: array[0..$FFFF] of Byte;
  DosOutputCount: Word;
  DosMemory: TDosMemory;
  CodeMemory: TDosMemory;
  RealModeMemory: TRealModeMemory;
  VideoPalette: TVideoPalette;
  VideoStatusReadSequence: array[0..255] of Byte;
  VideoStatusSequenceLength: Word;
  VideoStatusSequenceIndex: Word;

procedure CopyDWordsForward(source, destination: Pointer; dwordCount: Word);
procedure CopyBytesForward(source, destination: Pointer; byteCount: Word);
procedure CopyCodeWordsToESDI;
procedure ClearDWords(destination: Pointer; dwordCount: Word);
function SignWord(value: Integer): Word;
function ReadVideoStatusPort: Byte;
function ReadStackByte(offset: Word): Byte;
procedure WriteWordLE(destination: Pointer; byteOffset: Word; value: Word);

implementation

procedure CopyDWordsForward(source, destination: Pointer; dwordCount: Word);
var
  sourceBytePointer: PByte;
  destinationBytePointer: PByte;
  remainingDWords: Word;
  copiedDWord: Longint;
begin
  sourceBytePointer := PByte(source);
  destinationBytePointer := PByte(destination);
  remainingDWords := dwordCount;
  while remainingDWords <> 0 do
  begin
    Move(sourceBytePointer^, copiedDWord, SizeOf(copiedDWord));
    Move(copiedDWord, destinationBytePointer^, SizeOf(copiedDWord));
    Inc(sourceBytePointer, SizeOf(copiedDWord));
    Inc(destinationBytePointer, SizeOf(copiedDWord));
    Dec(remainingDWords);
  end;
end;

procedure CopyBytesForward(source, destination: Pointer; byteCount: Word);
var
  sourceBytePointer: PByte;
  destinationBytePointer: PByte;
  remainingBytes: Word;
begin
  sourceBytePointer := PByte(source);
  destinationBytePointer := PByte(destination);
  remainingBytes := byteCount;
  while remainingBytes <> 0 do
  begin
    destinationBytePointer^ := sourceBytePointer^;
    Inc(sourceBytePointer);
    Inc(destinationBytePointer);
    Dec(remainingBytes);
  end;
end;

procedure CopyCodeWordsToESDI;
var
  sourceOffset: Word;
  sourceNextByteOffset: Word;
  destinationOffset: Word;
  destinationNextByteOffset: Word;
  sourceAddress: Longint;
  destinationAddress: Longint;
  wordIndex: Integer;
begin
  sourceOffset := RegisterAX;
  destinationOffset := RegisterDI;
  for wordIndex := 0 to 5 do
  begin
    sourceAddress := sourceOffset;
    destinationAddress := ((Longint(RegisterES) * 16) + destinationOffset) and $FFFFF;
    sourceNextByteOffset := (sourceOffset + 1) and $FFFF;
    destinationNextByteOffset := (destinationOffset + 1) and $FFFF;
    RealModeMemory[destinationAddress] := CodeMemory[sourceAddress];
    RealModeMemory[((Longint(RegisterES) * 16) + destinationNextByteOffset) and $FFFFF] :=
      CodeMemory[sourceNextByteOffset];
    sourceOffset := (sourceOffset + 2) and $FFFF;
    destinationOffset := (destinationOffset + 2) and $FFFF;
  end;
  RegisterCarryFlag := destinationOffset < RegisterDI;
  RegisterZeroFlag := RegisterDI = 0;
  RegisterCX := 0;
  RegisterDirectionFlag := False;
end;

procedure ClearDWords(destination: Pointer; dwordCount: Word);
var
  destinationBytePointer: PByte;
  remainingDWords: Word;
  zeroDWord: Longint;
begin
  destinationBytePointer := PByte(destination);
  remainingDWords := dwordCount;
  zeroDWord := 0;
  while remainingDWords <> 0 do
  begin
    Move(zeroDWord, destinationBytePointer^, SizeOf(zeroDWord));
    Inc(destinationBytePointer, SizeOf(zeroDWord));
    Dec(remainingDWords);
  end;
end;

function SignWord(value: Integer): Word;
begin
  if value < 0 then
    SignWord := $FFFF
  else if value > 0 then
    SignWord := 1
  else
    SignWord := 0;
end;

function ReadVideoStatusPort: Byte;
begin
  if VideoStatusSequenceIndex < VideoStatusSequenceLength then
  begin
    ReadVideoStatusPort := VideoStatusReadSequence[VideoStatusSequenceIndex];
    Inc(VideoStatusSequenceIndex);
  end
  else if VideoStatusSequenceLength = 0 then
    ReadVideoStatusPort := 0
  else
    ReadVideoStatusPort := VideoStatusReadSequence[VideoStatusSequenceLength - 1];
end;

function ReadStackByte(offset: Word): Byte;
var
  physicalAddress: Longint;
begin
  physicalAddress := ((Longint(RegisterSS) shl 4) + offset) and $FFFFF;
  ReadStackByte := RealModeMemory[physicalAddress];
end;

procedure WriteWordLE(destination: Pointer; byteOffset: Word; value: Word);
var
  destinationBytePointer: PByte;
begin
  destinationBytePointer := PByte(destination);
  Inc(destinationBytePointer, byteOffset);
  destinationBytePointer^ := value and $00FF;
  Inc(destinationBytePointer);
  destinationBytePointer^ := value shr 8;
end;

end.
