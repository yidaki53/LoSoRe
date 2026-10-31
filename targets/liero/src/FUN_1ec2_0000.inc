{ liero::FUN_1ec2_0000 — copies floor(param_1 / 4) dwords forward.
  Oracle: none; its Pascal behavior has not been compared with the DOS binary. }
procedure FUN_1ec2_0000(param_1: Word; param_2, param_3: Pointer);
begin
  CopyDWordsForward(param_3, param_2, param_1 shr 2);
end;
