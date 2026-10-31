{ liero::FUN_1ec2_13d3 — clears 64000 consecutive bytes.
  Oracle: none; its Pascal behavior has not been compared with the DOS binary. }
procedure FUN_1ec2_13d3(param_1: Pointer);
begin
  ClearDWords(param_1, 16000);
end;
