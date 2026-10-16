static inline unsigned short
count (void *p)
{
  unsigned char *pc = p;
  unsigned short old_count = pc[-1];
  unsigned short new_count;
  pc[-1] = 0;
  new_count = ((unsigned) pc[-2] << 8) | pc[-1];
  pc[-1] = old_count;
  return new_count;
}