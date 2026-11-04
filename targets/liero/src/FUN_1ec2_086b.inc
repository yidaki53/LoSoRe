{ liero::FUN_1ec2_086b — signed-word result ($FFFF, 0, or 1).
  Oracle: complete original-byte source review and exhaustive signed-word
  return differential. unusedWord is not read by the original near routine.
  Valid SS frame/arguments required; host ABI and caller reachability differ. }
function FUN_1ec2_086b(unusedWord: Word; value: Integer): Word;
begin
  FUN_1ec2_086b := SignWord(value);
end;
