{ liero::FUN_1ec2_13b0 — copies 16000 dwords forward.
  Oracle: none; its Pascal behavior has not been compared with the DOS binary. }
procedure FUN_1ec2_13b0(param_1, param_2: Pointer);
begin
  CopyDWordsForward(param_2, param_1, 16000);
end;
