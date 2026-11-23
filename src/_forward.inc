\{ forward declarations for every routine (generated) }
# Forward declarations for procedures/functions with their parameter counts
# Format: (procedure|function) FUN_XXXX_XXXX(param1, param2, ...);

# Type definitions for Liero game structures (Turbo Pascal 7 / Free Pascal -Mtp)
# These are recovered from reverse-engineering Liero 1.33 LIERO.EXE assembly

type
  { LieroBufferObject is a record structure accessed via pointer arithmetic.
    Based on analysis of FUN_24dd_396c and FUN_24dd_397a: }
  TLieroBufferObject = record
    { Offset 0: Word - object words start (accessed as words^[0]) }
    { Offset 2: Word - magic number $37B3 checks validity }
    { Offset 8: Word - size limit (must be <= 128) }
    { Offset 10: Word - format magic $375E or $37B3 }
    { Offset 11: Word - code segment }
    { Offset 12: Word - source offset }
    { Offset 14: Word - source segment }
    { Additional fields exist for full buffer description }
  end;
  PLieroBufferObject = ^TLieroBufferObject;

  { LieroBufferSource / LieroBufferDestination - pointer to data buffer }
  PLieroBufferByte = ^Byte;

  { DOS Read/Write AFB (Assign Function Block) records }
  TLieroDosRead = record
    Count: Word;
    ReqCount: Word;
    BufPtr: Pointer;
    Status: Word;
  end;
  TLieroDosWrite = record
    Count: Word;
    Error: Word;
    Result: Word;
  end;

  { Code and data segment variables }
  LieroBufferCodeSegment = Word;
  LieroBufferObjectSegment = Word;
  LieroBufferObjectOffset = Word;
  LieroBufferSourceOffset = Word;
  LieroBufferSourceSegment = Word;
  slotOffset = Word;

  { Dispatch method function type }
  LieroDispatchMethod = function(Command: Word; Segment, ObjectOffset: Word): Word;

  { Buffer write procedure type }
  LieroInvokeBufferWrite = procedure(
    const BufferObject: PLieroBufferObject;
    const BufferSource: Pointer;
    const BufferDosWrite: TLieroDosWrite
  );

var
  { Current game object pointer }
  objectPointer: PLieroBufferObject;

  { Game object buffer - the main buffer structure }
  LieroBufferObject: PLieroBufferObject;

  { Code segment for buffers }
  LieroBufferCodeSegment: LieroBufferCodeSegment;

  { Text data segment }
  LieroTextDataSegment: segment;

  { DOS read state }
  LieroDosRead: TLieroDosRead;

  { DOS write state }
  LieroDosWrite: TLieroDosWrite;

  { Buffer write procedure }
  LieroInvokeBufferWrite: LieroInvokeBufferWrite;

  { Slot offset variable }
  slotOffset: slotOffset;

  { For function FUN_24dd_397a }
  LieroBufferObjectOffset: Word;

  { For function FUN_24dd_3b22 and others - DOS memory segment }
  RealModeMemory: array[0..65535] of Word;

  { DOS memory segment - byte array }
  DosMemory: array[0..65535] of Byte;

{ Forward declarations for procedures/functions}
function FUN_24dd_3eaf(s3, s, $CC);
function FUN_24dd_3e95(s3, s);
function FUN_24dd_3dbd;
