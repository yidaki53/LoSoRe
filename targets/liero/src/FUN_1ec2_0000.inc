{ liero::FUN_1ec2_0000 — copies floor(byteCount / 4) dwords forward.
  Oracle: scoped original-byte memory differential, entry DF=0 and valid
  disjoint nonwrapping buffers. Original flags/register/return ABI is not
  translated; ordinary caller allocation and DF provenance remain unresolved. }
procedure FUN_1ec2_0000(param_1: Word; param_2, param_3: Pointer);
begin
  CopyDWordsForward(param_3, param_2, param_1 shr 2);
end;
